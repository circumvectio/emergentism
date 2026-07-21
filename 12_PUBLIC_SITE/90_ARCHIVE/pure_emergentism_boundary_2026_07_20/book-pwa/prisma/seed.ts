import { PrismaClient } from '@prisma/client';
import fs from 'fs';
import path from 'path';
import { remark } from 'remark';
import type { Heading } from 'mdast';
import crypto from 'crypto';

const prisma = new PrismaClient();

type MarkdownNode = {
  type: string;
  value?: string;
  url?: string;
  children?: MarkdownNode[];
};

async function main() {
  console.log('Clearing old data...');
  await prisma.nodeLink.deleteMany();
  await prisma.aIPBranch.deleteMany();
  await prisma.node.deleteMany();
  await prisma.book.deleteMany();

  console.log('Creating Book...');
  const book = await prisma.book.create({
    data: {
      title: 'The Infinite Book of Emergence',
      slug: 'the-infinite-book-of-emergence',
    },
  });

  const manuscriptDir = path.join(
    process.cwd(),
    '../../08_FRAMEWORK_SUPPORT/05_SYNTHESIS/07_DEFINITIVE_ONE_BOOK/MANUSCRIPT'
  );

  const files = fs.readdirSync(manuscriptDir)
    .filter(f => f.endsWith('.md') && f !== 'README.md')
    .sort();

  let globalOrderIndex = 0;

  for (const file of files) {
    const rawContent = fs.readFileSync(path.join(manuscriptDir, file), 'utf-8');
    const ast = remark().parse(rawContent);

    // Track the tree hierarchy to assign parentIds
    const nodeStack: { id: string; depth: number; path: string }[] = [];

    for (const child of ast.children) {
      if (child.type === 'heading') {
        const heading = child as Heading;
        const text = extractText(heading);
        const slug = generateId(text);
        const depth = heading.depth; // e.g. 1 for Chapter, 2 for Section

        // Adjust stack based on depth
        while (nodeStack.length > 0 && nodeStack[nodeStack.length - 1].depth >= depth) {
          nodeStack.pop();
        }

        const parentId = nodeStack.length > 0 ? nodeStack[nodeStack.length - 1].id : null;
        const parentPath = nodeStack.length > 0 ? nodeStack[nodeStack.length - 1].path : '';
        const currentPath = parentPath ? `${parentPath}/${slug}` : slug;

        const createdNode = await prisma.node.create({
          data: {
            bookId: book.id,
            parentId,
            path: currentPath,
            depth,
            orderIndex: globalOrderIndex++,
            title: text,
            slug,
          },
        });

        const version = await prisma.nodeVersion.create({
          data: {
            hash: contentHash(`${currentPath}\n${text}`),
            contentMd: text,
            authorId: 'system',
            nodeId: createdNode.id
          }
        });

        await prisma.node.update({
          where: { id: createdNode.id },
          data: { currentVersionId: version.id }
        });

        nodeStack.push({ id: createdNode.id, depth, path: currentPath });
      }
      else if (child.type === 'paragraph' || child.type === 'blockquote' || child.type === 'list') {
        const text = extractText(child);
        if (!text.trim()) continue;

        const slug = generateId(text.substring(0, 30));
        // Paragraph depth is parent + 1
        const parentDepth = nodeStack.length > 0 ? nodeStack[nodeStack.length - 1].depth : 0;
        const depth = parentDepth + 1;

        const parentId = nodeStack.length > 0 ? nodeStack[nodeStack.length - 1].id : null;
        const parentPath = nodeStack.length > 0 ? nodeStack[nodeStack.length - 1].path : '';
        const currentPath = parentPath ? `${parentPath}/${slug}` : slug;

        const createdNode = await prisma.node.create({
          data: {
            bookId: book.id,
            parentId,
            path: currentPath,
            depth,
            orderIndex: globalOrderIndex++,
            title: null,
            slug,
          },
        });

        const version = await prisma.nodeVersion.create({
          data: {
            hash: contentHash(`${currentPath}\n${text}`),
            contentMd: text,
            authorId: 'system',
            nodeId: createdNode.id
          }
        });

        await prisma.node.update({
          where: { id: createdNode.id },
          data: { currentVersionId: version.id }
        });
      }
    }
    console.log(`Parsed ${file}`);
  }

  console.log(`Seeding complete. Inserted ${globalOrderIndex} canonical nodes.`);
}

function extractText(node: MarkdownNode): string {
  const childText = () => (node.children ?? []).map(extractText).join('');
  if (node.type === 'text' || node.type === 'inlineCode') return node.value ?? '';
  if (node.type === 'strong') return `**${childText()}**`;
  if (node.type === 'emphasis') return `*${childText()}*`;
  if (node.type === 'link') return `[${childText()}](${node.url ?? ''})`;
  if (node.type === 'listItem') return `- ${childText()}`;

  if (node.children) {
    return node.children.map(extractText).join(node.type === 'list' ? '\n' : '');
  }
  return '';
}

function generateId(text: string): string {
  return text.toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/(^-|-$)/g, '') + '-' + Math.random().toString(36).substring(2, 7);
}

function contentHash(value: string): string {
  return crypto.createHash('sha256').update(value).digest('hex');
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
