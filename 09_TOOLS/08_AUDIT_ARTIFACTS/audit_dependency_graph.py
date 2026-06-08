#!/usr/bin/env python3
"""
Dependency Graph Health Audit for EMERGENTISM_ORG/
Read-only. Extracts "Depends on", markdown links, claims, and analyzes graph.
Produces a concise, human-readable audit report.
"""

import re
from collections import defaultdict, Counter
from pathlib import Path

BASE_DIR = Path("EMERGENTISM_ORG/")

# Regex patterns
DEPENDS_ON_RE = re.compile(r'(?i)^\s*[-*]?\s*depends?\s*on\s*:?\s*(.*)$')
LINK_RE = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
FRONTMATTER_RE = re.compile(r'^---\s*\n(.*?)\n---\s*\n', re.DOTALL)
AXIOM_RE = re.compile(r'(?i)axiom\s*[A-Z]\d*|Axiom\s+[A-Z]\d+')
THEOREM_RE = re.compile(r'(?i)theorem\s+[A-Z]?\d+|proof\s+of|lemma\s+\d+')
K_INVARIANT_RE = re.compile(r'(?i)K\d+|invariant\s+K\d+')
PHI_RE = re.compile(r'(?i)φ\s*·\s*ν\s*=\s*1|phi\s*cdot\s*nu|coherence\s*viability')
CLAIM_INDICATORS = [
    re.compile(r'(?i)we\s+prove'),
    re.compile(r'(?i)it\s+follows\s+that'),
    re.compile(r'(?i)therefore,?\s+'),
    re.compile(r'(?i)consequently,?\s+'),
    re.compile(r'(?i)this\s+implies'),
]

def normalize_path(ref_path, current_file):
    if not ref_path:
        return None
    if ref_path.startswith('http://') or ref_path.startswith('https://'):
        return None
    if ref_path.startswith('#'):
        return None
    ref_path = ref_path.split('#')[0]
    current_dir = current_file.parent
    if ref_path.startswith('/'):
        target = BASE_DIR / ref_path.lstrip('/')
    else:
        target = current_dir / ref_path
    try:
        target = target.resolve()
        base_resolved = BASE_DIR.resolve()
        if str(target).startswith(str(base_resolved)):
            rel = target.relative_to(base_resolved)
            return str(rel)
    except Exception:
        pass
    return str(target)

def extract_frontmatter_depends(text):
    depends = []
    m = FRONTMATTER_RE.match(text)
    if m:
        fm = m.group(1)
        for line in fm.split('\n'):
            line = line.strip()
            dm = DEPENDS_ON_RE.match(line)
            if dm:
                val = dm.group(1).strip()
                items = re.split(r'[,;]|\s+-\s*', val)
                for item in items:
                    item = item.strip().strip('"\'').strip('- ').strip()
                    if item:
                        depends.append(item)
            if re.match(r'^-\s+', line) and 'depends' in line.lower():
                val = re.sub(r'^-\s+', '', line).strip()
                depends.append(val)
    return depends

def extract_inline_depends(text):
    depends = []
    for line in text.split('\n'):
        dm = DEPENDS_ON_RE.match(line)
        if dm:
            val = dm.group(1).strip()
            items = re.split(r'[,;]', val)
            for item in items:
                item = item.strip().strip('"\'').strip()
                if item:
                    depends.append(item)
    return depends

def extract_markdown_links(text):
    return LINK_RE.findall(text)

def has_load_bearing_claims(text):
    indicators = []
    if AXIOM_RE.search(text):
        indicators.append("axiom-reference")
    if THEOREM_RE.search(text):
        indicators.append("theorem/proof-reference")
    if K_INVARIANT_RE.search(text):
        indicators.append("K-invariant-reference")
    if PHI_RE.search(text):
        indicators.append("phi-nu-formula")
    for pat in CLAIM_INDICATORS:
        if pat.search(text):
            indicators.append("deductive-claim")
            break
    return indicators

def resolve_dep(d, all_paths):
    if d in all_paths:
        return d
    if d + '.md' in all_paths:
        return d + '.md'
    matches = [p for p in all_paths if p.endswith('/' + d) or p.endswith('/' + d + '.md') or p == d or p == d + '.md']
    if matches:
        return matches[0]
    return None

