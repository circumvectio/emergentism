"""Offline editorial checks; not runtime-packet validation or efficacy scoring."""
import argparse
import copy
import json
from pathlib import Path
import re
import subprocess
import unittest
from urllib.parse import unquote, urlsplit

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DESIGN = HERE.parent / "2026_09_10_MENEXUS_EDITION_DESIGN"
DESIGN_REVISION = "2ec3abb99d43fe9af44bc15a67f30b3267451696"
FILES = {
    "README.md", "01_EXECUTIVE_EXPLANATION.md", "02_ATLAS_D4_D5.md",
    "03_HUMAN_WALKTHROUGH.md", "04_MACHINE_REFERENCE.md", "SOURCES.md",
    "05_UI_DIRECTION.md", "check_slice.py",
}
HUMAN = "03_HUMAN_WALKTHROUGH.md"
MACHINE = "04_MACHINE_REFERENCE.md"
INTRO = "01_EXECUTIVE_EXPLANATION.md"
QUESTION = (
    "Our team agrees that launching next week is best. We have a working "
    "prototype, no independent user test, and capacity for one small trial. "
    "What do we know, what remains uncertain, and what should we do next?"
)
STATUS = (
    "TRIAL: NOT RUN\nOUTCOME: UNOBSERVED\nLAUNCH DECISION: UNDETERMINED\n"
    "AUTHORIZATION: NOT SUPPLIED\nRUNTIME PACKETS: NOT PRODUCED\n"
    "EXAMPLE: SYNTHETIC DEVELOPMENT; NOT HELD-OUT"
)
SHARED = ("facts", "unknowns", "options", "test", "recommendation", "updates", "status")
FIELDS = (
    "question-family", "operation", "sources", "uncertainty", "alternatives",
    "discriminator", "authority boundary", "outcome", "revision",
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def block(text, name):
    start = f"<!-- parity:{name}:start -->"
    end = f"<!-- parity:{name}:end -->"
    require(text.count(start) == text.count(end) == 1, "missing/duplicate block: " + name)
    left, right = text.index(start) + len(start), text.index(end)
    require(left < right, "reversed block: " + name)
    result = text[left:right].strip()
    require(result, "empty block: " + name)
    return result


def validate_docs(docs):
    require(set(docs) == FILES, "file set drift")
    for name in (INTRO, HUMAN, MACHINE):
        require(block(docs[name], "scenario") == QUESTION, "scenario changed: " + name)
    for name in SHARED:
        require(block(docs[HUMAN], name) == block(docs[MACHINE], name), "paired-view drift: " + name)
    for name in (HUMAN, MACHINE):
        require(block(docs[name], "status") == STATUS, "unobserved state promoted")
        facts = block(docs[name], "facts")
        require(re.findall(r"^- (F\d):", facts, re.M) == ["F1", "F2", "F3", "F4"], "fact IDs drift")
        require(re.findall(r"^- (A\d) —", block(docs[name], "options"), re.M) == ["A1", "A2", "A3"], "alternative IDs drift")
    fields = tuple(re.findall(r"^## (.+)$", docs[MACHINE], re.M))
    require(fields == FIELDS, "nine reference fields drift")
    require("not a validated runtime packet" in docs[MACHINE], "runtime boundary missing")
    for key in ("may_sign", "may_authorize"):
        require(re.findall(r"^" + key + r": (.+)$", docs[MACHINE], re.M) == ["false"], "authority promoted")
    require("## Plain decision journal — the simpler comparator" in docs[HUMAN], "comparator missing")
    require("## Exit" in docs["SOURCES.md"], "exit missing")
    require("Source drift stays visible" in docs["SOURCES.md"], "source-drift notice missing")


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args], stderr=subprocess.PIPE).decode().strip()


def read_docs():
    require({p.name for p in HERE.iterdir()} == FILES, "local file set drift")
    require(all((HERE / name).is_file() and not (HERE / name).is_symlink() for name in FILES), "non-file or symlink refused")
    return {name: (HERE / name).read_text(encoding="utf-8") for name in FILES}


