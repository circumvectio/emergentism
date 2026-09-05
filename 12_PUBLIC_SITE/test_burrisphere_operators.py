"""Deterministic source/HTML/record boundaries, independent of live services."""
import copy
import json
import shutil
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path
from unittest.mock import patch

import build_burrisphere_operators as builder


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids, self.local_links, self.record_ids = [], [], []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs: self.ids.append(attrs['id'])
        if attrs.get('href', '').startswith('#'): self.local_links.append(attrs['href'][1:])
        if 'data-operator' in attrs: self.record_ids.append(attrs['data-operator'])


class OperatorTests(unittest.TestCase):
    def test_frozen_records_and_markup_are_current(self):
        builder.build(check=True)

    def test_every_record_is_typed_intention_with_missing_instance_context(self):
        data = builder.catalogue()
        self.assertEqual(len(data['operators']), 7)
        self.assertEqual(len({r['id'] for r in data['operators']}), 7)
        for r in data['operators']:
            self.assertEqual(r['status'], 'INTENDED_NOT_OBSERVED')
            self.assertIsNone(r['units'])
            self.assertIsNone(r['outcomeEvidence'])
            self.assertFalse(r['gen7Projection']['identity'])
            self.assertIsNone(r['gen7Projection']['chartSample'])
            self.assertTrue(r['missingContext'])
        preserve = data['operators'][-1]
        self.assertIn('hold comparison or defended tolerance', preserve['missingContext'])
        self.assertNotIn('maximize', preserve['id'])

    def test_ids_and_local_anchor_references(self):
        text = (builder.SITE/builder.PAGE).read_text()
        page = Page(text)
        self.assertEqual(len(page.ids), len(set(page.ids)))
        self.assertEqual(len(page.record_ids), 7)
        self.assertFalse(set(page.local_links)-set(page.ids))

    def test_repeated_clean_generation_is_identical(self):
        with tempfile.TemporaryDirectory() as directory:
            site = Path(directory)
            (site/builder.PAGE).parent.mkdir(parents=True)
            shutil.copyfile(builder.SITE/builder.PAGE, site/builder.PAGE)
            builder.build(site=site)
            first = {p:(site/p).read_bytes() for p in (builder.PAGE,builder.DATA,builder.SCHEMA)}
            builder.build(site=site)
            builder.build(check=True, site=site)
            self.assertEqual(first, {p:(site/p).read_bytes() for p in first})
            (site/builder.DATA).write_text('{}')
            with self.assertRaisesRegex(ValueError, 'Generated inspector drift'):
                builder.build(check=True, site=site)

    def test_source_drift_refused_not_rehashed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for p in builder.PINS:
                (root/p).parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(builder.ROOT/p, root/p)
            (root/builder.G7).write_text((root/builder.G7).read_text()+'\nchanged\n')
            with self.assertRaisesRegex(ValueError, 'Source drift'):
                builder.catalogue(root)

    def test_deleted_signature_or_invented_id_refused(self):
        rows = copy.deepcopy(builder.RECORDS)
        row = list(rows[0])
        row[0] = 'invented_maximize_everything'
        rows[0] = tuple(row)
        with patch.object(builder, 'RECORDS', rows):
            with self.assertRaisesRegex(ValueError, 'Missing source signature or ID'):
                builder.catalogue()

    def test_generated_html_cannot_escape_source_text(self):
        data = builder.catalogue()
        data['operators'][0]['explanation'] = '<script>alert(1)</script>'
        self.assertNotIn('<script>', builder.render(data))
        self.assertIn('&lt;script&gt;', builder.render(data))

    def test_swapped_valid_ids_and_inverted_directions_are_rejected(self):
        rows = copy.deepcopy(builder.RECORDS)
        first, second = list(rows[0]), list(rows[1])
        first[0], second[0] = second[0], first[0]
        rows[0], rows[1] = tuple(first), tuple(second)
        with patch.object(builder, 'RECORDS', rows):
            with self.assertRaisesRegex(ValueError, 'Source row binding mismatch'): builder.catalogue()
        rows = copy.deepcopy(builder.RECORDS)
        rows[0][-1][0][-1] = 'decrease'
        with patch.object(builder, 'RECORDS', rows):
            with self.assertRaisesRegex(ValueError, 'Source clause binding mismatch'): builder.catalogue()

    def test_editorial_reordering_cannot_reassign_gen7_seats(self):
        expected = {r['id']:r['gen7Projection'] for r in builder.catalogue()['operators']}
        with patch.object(builder, 'RECORDS', list(reversed(builder.RECORDS))):
            self.assertEqual(expected, {r['id']:r['gen7Projection'] for r in builder.catalogue()['operators']})

    def test_schema_names_every_top_level_field_and_types_seats(self):
        schema = builder.schema_document()
        self.assertEqual(set(schema['required']),set(schema['properties']))
        self.assertFalse(schema['additionalProperties'])
        seat = schema['$defs']['operator']['properties']['gen7Projection']['properties']['seat']
        self.assertEqual(seat['type'],'string')


if __name__ == '__main__': unittest.main()
