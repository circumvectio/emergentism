from __future__ import annotations

import copy
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_agentz_rosetta as validator


class AgentzRosettaContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.specs = [
            validator.load_yaml(path)
            for path in sorted(validator.CONFIG_DIR.glob("*.agent.yaml"))
        ]

    def test_live_configuration_passes(self) -> None:
        self.assertEqual([], validator.validate_paths())

    def test_wrong_rosetta_row_fails(self) -> None:
        specs = copy.deepcopy(self.specs)
        specs[0]["metadata"]["reasoning"] = "Deductive"
        self.assertTrue(any("reasoning must be" in e for e in validator.validate_specs(specs)))

    def test_swapped_operator_fails(self) -> None:
        specs = copy.deepcopy(self.specs)
        l1 = next(s for s in specs if s["metadata"]["level"] == "L1")
        l4 = next(s for s in specs if s["metadata"]["level"] == "L4")
        l1["metadata"]["operator"], l4["metadata"]["operator"] = (
            l4["metadata"]["operator"],
            l1["metadata"]["operator"],
        )
        self.assertTrue(any("operator must be" in e for e in validator.validate_specs(specs)))

    def test_wrong_balance_coordinate_fails(self) -> None:
        specs = copy.deepcopy(self.specs)
        specs[0]["metadata"]["balance_coordinate"] = "B=1"
        self.assertTrue(any("balance_coordinate must be" in e for e in validator.validate_specs(specs)))

    def test_missing_equation_domain_fails(self) -> None:
        specs = copy.deepcopy(self.specs)
        for spec in specs:
            spec["metadata"].pop("equation_domain", None)
        self.assertTrue(any("equation_domain" in e for e in validator.validate_specs(specs)))

    def test_executive_mutation_fails(self) -> None:
        specs = copy.deepcopy(self.specs)
        l6 = next(s for s in specs if s["metadata"]["level"] == "L6")
        l6["tools"][0]["configs"].append(
            {"name": "write", "enabled": True, "permission_policy": {"type": "always_ask"}}
        )
        self.assertTrue(any("L6: read-only profile" in e for e in validator.validate_specs(specs)))

    def test_l4_permission_bypass_fails(self) -> None:
        specs = copy.deepcopy(self.specs)
        l4 = next(s for s in specs if s["metadata"]["level"] == "L4")
        write = next(c for c in l4["tools"][0]["configs"] if c["name"] == "write")
        write.pop("permission_policy")
        self.assertTrue(any("L4: write must be always_ask" in e for e in validator.validate_specs(specs)))

    def test_moral_identity_fails(self) -> None:
        specs = copy.deepcopy(self.specs)
        specs[0]["metadata"]["operator"] = "Demon"
        self.assertTrue(any("identity leakage" in e for e in validator.validate_specs(specs)))

    def test_d4_d5_inversion_fails(self) -> None:
        specs = copy.deepcopy(self.specs)
        specs[1]["metadata"]["d4_d5_contract"] = "D5 invokes tools"
        self.assertTrue(any("D4-carrier/D5-content" in e for e in validator.validate_specs(specs)))

    def test_environment_networking_must_fail_closed(self) -> None:
        env = validator.load_yaml(validator.ENV_PATH)
        env["config"]["networking"]["type"] = "unrestricted"
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "environment.yaml"
            path.write_text(yaml.safe_dump(env, sort_keys=False), encoding="utf-8")
            errors = validator.validate_paths(validator.CONFIG_DIR, path)
        self.assertTrue(any("networking must be limited" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
