#!/usr/bin/env python3
"""Run backbone tests. 00_BACKBONE/ goes on sys.path so 'from schemas.X' works."""

import sys, os, importlib.util

_script_dir = os.path.dirname(os.path.abspath(__file__))  # EMERGENTISM_ORG/09_TOOLS/01_SCRIPTS/
_repo_root = os.path.dirname(os.path.dirname(_script_dir))  # repo root (two levels up)
_bb = os.path.join(_repo_root, "02_ORGANISM", "00_BACKBONE")
if _bb not in sys.path:
    sys.path.insert(0, _bb)

errors, passed, failed = [], 0, 0

tests = [
    (
        "test_packet_schemas",
        [
            "test_signal_packet_roundtrip",
            "test_probability_packet_roundtrip",
            "test_action_packet_roundtrip",
            "test_receipt_packet_roundtrip",
            "test_context_packet_roundtrip",
        ],
    ),
    (
        "test_lineage_flow",
        [
            "test_lineage_root_and_child_flow",
        ],
    ),
    (
        "test_refusal_propagation",
        [
            "test_hold_blocks_envelope",
            "test_escalate_blocks_auto_execution",
            "test_reject_blocks_auto_execution",
            "test_execute_allows_envelope",
            "test_trace_closes_on_refusal_without_receipt",
        ],
    ),
    (
        "test_trace_closure",
        [
            "test_execute_path_closes_with_receipt",
            "test_hold_path_closes_without_receipt",
            "test_orphan_packet_detection",
        ],
    ),
    (
        "test_end_to_end_cycle",
        [
            "test_end_to_end_cycle_execute",
        ],
    ),
    (
        "test_backbone_demo_flow",
        [
            "test_full_trivium_loop_execute_path",
            "test_full_trivium_loop_hold_path",
            "test_witness_propagation_across_loop",
        ],
    ),
]

for mod_name, fns in tests:
    fp = os.path.join(_bb, "tests", f"{mod_name}.py")
    if not os.path.exists(fp):
        print(f"  SKIP {mod_name} (file missing)")
        continue
    spec = importlib.util.spec_from_file_location(f"_bbt_{mod_name}", fp)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    for fn in fns:
        f = getattr(mod, fn, None)
        if not f:
            print(f"  SKIP {mod_name}::{fn}")
            continue
        try:
            f()
            print(f"  PASS {mod_name}::{fn}")
            passed += 1
        except Exception as e:
            print(f"  FAIL {mod_name}::{fn}: {e}")
            errors.append((mod_name, fn, str(e)))
            failed += 1

print(f"\n{'=' * 60}")
print(f"Results: {passed} passed, {failed} failed, {passed + failed} total")
if errors:
    for m, f, e in errors:
        print(f"  FAIL {m}::{f}: {e}")
    sys.exit(1)
else:
    print("ALL TESTS PASSED")