def main():
    files = sorted([f for f in BASE_DIR.rglob('*.md')])
    all_paths = set()
    file_deps_declared = {}
    file_links = {}
    file_claims = {}

    for f in files:
        rel = str(f.relative_to(BASE_DIR))
        all_paths.add(rel)
        text = f.read_text(encoding='utf-8', errors='ignore')
        declared = extract_frontmatter_depends(text) + extract_inline_depends(text)
        file_deps_declared[rel] = declared
        links = []
        for label, href in extract_markdown_links(text):
            np = normalize_path(href, f)
            if np and np in all_paths:
                links.append(np)
        file_links[rel] = links
        file_claims[rel] = has_load_bearing_claims(text)

    graph = defaultdict(set)
    for rel in all_paths:
        for d in file_deps_declared.get(rel, []):
            resolved = resolve_dep(d, all_paths)
            if resolved and resolved != rel:
                graph[rel].add(resolved)
        for d in file_links.get(rel, []):
            if d != rel:
                graph[rel].add(d)

    # Tarjan SCC
    def tarjan_scc(graph):
        index_counter = [0]
        stack = []
        lowlinks = {}
        index = {}
        on_stack = {}
        sccs = []
        def strongconnect(v):
            index[v] = index_counter[0]
            lowlinks[v] = index_counter[0]
            index_counter[0] += 1
            stack.append(v)
            on_stack[v] = True
            for w in graph.get(v, []):
                if w not in index:
                    strongconnect(w)
                    lowlinks[v] = min(lowlinks[v], lowlinks[w])
                elif on_stack.get(w, False):
                    lowlinks[v] = min(lowlinks[v], index[w])
            if lowlinks[v] == index[v]:
                scc = []
                while True:
                    w = stack.pop()
                    on_stack[w] = False
                    scc.append(w)
                    if w == v:
                        break
                sccs.append(scc)
        for v in list(graph.keys()):
            if v not in index:
                strongconnect(v)
        return sccs

    sccs = tarjan_scc(graph)

    # Find shortest cycle in each nontrivial SCC
    def shortest_cycle_in_scc(nodes, graph):
        scc_set = set(nodes)
        best = None
        for start in nodes:
            dist = {start: [start]}
            queue = [start]
            while queue:
                cur = queue.pop(0)
                for nxt in sorted(graph.get(cur, [])):
                    if nxt not in scc_set:
                        continue
                    if nxt == start and len(dist[cur]) >= 2:
                        if best is None or len(dist[cur]) + 1 < len(best):
                            best = dist[cur] + [start]
                        break
                    if nxt not in dist and len(dist[cur]) < 8:
                        dist[nxt] = dist[cur] + [nxt]
                        queue.append(nxt)
        return best

    circular_clusters = []
    for scc in sccs:
        if len(scc) == 1:
            n = scc[0]
            if n in graph.get(n, set()):
                circular_clusters.append(([n], [n, n]))
        elif len(scc) > 1:
            cycle = shortest_cycle_in_scc(scc, graph)
            circular_clusters.append((sorted(scc), cycle))

    # Missing upstream
    formal_prefixes = ('01_FORMAL_SYSTEM/', '02_THE_DERIVATION/', '00_THE_TRANSCENDENTAL_TRINITY/')
    missing_upstream = []
    for rel, claims in file_claims.items():
        if not claims:
            continue
        deps = graph.get(rel, set())
        has_formal_upstream = any(d.startswith(formal_prefixes) for d in deps)
        if not has_formal_upstream and not rel.startswith(formal_prefixes):
            missing_upstream.append((rel, claims))

    over_coupled = [(rel, len(deps), sorted(deps)) for rel, deps in graph.items() if len(deps) > 10]
    over_coupled.sort(key=lambda x: -x[1])

    under_coupled = []
    for rel, claims in file_claims.items():
        if claims and len(graph.get(rel, set())) == 0:
            under_coupled.append((rel, claims))

    stale = []
    for rel, declared in file_deps_declared.items():
        for d in declared:
            if not resolve_dep(d, all_paths):
                stale.append((rel, d))

    level_order = {
        '01_FORMAL_SYSTEM/': 1,
        '02_THE_DERIVATION/': 2,
        '03_THE_PAPERS/': 3,
    }
    cross_skips = []
    for rel, deps in graph.items():
        my_level = None
        for prefix, lvl in level_order.items():
            if rel.startswith(prefix):
                my_level = lvl
                break
        if my_level is None:
            continue
        for d in deps:
            dep_level = None
            for prefix, lvl in level_order.items():
                if d.startswith(prefix):
                    dep_level = lvl
                    break
            if dep_level is not None and dep_level < my_level - 1:
                cross_skips.append((rel, d, dep_level, my_level))

    in_degree = Counter()
    for deps in graph.values():
        for d in deps:
            in_degree[d] += 1

    print("# O3 Audit: Dependency Graph Health")
    print()

    print("## Circular Dependencies (SCC Clusters)")
    print("| Representative Cycle | SCC Size | Severity | Files in Cluster |")
    print("|---------------------|----------|----------|------------------|")
    if not circular_clusters:
        print("| None detected | — | — | — |")
    else:
        for members, cycle in circular_clusters:
            size = len(members)
            if cycle is None:
                cycle_str = f"SCC of {size} nodes (no short cycle found)"
                sev = "HIGH" if size > 5 else "MEDIUM"
            else:
                cycle_str = ' → '.join(cycle)
                cyc_len = len(cycle) - 1
                sev = "CRITICAL" if cyc_len <= 3 else "HIGH" if cyc_len <= 5 else "MEDIUM"
            members_str = ', '.join(members[:4]) + ('...' if len(members) > 4 else '')
            print(f"| {cycle_str} | {size} | {sev} | {members_str} |")
    print()

    print("## Files with Missing Upstream Links")
    print("| File | Claim | Should Reference |")
    print("|------|-------|------------------|")
    if not missing_upstream:
        print("| — | — | — |")
    else:
        for rel, claims in missing_upstream:
            print(f"| {rel} | {', '.join(claims)} | Formal System or Derivation |")
    print()

    print("## Over-Coupled Files (>10 dependencies)")
    print("| File | Dependency Count | Dependencies |")
    print("|------|-----------------|--------------|")
    if not over_coupled:
        print("| — | — | — |")
    else:
        for rel, count, deps in over_coupled:
            deps_str = ', '.join(deps[:5]) + ('...' if len(deps) > 5 else '')
            print(f"| {rel} | {count} | {deps_str} |")
    print()

    print("## Under-Coupled Files (0 dependencies despite load-bearing claims)")
    print("| File | Load-Bearing Claims |")
    print("|------|--------------------|")
    if not under_coupled:
        print("| — | — |")
    else:
        for rel, claims in under_coupled:
            print(f"| {rel} | {', '.join(claims)} |")
    print()

    print("## Stale Dependencies")
    print("| File | Stale Reference | Current Canonical Path |")
    print("|------|----------------|------------------------|")
    if not stale:
        print("| — | — | — |")
    else:
        for rel, d in stale:
            print(f"| {rel} | {d} | Unknown |")
    print()

    print("## Cross-Level Dependency Skips")
    print("| File | Claims to Skip | Recommended Route |")
    print("|------|---------------|-------------------|")
    if not cross_skips:
        print("| — | — | — |")
    else:
        for rel, d, dep_lvl, my_lvl in cross_skips:
            route = "→".join([k.strip('/') for k,v in sorted(level_order.items(), key=lambda x: x[1]) if dep_lvl < v <= my_lvl-1])
            print(f"| {rel} | {d} (L{dep_lvl}→L{my_lvl}) | {route} |")
    print()

    print("## Additional Statistics")
    print(f"- Total files audited: {len(all_paths)}")
    print(f"- Files with declared dependencies: {sum(1 for v in file_deps_declared.values() if v)}")
    print(f"- Files with markdown links: {sum(1 for v in file_links.values() if v)}")
    print(f"- Files with load-bearing claims: {sum(1 for v in file_claims.values() if v)}")
    print(f"- Total edges in dependency graph: {sum(len(v) for v in graph.values())}")
    print("- Most referenced files (in-degree):")
    for f, c in in_degree.most_common(10):
        print(f"  - {f}: {c}")

if __name__ == '__main__':
    main()
