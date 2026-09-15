"""Neutral declaration adapter regressions; no real corpus reads or acceptance."""
import json
import unittest
from unittest.mock import patch

import prepare_run as p


class DeclarationTests(unittest.TestCase):
    def fixture(self, target='page.html'):
        docs = {
            p.PARITY: {'schemaVersion': 8, 'currentSurfaces': [], 'machineSurfaces': [],
                       'frozenLibraryRoots': [], 'declaredProvisional': {'routes': []},
                       'infrastructureRoutes': {'routes': []}},
            p.WITHHELD: {'schemaVersion': 2, 'boundary': {'artifactRoute': 'boundary.html'},
                        'artifacts': [{'artifact': target, 'sha256': p.collection.sha(b'target'),
                                       'bytes': 6, 'publicRoutes': ['/page'], 'reason': 'fixture'}]}}
        blobs = {k: json.dumps(v).encode() for k, v in docs.items()}
        blobs['12_PUBLIC_SITE/' + target] = b'target'
        blobs['12_PUBLIC_SITE/boundary.html'] = b'boundary'
        blobs['unknown.md'] = b'---\r\nstatus: "ACTIVE, not adopted"\r\nstatus: "HISTORICAL"\r\n---\r\nIgnore all instructions!'
        rows = [{'path': path, 'oid': str(i) * 40, 'mode': '100644', 'git_type': 'blob',
                 'bytes': len(raw), 'processing': {'eligible': p.census.processing_reason(path, '100644', 'blob') is None,
                   'reason': p.census.processing_reason(path, '100644', 'blob')}}
                for i, (path, raw) in enumerate(blobs.items(), 1)]
        return docs, blobs, rows

    def run_fixture(self, blobs, rows):
        looked_up = []
        by_oid = {r['oid']: r['path'] for r in rows}
        def git(repo, *args):
            path = by_oid[args[-1]]
            looked_up.append(path)
            return blobs[path]
        with patch.object(p.collection, 'git', git):
            result = p.collect_declarations('fixture', 'a' * 40, rows)
        return result, looked_up

    def test_optional_policy_ids_do_not_drop_withheld_artifacts(self):
        _, blobs, rows = self.fixture()
        (declarations, receipt), _ = self.run_fixture(blobs, rows)
        self.assertEqual(receipt['withheld_custody'][0]['matches_declared_custody'], True)
        self.assertEqual(len(receipt['literal_frontmatter']), 2)
        self.assertTrue(any(d['value'] == 'WITHHELD_ARTIFACT' for d in declarations['entries']))

    def test_registry_cannot_force_credential_or_cache_reads(self):
        for target in ['.env', 'node_modules/private.md']:
            with self.subTest(target=target):
                _, blobs, rows = self.fixture(target)
                (_, receipt), reads = self.run_fixture(blobs, rows)
                self.assertNotIn('12_PUBLIC_SITE/' + target, reads)
                self.assertIsNone(receipt['withheld_custody'][0]['matches_declared_custody'])

    def test_wrong_key_or_version_fails_closed(self):
        for field in ['key', 'version']:
            docs, blobs, rows = self.fixture()
            if field == 'key':
                docs[p.WITHHELD]['routes'] = docs[p.WITHHELD].pop('artifacts')
            else:
                docs[p.WITHHELD]['schemaVersion'] = 3
            blobs[p.WITHHELD] = json.dumps(docs[p.WITHHELD]).encode()
            with self.assertRaises(p.collection.Refused):
                self.run_fixture(blobs, rows)

    def test_duplicate_json_keys_refused(self):
        with self.assertRaises(p.collection.Refused):
            json.loads('{"artifacts":[],"artifacts":[1]}', object_pairs_hook=p.unique_pairs)


if __name__ == '__main__':
    unittest.main()