def check_sources():
    inventory = DESIGN / "04_SOURCE_BINDINGS.json"
    prefix = DESIGN.relative_to(ROOT).as_posix()
    for name in ("04_SOURCE_BINDINGS.json", "01_OUTLINE.md"):
        require(git("hash-object", str(DESIGN / name)) == git("rev-parse", DESIGN_REVISION + ":" + prefix + "/" + name), "agreed design changed; review required")
    data = json.loads(inventory.read_text(encoding="utf-8"))
    succession = json.loads((HERE.parent / "2026_09_10_AI_RESEARCH_ENTRY" / "SOURCE_SUCCESSION.json").read_text())
    require(succession["type"] == "bounded-editorial-source-succession" and succession["authority_effect"] == "none", "source succession boundary changed")
    successors = {item["path"]: item for item in succession["sources"]}
    expected_successors = {
        "17_EMERGENTISM_2_MACHINE_INTELLIGENCE/10_KERNEL/LENS.v0.json",
        "17_EMERGENTISM_2_MACHINE_INTELLIGENCE/10_KERNEL/00_WHAT_THE_MACHINE_RECEIVES.md",
    }
    require(set(successors) == expected_successors and len(succession["sources"]) == 2, "succession scope changed")
    for item in data["sources"]:
        path = ROOT / item["path"]
        require(path.resolve().is_relative_to(ROOT) and path.is_file() and not path.is_symlink(), "source path refused")
        for revision, blob in ((data["delivered_source_revision"], item["delivery_blob"]), (data["local_planning_revision"], item["local_blob"])):
            require(git("rev-parse", revision + ":" + item["path"]) == blob, "source snapshot mismatch")
        expected = item["local_blob"]
        if item["path"] in successors:
            adopted = successors[item["path"]]
            require(adopted["predecessor_blob"] == expected, "succession predecessor mismatch")
            require(git("rev-parse", succession["predecessor_revision"] + ":" + item["path"]) == expected, "succession history mismatch")
            expected = adopted["successor_blob"]
        require(git("hash-object", str(path)) == expected, "live source changed; reopen review: " + item["id"])
    manifest = (ROOT / "17_EMERGENTISM_2_MACHINE_INTELLIGENCE/10_KERNEL/00_WHAT_THE_MACHINE_RECEIVES.md").read_text()
    section = manifest.split("## 5 ·", 1)[1].split("## 6 ·", 1)[0]
    source_fields = tuple(re.findall(r"^\| ([a-z][a-z -]+) \|", section, re.M))
    require(source_fields == FIELDS, "native reference field names changed")
    outline = (DESIGN / "01_OUTLINE.md").read_text()
    normalized_outline = " ".join(re.sub(r"(?m)^> ?", "", outline).split())
    require(QUESTION in normalized_outline, "scenario not in agreed outline")


def check_links(docs):
    count = 0
    for name, text in docs.items():
        if not name.endswith(".md"):
            continue
        for target in re.findall(r"\]\(([^)]+)\)", text):
            parsed = urlsplit(target)
            require(not parsed.scheme and not parsed.netloc, "unexpected network link")
            path = (HERE / unquote(parsed.path)).resolve()
            require(path.is_relative_to(ROOT) and path.is_file(), "broken/outside link: " + target)
            count += 1
    return count


class SliceTests(unittest.TestCase):
    def setUp(self):
        self.docs = read_docs()

    def rejects(self, edit):
        docs = copy.deepcopy(self.docs)
        edit(docs)
        with self.assertRaises(ValueError):
            validate_docs(docs)

    def test_valid(self):
        validate_docs(self.docs)

    def test_scenario_inflation(self):
        self.rejects(lambda d: d.update({MACHINE: d[MACHINE].replace("one small trial", "three trials")}))

    def test_lost_qualification(self):
        self.rejects(lambda d: d.update({MACHINE: d[MACHINE].replace("The agreement is stipulated", "The agreement is evidence")}))

    def test_duplicate_block(self):
        self.rejects(lambda d: d.update({HUMAN: d[HUMAN] + "\n<!-- parity:facts:start -->"}))

    def test_result_invented_in_both_views(self):
        def edit(d):
            for name in (HUMAN, MACHINE):
                d[name] = d[name].replace("OUTCOME: UNOBSERVED", "OUTCOME: SUCCESS")
        self.rejects(edit)

    def test_signing_authority(self):
        self.rejects(lambda d: d.update({MACHINE: d[MACHINE].replace("may_sign: false", "may_sign: true")}))

    def test_extra_runtime_field(self):
        self.rejects(lambda d: d.update({MACHINE: d[MACHINE] + "\n## approval\ntrue"}))

    def test_missing_comparator(self):
        self.rejects(lambda d: d.update({HUMAN: d[HUMAN].replace("## Plain decision journal — the simpler comparator", "## Conclusion")}))

    def test_broken_link(self):
        docs = copy.deepcopy(self.docs)
        docs[INTRO] += "\n[missing](not-present.md)"
        with self.assertRaises(ValueError):
            check_links(docs)

    def test_external_link(self):
        docs = copy.deepcopy(self.docs)
        docs[INTRO] += "\n[external](https://example.invalid)"
        with self.assertRaises(ValueError):
            check_links(docs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        unittest.main(argv=[__file__])
    else:
        docs = read_docs()
        validate_docs(docs)
        check_sources()
        links = check_links(docs)
        print(f"PASS: 8 local files; paired reference parity; 14 source pins and live files; {links} local links. Editorial checks only; no runtime, brand-conformance or efficacy qualification.")
