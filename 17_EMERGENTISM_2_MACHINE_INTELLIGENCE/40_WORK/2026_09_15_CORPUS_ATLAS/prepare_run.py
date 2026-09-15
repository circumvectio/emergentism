#!/usr/bin/env python3
"""Sprint 0 private metadata run; corpus-specific declarations stay with corpus.

Reads pinned Git blobs only. Does not index, accept, publish or edit originals.
Frontmatter scalar lines are attributed literally, not interpreted as adoption.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tarfile
import uuid

DOCUMENTS = Path('/Users/Yves/Documents')
SOURCE = DOCUMENTS / '01_EMERGENTISM'
APU = DOCUMENTS / '04_CODE/01_SKYZAI_LEVELS/L5_REFLECTION/APU'
CORTEX = DOCUMENTS / '04_CODE/03_VENTURES/MENEXUS/menexus-core'
sys.path.insert(0, str(APU / 'apu.bot/scripts'))
import corpus_census as census
import corpus_collection as collection

PARITY = '12_PUBLIC_SITE/public_semantic_parity.json'
WITHHELD = '12_PUBLIC_SITE/withheld-routes.json'


def unique_pairs(pairs):
    out = {}
    for key, value in pairs:
        collection.require(key not in out, 'duplicate_json_key')
        out[key] = value
    return out


def collect_declarations(repo, pin, rows):
    by_path = {r['path']: r for r in rows if r['path'] is not None}
    declarations, issues, raw_status, registry_receipts = [], [], [], []

    def read_blob(path):
        row = by_path.get(path)
        collection.require(row is not None and row['git_type'] == 'blob'
                           and row['mode'] in {'100644', '100755'}, 'registry_or_source_not_regular')
        collection.require(row['processing']['reason'] in {None, 'format_not_supported_by_markdown_collection'}
                           and row['bytes'] <= 16 * 1024 * 1024, 'content_processing_excluded_or_oversize')
        return collection.git(repo, 'cat-file', 'blob', row['oid'])

    def declare(path, field, value, owner, locator):
        if path not in by_path:
            issues.append({'kind': 'declaration_target_outside_snapshot', 'path': path,
                           'owner': owner, 'locator': locator})
            return
        declarations.append({'path': path, 'field': field, 'value': value,
                             'basis': {'path': owner, 'oid': by_path[owner]['oid'], 'locator': locator}})

    def registry(path, version):
        raw = read_blob(path)
        obj = json.loads(raw, object_pairs_hook=unique_pairs)
        collection.require(type(obj.get('schemaVersion')) is int and obj['schemaVersion'] == version,
                           'unsupported_registry_version')
        registry_receipts.append({'path': path, 'oid': by_path[path]['oid'],
                                  'sha256': collection.sha(raw), 'schema_version': version})
        return obj

    parity = registry(PARITY, 8)
    for key, label in [('currentSurfaces', 'CURRENT_SURFACE'), ('machineSurfaces', 'MACHINE_SURFACE'),
                       ('declaredProvisional', 'PROVISIONAL_SURFACE'),
                       ('infrastructureRoutes', 'INFRASTRUCTURE')]:
        block = parity.get(key)
        nested = key in {'declaredProvisional', 'infrastructureRoutes'}
        collection.require(not nested or isinstance(block, dict), 'invalid_route_block')
        values = block.get('routes') if nested else block
        collection.require(isinstance(values, list) and all(isinstance(v, str) for v in values)
                           and len(set(values)) == len(values), 'invalid_route_list')
        for i, value in enumerate(values):
            collection.require(not value.startswith('/') and all(p not in {'', '.', '..'} for p in value.split('/')),
                               'unsafe_declared_route')
            locator = f'/{key}' + ('/routes' if nested else '') + f'/{i}'
            declare('12_PUBLIC_SITE/' + value, 'disclosure', label, PARITY, locator)
    roots = parity.get('frozenLibraryRoots')
    collection.require(isinstance(roots, list) and all(isinstance(r, str) and '/' not in r
                       and r not in {'', '.', '..'} for r in roots), 'invalid_frozen_roots')
    for i, root in enumerate(roots):
        for path in by_path:
            if path.startswith('12_PUBLIC_SITE/' + root + '/'):
                declare(path, 'disclosure', 'FROZEN_LIBRARY_ROOT', PARITY, f'/frozenLibraryRoots/{i}')

    withheld = registry(WITHHELD, 2)
    artifacts = withheld.get('artifacts')
    collection.require(isinstance(artifacts, list), 'missing_withheld_artifacts')
    seen = set()
    custody = []
    for i, row in enumerate(artifacts):
        collection.require(isinstance(row, dict) and isinstance(row.get('artifact'), str), 'invalid_withheld_row')
        name = row['artifact']
        collection.require(name not in seen and not name.startswith('/')
                           and all(p not in {'', '.', '..'} for p in name.split('/')), 'invalid_withheld_path')
        seen.add(name)
        collection.require(isinstance(row.get('sha256'), str) and re.fullmatch('[a-f0-9]{64}', row['sha256'])
                           and type(row.get('bytes')) is int and row['bytes'] >= 0
                           and isinstance(row.get('reason'), str) and isinstance(row.get('publicRoutes'), list)
                           and all(isinstance(r, str) and r.startswith('/') for r in row['publicRoutes']),
                           'invalid_withheld_custody')
        path = '12_PUBLIC_SITE/' + name
        declare(path, 'disclosure', 'WITHHELD_ARTIFACT', WITHHELD, f'/artifacts/{i}')
        if path in by_path:
            target = by_path[path]
            if target['processing']['reason'] not in {None, 'format_not_supported_by_markdown_collection'} or target['bytes'] is None or target['bytes'] > 16 * 1024 * 1024:
                custody.append({'path': path, 'matches_declared_custody': None,
                                'verification': 'NOT_CHECKED_EXCLUDED_OR_OVERSIZE',
                                'declaration': row, 'basis_locator': f'/artifacts/{i}'})
                issues.append({'kind': 'withheld_custody_not_checked', 'path': path})
                continue
            blob = read_blob(path)
            ok = len(blob) == row['bytes'] and collection.sha(blob) == row['sha256']
            custody.append({'path': path, 'matches_declared_custody': ok,
                            'declaration': row, 'basis_locator': f'/artifacts/{i}'})
            if not ok:
                issues.append({'kind': 'withheld_custody_mismatch', 'path': path})
    boundary = withheld.get('boundary')
    collection.require(isinstance(boundary, dict) and isinstance(boundary.get('artifactRoute'), str),
                       'invalid_withholding_boundary')
    declare('12_PUBLIC_SITE/' + boundary['artifactRoute'], 'disclosure', 'WITHHOLDING_DESTINATION',
            WITHHELD, '/boundary/artifactRoute')

    # Literal line harvest only: no YAML execution, inferred D/L metadata or tier promotion.
    # All eligible Markdown remains queued, even when a declaration cannot be parsed.
    for row in rows:
        if not row['processing']['eligible']:
            continue
        if row['bytes'] > 1024 * 1024:
            issues.append({'kind': 'frontmatter_size_debt', 'path': row['path']})
            continue
        raw = read_blob(row['path'])
        try:
            text = raw[:65536].decode('utf-8', 'strict')
        except UnicodeDecodeError:
            issues.append({'kind': 'frontmatter_encoding_or_boundary_debt', 'path': row['path']})
            continue
        lines = text.splitlines(keepends=True)
        if not lines or lines[0].strip('\r\n') != '---':
            continue
        end = next((i for i, line in enumerate(lines[1:], 1) if line.strip('\r\n') == '---'), None)
        if end is None:
            issues.append({'kind': 'frontmatter_unclosed_or_bounded', 'path': row['path']})
            continue
        offset = len(lines[0].encode())
        for number, line in enumerate(lines[1:end], 2):
            match = re.match(r'^(status|lifecycle):[ \t]*(.+?)[\r\n]*$', line)
            if match:
                locator = f'bytes:{offset}:{offset + len(line.encode())};line:{number}'
                literal = match.group(2)
                raw_status.append({'path': row['path'], 'key': match.group(1), 'raw_value': literal,
                                   'oid': row['oid'], 'locator': locator})
                declare(row['path'], 'lifecycle', f'{match.group(1)}: {literal}', row['path'], locator)
            offset += len(line.encode())
    return ({'kind': 'apu.census_declarations', 'version': 1, 'commit': pin, 'entries': declarations},
            {'registries': registry_receipts, 'withheld_custody': custody,
             'literal_frontmatter': raw_status, 'issues': issues,
             'boundary': 'Attributed raw declarations only. Delivery enforcement and semantic adoption not tested.'})


def repository_pin(repo):
    return {'root': str(repo), 'commit': collection.git(repo, 'rev-parse', 'HEAD').decode().strip(),
            'branch': collection.git(repo, 'branch', '--show-current').decode().strip()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--revision', required=True)
    parser.add_argument('--parent', default='/Users/Yves/Library/Application Support/APU/collections/emergentism-atlas')
    args = parser.parse_args()
    os.umask(0o077)
    parent = collection.no_symlinks(args.parent)
    for repo in (SOURCE, APU, CORTEX):
        collection.require(not parent.is_relative_to(repo), 'private_run_inside_repository')
    parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    now = datetime.now(timezone.utc)
    run = parent / (now.strftime('%Y%m%dT%H%M%SZ') + '-' + uuid.uuid4().hex[:12])
    run.mkdir(mode=0o700)
    initial = census.census(SOURCE, args.revision)
    pin = initial['commit']
    pins = {name: repository_pin(repo) for name, repo in [('emergentism', SOURCE), ('apu', APU), ('cortex', CORTEX)]}
    pins['source_snapshot'] = pin
    pins['created_utc'] = now.isoformat()
    pins['runtime'] = {name: subprocess.check_output(command, stderr=subprocess.STDOUT).decode().strip()
                       for name, command in [('python', [sys.executable, '--version']), ('git', ['git', '--version']),
                                             ('node', ['node', '--version']),
                                             ('cortex_python', [str(CORTEX / '.venv/bin/python'), '--version'])]}
    tool_paths = [Path(__file__).resolve(), APU / 'apu.bot/scripts/corpus_census.py',
                  *[APU / 'apu.bot' / p for p in collection.ENGINE],
                  CORTEX / 'src/menexus_core/snapshot.py', CORTEX / 'src/menexus_core/contracts.py']
    pins['tool_sha256'] = {str(p): collection.sha(p.read_bytes()) for p in tool_paths}
    for tool in tool_paths:
        relative = tool.relative_to(DOCUMENTS)
        target = run / 'run-executable' / relative
        target.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        raw = tool.read_bytes()
        collection.require(collection.sha(raw) == pins['tool_sha256'][str(tool)], 'tool_changed_during_capture')
        with open(target, 'xb') as stream:
            stream.write(raw)
    pins['outside_snapshot'] = {name: census.worktree_observation(repo, pins[name]['commit'])
                                for name, repo in [('emergentism', SOURCE), ('apu', APU), ('cortex', CORTEX)]}
    collection.fresh_json(run / 'pins.json', pins)
    # Preserve the previous committed executable independently from future working changes.
    archive = collection.git(APU, 'archive', '--format=tar', pins['apu']['commit'],
                             *['apu.bot/' + p for p in collection.ENGINE])
    with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
        for member in tar.getmembers():
            if not member.isfile():
                continue
            collection.require(member.name in {'apu.bot/' + p for p in collection.ENGINE}, 'unexpected_engine_member')
            target = run / 'previous-engine' / member.name
            target.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
            with open(target, 'xb') as stream:
                stream.write(tar.extractfile(member).read())
    declarations, receipts = collect_declarations(SOURCE, pin, initial['artifacts'])
    collection.fresh_json(run / 'declarations.json', declarations)
    collection.fresh_json(run / 'classification-receipts.json', receipts)
    result = census.census(SOURCE, pin, declarations)
    repeat = census.census(SOURCE, pin, declarations)
    collection.require(collection.encoded(result) == collection.encoded(repeat), 'census_not_repeatable')
    totals = result['totals']
    collection.require(totals['tracked_entries'] == totals['eligible'] + sum(totals['excluded_by_reason'].values()),
                       'denominator_not_reconciled')
    collection.fresh_json(run / 'census.json', result)
    collection.fresh_json(run / 'census-repeat.json', repeat)
    queue = [{'path': r['path'], 'oid': r['oid'], 'lifecycle': r['lifecycle'],
              'disclosure': r['disclosure'], 'state': 'UNREAD',
              'queue_reason': 'READING_CANDIDATE_REQUIRING_MODULE_CLASSIFICATION; not an active-source assertion'}
             for r in result['artifacts'] if r['processing']['eligible']]
    collection.fresh_json(run / 'review-queue.json', {'kind': 'emergentism.atlas_review_queue', 'version': 1,
                          'commit': pin, 'entries': queue, 'reading_order': 'PLAN.md Sprint 3; not physical migration'})
    end_tools = {str(p): collection.sha(p.read_bytes()) for p in tool_paths}
    end_repos = {name: repository_pin(repo) for name, repo in [('emergentism', SOURCE), ('apu', APU), ('cortex', CORTEX)]}
    stable = end_tools == pins['tool_sha256'] and all(end_repos[name] == pins[name] for name in end_repos)
    collection.fresh_json(run / 'end-pins.json', {'tool_sha256': end_tools, 'repositories': end_repos, 'stable': stable})
    collection.require(stable, 'run_versions_changed_retain_outputs_but_do_not_accept_run')
    summary = {'run': str(run), 'source_snapshot': pin, 'totals': totals,
               'census_sha256': collection.sha(collection.encoded(result)),
               'repeat_identical': True, 'registry_issues': len(receipts['issues']),
               'withheld_custody_matches': sum(r['matches_declared_custody'] is True for r in receipts['withheld_custody']),
               'withheld_custody_unchecked': sum(r['matches_declared_custody'] is None for r in receipts['withheld_custody']),
               'lifecycle_states': dict(Counter(r['lifecycle']['state'] for r in result['artifacts'])),
               'disclosure_states': dict(Counter(r['disclosure']['state'] for r in result['artifacts'])),
               'review_queue': len(queue), 'fully_read_by_this_run': 0,
               'status': 'METADATA_CENSUS_COMPLETE_NOT_INDEXED_OR_REVIEWED'}
    collection.fresh_json(run / 'summary.json', summary)
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
