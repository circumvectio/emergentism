"""Offline checks for this design inventory, not an instrument evaluation."""
import argparse
import copy
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import unittest

HERE = Path(__file__).resolve().parent
FILES = {
    "README.md", "01_OUTLINE.md", "02_FILE_ARCHITECTURE.md",
    "03_RELEASE_SEQUENCE.md", "04_SOURCE_BINDINGS.json",
    "05_CUSTODY_AND_DELIVERY.md", "check_packet.py",
}
SECTIONS = {"start", "lens", "instrument", "cases", "research", "sources", "release"}
HEX = re.compile(r"[0-9a-f]{40}")
SECRET = re.compile(r"gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|sk-(?:proj-)?[A-Za-z0-9_-]{24,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def relative_path(value):
    require(isinstance(value, str) and value, "missing path")
    path = PurePosixPath(value)
    require(not path.is_absolute() and ".." not in path.parts, "unsafe path")
    require("\\" not in value and ":" not in value, "ambiguous path")


def validate_inventory(data):
    require(data["type"] == "edition-design-inventory", "wrong inventory type")
    require(data["status"] == "DESIGN_ONLY", "design state promoted")
    require(data["semantic_authority"] == "none", "semantic authority introduced")
    require(data["may_sign"] is False and data["may_authorize"] is False, "authority introduced")
    require(data["destination"] == {
        "repository": "Menexus-GmbH/emergentism", "visibility": "private",
        "branch": "theory/parasite-load-2026-08-17",
    }, "destination changed")
    require(set(data["packet_files"]) == FILES and len(data["packet_files"]) == len(FILES), "packet scope drift")
    require(set(data["reader_sections"]) == SECTIONS - {"release"}, "reader section drift")
    require(data["metadata_sections"] == ["release"], "release metadata missing")
    for field in ("delivered_source_revision", "local_planning_revision"):
        require(HEX.fullmatch(data[field]), "invalid revision")
    ids = set()
    covered = set()
    require(len(data["sources"]) == 14, "source inventory count drift")
    for item in data["sources"]:
        require(item["id"] not in ids, "duplicate source ID")
        ids.add(item["id"])
        relative_path(item["path"])
        require(set(item["sections"]) <= SECTIONS and item["sections"], "unknown section")
        covered.update(item["sections"])
        require(HEX.fullmatch(item["delivery_blob"]) and HEX.fullmatch(item["local_blob"]), "invalid source blob")
        require(item["local_differs"] is (item["delivery_blob"] != item["local_blob"]), "concealed source drift")
        expected = "https://github.com/Menexus-GmbH/emergentism/blob/" + data["delivered_source_revision"] + "/" + item["path"]
        require(item["url"] == expected, "unpinned source URL")
    require(covered == SECTIONS, "unbound section")


def validate_text(name, text):
    require(not SECRET.search(text), "credential-shaped content in " + name)
    require(not re.search(r"[/]Users[/][^/\s]+/", text), "workstation path in " + name)
    if name.endswith(".md"):
        for target in re.findall(r"\]\(([^)]+)\)", text):
            require(target in FILES, "unbound packet link in " + name)


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args], stderr=subprocess.PIPE).decode().strip()


def validate_bindings(data, lookup, include_local=True):
    for item in data["sources"]:
        require(lookup(data["delivered_source_revision"], item["path"]) == item["delivery_blob"], "pinned source mismatch")
        if include_local:
            require(lookup(data["local_planning_revision"], item["path"]) == item["local_blob"], "local planning source mismatch")


def check(tree=None, delivered_only=False):
    repo = Path(git(HERE, "rev-parse", "--show-toplevel"))
    prefix = HERE.relative_to(repo).as_posix() + "/"
    if tree:
        tree = git(repo, "rev-parse", "--verify", tree + "^{commit}")
        actual = set(git(repo, "ls-tree", "-r", "--name-only", tree, "--", prefix).splitlines())
        require(actual == {prefix + name for name in FILES}, "delivery file set drift")
        contents = {name: git(repo, "show", tree + ":" + prefix + name) for name in FILES}
    else:
        require({path.name for path in HERE.iterdir()} == FILES, "local file set drift")
        require(all(not (HERE / name).is_symlink() for name in FILES), "symlink refused")
        contents = {name: (HERE / name).read_text() for name in FILES}
    data = json.loads(contents["04_SOURCE_BINDINGS.json"])
    validate_inventory(data)
    for name, text in contents.items():
        validate_text(name, text)
    def lookup(revision, path):
        reference = revision + ":" + path
        require(git(repo, "cat-file", "-t", reference) == "blob", "source is not a blob")
        return git(repo, "rev-parse", reference)
    validate_bindings(data, lookup, include_local=not delivered_only)
    for item in data["sources"]:
        if tree:
            require(git(repo, "rev-parse", tree + ":" + item["path"]) == item["delivery_blob"], "delivery source drift")
    scope = "delivered pins only; local planning pins NOT VERIFIED" if delivered_only else "both delivered and local planning pins"
    print("PASS: 7 design files, 6 reader sections, 14 sources, " + scope + "; structure only, no efficacy or release claim.")


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((HERE / "04_SOURCE_BINDINGS.json").read_text())

    def rejects(self, mutate):
        changed = copy.deepcopy(self.data)
        mutate(changed)
        with self.assertRaises(ValueError):
            validate_inventory(changed)

    def test_valid(self):
        validate_inventory(self.data)

    def test_authority(self):
        self.rejects(lambda d: d.update(may_authorize=True))

    def test_destination(self):
        self.rejects(lambda d: d["destination"].update(visibility="public"))

    def test_duplicate(self):
        self.rejects(lambda d: d["sources"].append(d["sources"][0]))

    def test_path(self):
        self.rejects(lambda d: d["sources"][0].update(path="../private"))

    def test_drift(self):
        self.rejects(lambda d: d["sources"][5].update(local_differs=False))

    def test_source_url(self):
        self.rejects(lambda d: d["sources"][0].update(url="https://github.com/example"))

    def test_false_local_pin(self):
        original = {}
        for item in self.data["sources"]:
            original[(self.data["delivered_source_revision"], item["path"])] = item["delivery_blob"]
            original[(self.data["local_planning_revision"], item["path"])] = item["local_blob"]
        changed = copy.deepcopy(self.data)
        changed["sources"][0].update(local_blob="0" * 40, local_differs=True)
        validate_inventory(changed)
        with self.assertRaises(ValueError):
            validate_bindings(changed, lambda revision, path: original[(revision, path)])

    def test_bad_link(self):
        with self.assertRaises(ValueError):
            validate_text("README.md", "[absent](missing.md)")

    def test_credential(self):
        with self.assertRaises(ValueError):
            validate_text("README.md", "gh" + "p_" + "a" * 36)

    def test_workstation_path(self):
        with self.assertRaises(ValueError):
            validate_text("README.md", "/" + "Users/Example/private/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tree", help="Check the exact packet and source bindings in a delivery commit")
    parser.add_argument("--delivered-only", action="store_true", help="Explicit reduced scope when local-only history is unavailable; local planning pins are not verified")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        unittest.main(argv=[sys.argv[0]])
    else:
        try:
            check(args.tree, args.delivered_only)
        except (ValueError, KeyError, TypeError, OSError, subprocess.CalledProcessError) as error:
            print("FAIL: " + str(error), file=sys.stderr)
            sys.exit(1)
