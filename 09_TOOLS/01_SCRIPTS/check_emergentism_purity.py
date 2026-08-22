#!/usr/bin/env python3
"""Fail closed when application-era authority leaks into active Emergentism.

The scan is intentionally scoped to source owners, front doors, route cards,
and active tooling. Archives, compatibility stubs, public projection, session
packets, handoffs, and dated receipts are provenance rather than authority.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[2]

ROUTE_EXCLUDED_PARTS = {
    "90_ARCHIVE",
    "91_COMPATIBILITY",
    "12_PUBLIC_SITE",
    "00_HANDOFF",
    "50_AUDITS_AND_EXECUTIONS",
}

CORPUS_EXCLUDED_PARTS = ROUTE_EXCLUDED_PARTS | {
    "91_COMPATIBILITY",
    "60_SESSION_PACKETS",
}

ACTIVE_TOP_LEVELS = {
    # 2026-08-01: 00_ESTABLISHED, 00_WORK_IN_PROGRESS and 13_BOOKS were ACTIVE lanes sitting
    # outside this checker's scope. 00_ESTABLISHED is the corpus's short list of what
    # survives an outside check — arguably the document that most needs the gate — and it
    # was carrying both a literal product form and a bare eta, invisible to every checker.
    # 00_HANDOFF stays excluded: it is dated provenance, like the receipt lanes.
    "00_CONTROL",
    "00_ESTABLISHED",
    "00_WORK_IN_PROGRESS",
    "13_BOOKS",
    "14_THE_DISTILLATION",
    "00_META",
    "01_TELEOLOGY",
    "02_EPISTEMOLOGY",
    "03_METHODOLOGY",
    "04_AXIOLOGY",
    "05_COSMOLOGY",
    "06_ONTOLOGY",
    "07_THEOLOGY",
    "08_FRAMEWORK_SUPPORT",
    "09_TOOLS",
    "10_SEED",
    "11_UPLINK",
}

TEXT_SUFFIXES = {".md", ".py", ".r", ".json", ".yaml", ".yml", ".toml"}

RECEIPT_CITATION_LANES = (
    Path("11_UPLINK/50_AUDITS_AND_EXECUTIONS"),
    Path("11_UPLINK/60_SESSION_PACKETS"),
)
RECEIPT_TARGET_REGISTRY = Path("00_META/ACTIVE_RECEIPT_CITATION_REGISTRY.json")
EXPECTED_RECEIPT_TARGET_UNIVERSE_SHA256 = (
    "25661f69c75f93ee977969bb2fcc6a1158698013c5517000ef3868b9d088bd5a"  # pragma: allow-secret
)
EXPECTED_RECEIPT_TARGET_COUNT = 321

# Derived custody surfaces repeat source semantic units and exact historical
# filenames by design. Their dedicated checker and digest receipt own that
# copied content; scanning the copy as fresh doctrine would both double count
# and misread identity strings as authority assertions.
DERIVED_CUSTODY_SURFACES = {
    Path("00_META/ACTIVE_RECEIPT_CITATION_REGISTRY.json"),
    # Machine snapshot of separately validated receipt, claim-lifecycle, public
    # delivery, and topology state.  It necessarily records exact historical
    # artifact names (including retired application-era tokens); the dedicated
    # contact-limited checker owns its schema, hashes, and dated receipt bind.
    Path("00_META/CONTACT_LIMITED_STATE.json"),
}

# Frozen tooling/history is admitted only at these exact bytes.  This replaces
# the former whole-file vocabulary bypass: any mutation, including a new
# authority assertion, loses the digest contract and fails closed.
FROZEN_TOOLING_SHA256 = {
    Path("03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SCHEMA.json"): "f8c4205af97635f8eea9f83cbf3a1e05ff50a0f64bc6ee8dd54ff61f6df78a3f",
    Path("09_TOOLS/01_SCRIPTS/check_contradiction_census.py"): "cc1d16ecdfc1e1b7835bdf3572e0cf0fece7d5bae7e1e59d6c4863d90e8898a4",
    Path("09_TOOLS/01_SCRIPTS/check_established.py"): "0b1f50f8e9269e6da87bda7e6a72792cc5c87adf0419ffdcd3a4fec6588d6b5b",
    Path("09_TOOLS/01_SCRIPTS/check_ruling_landed.py"): "565cfed0c21cb15e3196d2d0b6773a37aef289b564680869071fa5674c9ea524",
    Path("09_TOOLS/01_SCRIPTS/check_tree_contract.py"): "cc11cd929c3e7fa73686c24f5f7f1e96e0437af55e6377a09b55ba7fa36c5336",
    Path("09_TOOLS/01_SCRIPTS/lint_rule_tokens.py"): "8388862c3d43d928f7fcdeb15c5c8c4859871f70e3880d35e03720ed00920dcc",
    Path("09_TOOLS/02_COMPILERS/kintsugi_baseline_failures.json"): "74496df660f0ca989f293c30db652b8f9aeb78beb30fa91fe249d87ee29ef69b",
    Path("09_TOOLS/02_COMPILERS/kintsugi_kernel/semantics.py"): "97fd9953721fd89532bb5c05b9c26ca235cd1a75a0f0cc7fe0dff3385567ebc6",
    Path("09_TOOLS/02_COMPILERS/kintsugi_kernel/docs/plans/2026-07-12-kintsugi-a0-foundations-implementation.md"): "f29cf940e5f9596367f30bb99b79d25983b4d0d43453842247da0d7c9ee18a8c",
    Path("09_TOOLS/02_COMPILERS/kintsugi_kernel/docs/plans/2026-07-12-kintsugi-a0b-machine-kernel-implementation.md"): "6ab7af84682ba22dd3a5464385e563af726c7b604dd9cbb3f75a236890e73ae9",
    Path("09_TOOLS/02_COMPILERS/kintsugi_kernel/docs/specs/2026-07-11-kintsugi-formal-logic-design.md"): "c4491a3fd3ffdbc7685049ee50f61b35d07e640061ee62c969a814757f02cd6d",
    Path("09_TOOLS/02_COMPILERS/kintsugi_kernel/docs/specs/2026-07-12-kintsugi-a0-concurrency-addendum-992a838.md"): "50a2633d7df9dfdf1b8ce3bec4e1ee64fedc7dca4a3c0a4e02892703736741f3",
    Path("09_TOOLS/02_COMPILERS/kintsugi_kernel/docs/specs/2026-07-12-kintsugi-a0-execution-lock-26e616e.md"): "d6e7097facab94fb88ed79166fbd7cda9185740830087f69309d748eff61d2fd",
    Path("09_TOOLS/02_COMPILERS/kintsugi_kernel/docs/specs/2026-07-12-kintsugi-a0b-machine-kernel-addendum.md"): "27ccf6aaf74836019ff33517c243c35f0ce820420d5daa1c4311d7b15e354e2d",
    Path("09_TOOLS/02_COMPILERS/test_emergentist_compass_semantics.py"): "5ce532bee2673f25b8b6fc452bf43f3659a9581af55dbf8c45ca5ebe1be1d805",
    Path("09_TOOLS/02_COMPILERS/test_kintsugi_mutations.py"): "dc7ecc04292b8a0d3657aa0667a10ca81639cf51999924beb6b4cd539aa5a1a9",
    Path("09_TOOLS/02_COMPILERS/test_kintsugi_schema.py"): "82703f06a9fb25ac808b15b3c45286a62c6cfcd9918bd842979eac46a391b5df",  # pragma: allow-secret -- SHA-256 custody pin
    Path("09_TOOLS/02_COMPILERS/test_kintsugi_semantics.py"): "e134e8639625831b951e07d556ce21f10cc5dfebbfdea93ed30025d68250e09c",
    Path("09_TOOLS/02_COMPILERS/test_validate_kintsugi.py"): "9ca7f87ba8f37f7648bea7ac961e0cea1dcc85441ad4fde16a7ef457c296738a",
    Path("09_TOOLS/02_COMPILERS/test_corpus_claim_graph.py"): "c80113a98ecb87e244de0cb169eefa59b6fb2e0110c7a0152241d61e8f78962e",
    Path("09_TOOLS/02_COMPILERS/test_dimension_first_canon.py"): "796af0e9eb360e000a4734d35e3cbfe841b07bea8efc1b62671be86e260e275c",
}

# Frozen forwarding/history files retain external names only as exact reviewed
# provenance. They are active-lane artifacts, so their custody is explicit
# rather than inherited from a broad provenance exception.
FROZEN_PROVENANCE_SHA256 = {
    Path("08_FRAMEWORK_SUPPORT/05_SYNTHESIS/07_DEFINITIVE_ONE_BOOK_MOVED.md"): "1d827c5652481d8af9db1d94823c7a7812439a35c6937652a4269ac02efddf05",
    Path("08_FRAMEWORK_SUPPORT/03_EVIDENCE/COMPARATIVE/2026_06_05_FILENAME_REPAIR_RECEIPT.md"): "170481275a66ee643910307063746bb71a8dfa6f7a2178d480c600763409def1",
}

# These exact, reviewed projection/history artifacts live in lanes deliberately
# excluded from ordinary doctrine scanning.  They do not inherit a lane-wide
# bypass: each file must remain a lexical regular file at the reviewed bytes.
# This binds the public reader correction, its receipt, and the archive record
# reached by the two active source-owner links below.
REVIEWED_PROJECTION_HISTORY_SHA256 = {
    Path("11_UPLINK/50_AUDITS_AND_EXECUTIONS")
    / (
        "243_PUBLIC_RELEASE_PREFLIGHT_AND_CONTACT_"
        + "SNAPSHOT_2026_08_09.md"
    ): "2196c5b7e782606f034dabf41201669a1e3596c42b7c37b73d44145e88121da8",
    Path("12_PUBLIC_SITE/00_THE_RUNGS_2026_08_05.md"): "d072044eeaa001421f47a57017a2b71fa712870f2f68e7ab38e235496b01a18d",
    Path("90_ARCHIVE/50_AUDITS/README.md"): "68de4387e1e5f4b3c09acf4f2792f0c4eeede4e92376aee1377785a351f66e80",
    Path("90_ARCHIVE/50_AUDITS/57_TITAN_CHART_TYPE_CORRECTION_TOMBSTONE_2026_08_09.md"): "4aaa3fdd0d82266710292dcc320293459a5cfafb2d902988d8a5ff537627b3d8",
}

# This checker cannot bind its own complete digest without recursion. Instead,
# every vocabulary-sensitive line is reviewed and hash-bound; ordinary code
# changes remain possible while any new or changed sensitive unit fails closed.
SELF_VALIDATED_TOOLING_PATH = Path(
    "09_TOOLS/01_SCRIPTS/check_emergentism_purity.py"
)
SELF_CHECKER_UNIT_SHA256: tuple[str, ...] = (
    "0d105c0dc7d3059e54277e1ba5fcd460efe338555fd139eede870cb805ebb5df",
    "1597a2cdc72abb2bdf8ce77cfb226d4f5d2e7c5b6dc97e9263e96e1b2d8ee334",
    "1957cd1741a9f21b16f4a0065091a2480041f7ef8502b417fba6c4f567fe4c40",
    "1957cd1741a9f21b16f4a0065091a2480041f7ef8502b417fba6c4f567fe4c40",
    "1957cd1741a9f21b16f4a0065091a2480041f7ef8502b417fba6c4f567fe4c40",
    "1ebfe1ed60597b3bef9e5fc811562da43a4f0fa6d1826e6f286f63baa02e0cc1",
    "2678a01146d33ecf7bd3e031c302dd15bdf08a74f4f5fd7512cc6b84d7ccb031",
    "286fecae785aba41b07e66f34a4a92b885c4bc5b7fc8555f0c9666bdc221d314",
    "2c48f403f4687c0af8de08b5b27c63b1d80b518da4691d68e72e7a8b7d55dcfd",
    "34ef9859a341dca102e9919e9d3ed18d635339587b2dd4b315a2d96699a11075",
    "3820c4322e3ea08f4555ab715f3587b9e7e35736b182d6ec4f31afe40877579e",
    "39a43501905dae6b24c3ab39df8add0055ca95c3d0d1ef020736e8065c9b13a9",
    "48f74388444c078f68d21c22c7272411995c38cf97a0c4b1544062fc57a2c6c9",
    "4966c5097d67dbb336161be6b138985dd43b360a74d75a5a31057378e551e47a",
    "4e7e3c3f38634ce26d3787a0cbd695bab3f9879a33f9c384807969dca4bd5e58",
    "4b713dc0bed82f5c7995b5825fd99e5e9519d02006792ab108919ea140eeb2ac",
    "508eb489853dec4a4ccf4dea8e96b75b6e5e284682778c2f18ace69014e78b64",
    "5662f872bb1f6bbd0cacbe9e30319db41f174b9a08fa6200303e933cde6b0b4b",
    "60b8ff253e55f2244dc0ebcdc2f8677a53ce0c755135d6b8a63dc9ae9b616c5b",
    "69c1290e4b4cfd92597bf3a86fc66fb4933d25bb0bcfbde9a07286eebbb46e69",
    "67803971544f63c65da98700769d36335d564876f3f89f0eccccad50be7a3e88",
    "27132b35ab5f2979de2952eb6ea6ac103edea4c64d46cf17bfae57fa24e02a1a",
    "6d7803eb9c0b330f830e3bbe7037eabe25bab41b391fe68e5bd1aee81292b2b4",
    "6dea045c940012e4afbe70b3391c3f6c6a4b51958829a6c7a8c9f7085497e354",
    "6dea045c940012e4afbe70b3391c3f6c6a4b51958829a6c7a8c9f7085497e354",
    "75946ea116c3c927f6506c4212135a0464805c05e2c85cdf28b406e8f464a6ad",
    "c1e0b47ef0a4fa7147a1640f7a90f43940be68069c2d3547d1a8afa2d17a86e9",
    "79ac35b2b4fe586a408e675cc3c319624ca086c064b8433480b166b876eaa3ea",
    "8debd3d575b9949c45b31be6ac4857b901a485cfabf40115466bfd3ebc7fe37a",
    "c258eb20309df4550b9beeba3468d5a931122f82b161615d0436bbb8550f90f9",
    "935798a5964cf82e85ed142bf2d15a7c70bb64565b5bac55ce77f03f528cfbd3",
    "935798a5964cf82e85ed142bf2d15a7c70bb64565b5bac55ce77f03f528cfbd3",
    "98f8ef18499cfa1eb60a9677a6c8b4e5fcabcc4d6e78510b718388d3e598302a",
    "990e4ece0ccf9cdba42ae711dad04b4a88effe737082cbc5b5337f5bfc0e74dd",
    "a3d9c7f05521db35526c160edc327c71119f17937fda0d01e2c33531c76bd7c4",
    "b3b44f2ff0c2709781b4c4dffa76ee92021486b6f873c63dcac0782d753df53f",
    "b3b44f2ff0c2709781b4c4dffa76ee92021486b6f873c63dcac0782d753df53f",
    "b998c4eef8f1d95f77fd8d366622e675254ee85db766e10a9269861f95e9b3b2",
    "cfc6c61ca8c34a2ea43c4aa63024590998bf3dfbf105c14bde9b8b0e1206372d",
    "d006e73bd28c0f879667222f69361c0f03b62d084aef1cb3ef9fd47b99e0f99d",
    "d58244993cc2051fb9d4096f4e4cf7d172b6d4532985f7fb08090aa3bb688aa9",
    "e9d54950b99340dccc4e3a5d8a41f2ceae4f3411d50dbd5d758671cec7f97387",
    "e4b3f8ac66e884dc5bf70cef426deceef786c31a2878969205b687bf568e5805",
)

# The former gate-health diagnostic was intentionally reverted in 00e68c83.
# Keep the structured-diagnostic hook empty so a future, separately reviewed
# diagnostic can opt into field-level scanning without making a deleted
# artifact mandatory.
STRUCTURED_DIAGNOSTIC_PATHS: frozenset[Path] = frozenset()

# Generated projections are parsed/line-typed below.  Only external source
# locator fields may carry application-era names; every other field and line is
# scanned as active text.
DERIVED_BOOK_PROJECTION_PATHS = {
    Path("13_BOOKS/manifesto/MANIFESTO_BOOK_1.md"),
    Path("13_BOOKS/manifesto/MANIFESTO_BOOK_1_BUILD.json"),
    Path("13_BOOKS/manifesto/MANIFESTO_BOOK_1_PARAGRAPH_LEDGER.json"),
}

# The generated Rosetta agent bundle used to be hidden behind a directory-wide
# exception.  Every currently reviewed source is now named and byte-bound.  A
# changed file must be re-reviewed, while a new sibling falls through to the
# ordinary active-corpus scan (and the inventory check below rejects even a
# non-text sibling that the generic scanner cannot classify).
MANAGED_AGENT_PROJECTION_ROOT = Path(
    "08_FRAMEWORK_SUPPORT/08_AGENTS/MANAGED_AGENTS"
)
MANAGED_AGENT_PROJECTION_SHA256 = {
    MANAGED_AGENT_PROJECTION_ROOT / "AGENTS.md": "b73c0bb4745f1456b0f8d3e213fd89346b99a8b844db84196bd384bf7aacc555",
    MANAGED_AGENT_PROJECTION_ROOT / "CLAUDE.md": "9ddfb4dfe38c852b065baa1ce8bc2442de9c748738392f2867601e35811f088d",
    MANAGED_AGENT_PROJECTION_ROOT / "QUALITY_QUANTITY_BALANCE_LAW_2026_07_22.md": "dd601c207d4240126c8d76e6588fe1af01d72bccc0b2f09a2740fdc01f561670",
    MANAGED_AGENT_PROJECTION_ROOT / "README.md": "3d9815ce7b1d8dd550a9461c6872e1cd9a2368350e30929675ef8c9ff707f1c1",
    MANAGED_AGENT_PROJECTION_ROOT / "ROSETTA_AGENT_PROJECTION_CONTRACT.md": "d8efba4f6f1d1b1f053ab9f905553072a3623d66d0e7b01701059b4c74f8c03a",
    MANAGED_AGENT_PROJECTION_ROOT / "agents/01_candala_firewall.agent.yaml": "4bd5080b3a5c37195430880072b8e9e1944919ffce8b05a6e26a974705612a04",
    MANAGED_AGENT_PROJECTION_ROOT / "agents/02_sudra_explorer.agent.yaml": "2aa19190f285d699d7a953b1b562c0be6ebc1d959b1f000161ad2c91d3953cca",
    MANAGED_AGENT_PROJECTION_ROOT / "agents/03_vaisya_auditor.agent.yaml": "1c3fc24cf457ba147b892ba8a0cd352fa5cbeb2c634ac7dc5b5717c73b7aacff",
    MANAGED_AGENT_PROJECTION_ROOT / "agents/04_ksatriya_executor.agent.yaml": "3dc42c105348ae05d73fb765108ca5368cf6574513beffc2af08e7c016e7650b",
    MANAGED_AGENT_PROJECTION_ROOT / "agents/05_brahmana_architect.agent.yaml": "245b070e81e59377c084bcbf698986dbec02e0c1a3ac0793c7f73889fd495763",
    MANAGED_AGENT_PROJECTION_ROOT / "agents/06_sadhu_compressor.agent.yaml": "5603cfbae641a2658a075d798e59cc221894991fb5b745b0a9cbb45bce4a9e8c",
    MANAGED_AGENT_PROJECTION_ROOT / "agents/07_rsi_constitution.agent.yaml": "053ee865d3df8f70b8d05ccd678e2cf28bca118fcd3bf230dea334c4c52ae490",
    MANAGED_AGENT_PROJECTION_ROOT / "agents/MANIFEST.sha256": "673cc62825c0a7257cd1552388b3dd4cff43fd480caf56bec7d056339495d028",
    MANAGED_AGENT_PROJECTION_ROOT / "check_agent_source_hashes.py": "b4d024bfb3e421aa4cd5a0591c4ce02b53703d03e74f1d8b002159872174af18",
    MANAGED_AGENT_PROJECTION_ROOT / "emergentism.environment.yaml": "9c68bf66bfaf7a86466efc5990e8120c03c1a74177585b1dc66a1081a9640c81",
    MANAGED_AGENT_PROJECTION_ROOT / "provision.py": "a2a40162849d927b19c053213d2047211b9797858238b50e980343748b4b53b4",
    MANAGED_AGENT_PROJECTION_ROOT / "provision.sh": "3ab5bc2ac3886873ac2bf9710885b0b37bed50ae117577273efd4657d8245023",
    MANAGED_AGENT_PROJECTION_ROOT / "run_session.py": "b18870fa34fade54cc6530fd5aa762ab2430960f2a6a0ed9c1ca70fcb1cf7cf5",
}
MANAGED_AGENT_PROJECTION_DIRECTORIES = frozenset({
    MANAGED_AGENT_PROJECTION_ROOT / "agents",
})
MANAGED_AGENT_PROJECTION_ENTRIES = (
    set(MANAGED_AGENT_PROJECTION_SHA256)
    | set(MANAGED_AGENT_PROJECTION_DIRECTORIES)
)

# The distillation is an active, projection-only reader surface with extensive
# historical quotations.  Its complete current shape and exact reviewed bytes
# are bound here; no future sibling or changed authority-bearing unit inherits
# projection status automatically.
DISTILLATION_PROJECTION_ROOT = Path("14_THE_DISTILLATION")
DISTILLATION_PROJECTION_SHA256 = {
    DISTILLATION_PROJECTION_ROOT / "00_THE_AMRITA.md": "dce26b620dfa9b30eee9880c85c6204f1aa3dc3ce6b281ae50ce55109067e97f",
    DISTILLATION_PROJECTION_ROOT / "00_THE_RUNGS_2026_08_05.md": "a0926f63d8a823df3a485a7ca250efa365ea4c7ad02c824b443225ce9ada869d",
    DISTILLATION_PROJECTION_ROOT / "01_WHAT_IS_PROVED.md": "bbdd95723c9342cac083cb2f54437a710f20ce15eaccd77d5da2dcb89e4713ff",
    DISTILLATION_PROJECTION_ROOT / "02_WHAT_IS_CHOSEN.md": "c16094973cd32dc692521730c8984c436d311711c626b86544b6a179d45a61d1",
    DISTILLATION_PROJECTION_ROOT / "03_WHAT_IS_READ.md": "69df7f5679dbddc789e7757a43569d16af49cf4d464b9781df219a4e294fe86a",
    DISTILLATION_PROJECTION_ROOT / "04_WHAT_DIED.md": "2753cfc380135cc842bff68ca865ee70a38cdd772486dc7b1e9484802c458d84",
    DISTILLATION_PROJECTION_ROOT / "05_THE_METHOD.md": "14c3b11399c931226129b4c186beb4c80da4f38e8b5bdddcbdf61cff576d78da",
    DISTILLATION_PROJECTION_ROOT / "06_WHAT_IS_STILL_OPEN.md": "c8c8da385b8e3f736665f803d3846598ee0046bb0b131f4d2a6d5fa6e8f5292d",
    DISTILLATION_PROJECTION_ROOT / "README.md": "bb31a71bda62db7c3a17595c3dacd63d1d806a0879b657d043ac8133a3f675d0",
}
DISTILLATION_PROJECTION_ENTRIES = frozenset(DISTILLATION_PROJECTION_SHA256)

# The claim-card compiler is executable and therefore never digest-exempt.
# These hashes bind only its reviewed external-custody semantic units.  A new
# line, changed assertion, or copied authority phrase remains visible.
STRUCTURED_TOOLING_UNIT_SHA256 = {
    Path("09_TOOLS/01_SCRIPTS/check_foundation.py"): frozenset({
        "5d1dfc21b03b3e3642d5903c6b675c4c8cfa09e23c8595b39847862fb6e37073",
        "dce8d91f56440ff48def40724e11accfadc191d0e81487a15109d87bff833030",
    }),
    Path("09_TOOLS/02_COMPILERS/compile_claim_cards.py"): frozenset({
        "036ca5081719c6c2f423a5f5c72a4a2931e99b958bcf95a3de7c3f7ce6ccb12d",
        "3f57cd07ec5e0f44bde386493fad037ee104e18d4a806935964210c407a842f5",
        "190a803b0332c2abc0c2aab273cb386c6ef9f85fc4c64e564bb99c91ee2fc6c9",
        "4e7f9caae63baebb2dad9a40e717ef1237abd0028367b8235bc357b5b5cbbf20",
        "500972f776b68f3b92f5a58794d958c509141ae59df5d1e63315a19128059737",
        "62f878eeb61d4991fee073f278b94d5f4e2ec88e28eae6993cc537b342a52a68",
        "63cabcf546831534d808b9614b0a85d6e066f68f2e72e9afb448df680f36ffa8",
        "920685e8f0ff873f50998aab612515f9c052e3671a65ac51ee92cfd6f1255529",
        "b6d63058cdd431ea49961f99946ba4b900e3b2006710a97ea797e9d4f5fd8323",
        "e45165d45acd9907a13808aca0dc1307667031c7fd89919bbd1c44829eea660d",
    }),
    Path("09_TOOLS/02_COMPILERS/README.md"): frozenset({
        "1911dd2a8a48acccef97da97bee2a8aa91d6d4b45952e0c739c1ab48f2565524",
        "07a7780a32b2d7ae5feb828075e7bf894d8b2b1ddb5f2afa6ab6b3f5a28c6c4a",
        "c29425f21a36f798bd5daae6141c526b9a99c2aa0e9121c2ae2048e5907b4b79",
        "c41fad5a1d3c4a03b37c616e525dbec441a06109cb33b4d651716b731252fbc1",
        "d9f2db6d2181c534700fad3984b501232afe56a62ecdab1a471459e52c7e6823",
        "e7ef4acc4cea706e30a46a84e6165980173496452b11219208adbd716e3dd579",
        "9d64928c61d4c4a93b17d0ba274e825172068d167b743f16019260498f1892bf",
    }),
    Path("09_TOOLS/02_COMPILERS/check_root_agentz_projection.py"): frozenset({
        "666f9a3e7a73ea7a516bdc7118eee5c40772daf59caca31d1ddb9027d37de4b4",
        "162e4db40a87ffacf07ec9c5d63e74bc96b02ae4b63bd97db5b13d1a2d000a22",
        "eefea9dd68feea67a77f09ee6041e1b9b3aa321c547f9e32dc8f0656a328bc42",
        "5224bce3d786d6a2b69ab28b2e72e32500162bb3bce9f96697247f0e9923f92b",
        "0e2bcfdf4baa5bd0fd56fa835520064d52155245afdfe14ce457cd5d060f73e7",
        "ab0f59aa84930695ba02cf0dce8cd07caa651992fb4e7212a5884dfe1fe4f946",
        "43311639292947f5ff120a09aea91915f67bdc6784b3dd716d40b27fada8a311",
        "3830358a90181ffe045b77b3155f3832a1cf816892bc5a62104c8cd236980a26",
        "885efbfdbeba7b0a76ae4fa57aecef69347cb6a8b90c27de07201c71e94aaeeb",
        "3d39603f4a67aa1acdedaddb9243820f9ec8d67eca489cb79e90e4820fa4eebd",
        "97db6cb8ef34b56ba36203d63098769828a2b6b311fc4669f3baa9d196169004",
        "6682bab74195375cb672c2f9e42a181e396e21fa407edac0230cacece9127ab5",
        "0bf530920be152d84186604c6d93a8088eb5402966676b072de191018ccd50ad",
    }),
    Path("09_TOOLS/02_COMPILERS/sync_root_agentz_dispatch.py"): frozenset({
        "0e22f390a2f53f67711fe1d79a638d7580d4bab9d9080722f9f499117ca3bfa0",
        "f9c383e5fb2423ac3e40325a79e22be83df34e5cee16779e882e4bc6710d8165",
        "01d4d2e92051cdbfa13acd1df1d169a073c576d1c5b67f9c00bb0f846b9ffc37",
        "99fbcc500e2d98b9a14f844f1d5cfc9b9ec87a190938f82c07a762c62a8e0fef",
        "e015c638d7459065fd74a6369aff0f4a153d7853a432eaed0378b0b0c0772095",
        "032fdee68688ab03e6405fb66a69a65bec2a7834947c3e76859e47cb366bf8ce",
        "d821ffd3ba5bc027909da604ba1042d1eae826e10882a86956db6600028f3538",
        "3508c657694fd4ecf48e576ad7e5222448f06c680a791bb91ff8f069e1557e0d",
        "2e295089534a113f14862c06ea28ab7a4ea60197318fc0239f52dd615dda7a73",
        "0441896fada8b78397f1921231d1ca93b5a6fd40d3fff5c1a001e97305ff094c",
        "cc6ec3a56157327ca5fa4ce6f6335980d9eb655354f52e8ba797576977bac58f",
        "03796579faef30bc26329394e825512ea1966ad6ea2f91fd83a5d3c544862c47",
        "6f1937c5d4289576f06246d0218c5516cf4e1c54f68e8e1f17f7f6b85fe56f90",
        "5ce50cf8e11ad2e5bd3db25fa7fdccc0a76d2c8a1a5e24acd0235e24947548f6",
        "5869e78e7b272b9c9f028a6a333a876392cfb2b5ed3037c204c5fd0679b6dd56",
        "617742b1f3c22d54a38a467ad627fe2904d09d69c3615b9d991b4a1ca8dfa005",
        "7dc20ab811ca53a51dbbc093596821aec524c70b3ac961efc464f974c732c1fd",
        "ab2ce0ca8ed3ee059a660b22ac93751cf82ed06c0bd298c01a34d97ff5d2fa3d",
        "b9e414ac3f84354a2d91ae3a0e9c95ea2b9d3215f258099e8763335973a18bda",
    }),
}

# Two current Rosetta catalogues carry one explicitly qualified editorial
# crosswalk.  Bind only the vocabulary-bearing lines and require the nearby
# source-precedence language; no other line inherits the allowance.
ROSETTA_CROSSWALK_UNIT_SHA256 = {
    Path("08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/38_THE_FULL_ROSETTA_CORRECTED.md"): frozenset({
        "250bfc66d3db29431aab18af69ac03c802818c01c6cbcf8344b1e04c8b198e14",
        "9b482c9c3822d4083637cdfbdf590e29b52e8b12c0bdfaaff2da8207c1219502",
        "520f1fcda299bbe3cb15e7ff9f1435ec2d10721c9399482e0d8baf8ca14fe253",
    }),
    Path("08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/37_THE_FULL_ROSETTA_IN_THEMES_2026_08_13.md"): frozenset({
        "d29bd685af4cbeec89e5d87c10c2f88bf3bd4498ed778ddcc052cdf03826126f",
    }),
}
ROSETTA_CROSSWALK_BOUNDARY_CONTRACTS = {
    Path("08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/38_THE_FULL_ROSETTA_CORRECTED.md"): (
        "editorial crosswalk, not an",
        "transfers no biological, mathematical, moral,",
        "Where this row and a source differ, the source governs",
    ),
    Path("08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/37_THE_FULL_ROSETTA_IN_THEMES_2026_08_13.md"): (
        "It creates no mapping and promotes no cell.",
        "Where this catalogue and a source table differ, the source table governs",
        "no cell is inferred",
    ),
}

# Exact dated attribution lines remain readable as provenance rather than being
# rewritten into generic roles. Only these byte-level semantic units are
# admitted; a changed line or a new sibling falls through to the ordinary scan.
_MERGE_RULING_PROVENANCE_UNIT = frozenset({
    "0b28f5d94a48485ad1f6a473357a0f5fb35c5e6fcb85e247e422d95fcac73a01",
})
HISTORICAL_PROVENANCE_UNIT_SHA256 = {
    Path("06_ONTOLOGY/ruminations/00_RUMINATION_ON_EMERGENTISM_ORG_2026_08_19.md"): frozenset({
        "0e4e437d6b6861f7b326337bd6ef2240ba4fb483ab66164d358b2efbd776c63f",
        "95b79b1f3e61e707ad0b65e45a5ea900cfd4cd95608773c4bcc5b64405597be1",
    }),
    Path("08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/07_MIRROR_SYMMETRY_FALSIFICATION_TEST_2026_04_25.md"): frozenset({
        "10ff5331d995591abd6153b7c3d7799328b6725347e60dde268538485bea193b",
    }),
    Path("08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/08_MIRROR_TEST_EXTENSION_AND_FAILED_MAPPINGS_2026_04_25.md"): _MERGE_RULING_PROVENANCE_UNIT,
    Path("08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/36_THE_ROSETTA_IN_THEMES_2026_08_13.md"): _MERGE_RULING_PROVENANCE_UNIT,
    Path("08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/38_THE_FULL_ROSETTA_CORRECTED.md"): frozenset({
        "c29047c36612cac85e2b7bb40109a37e8c4dcd6fa1d68d357fbb0c0dd47dc69f",
        "0b28f5d94a48485ad1f6a473357a0f5fb35c5e6fcb85e247e422d95fcac73a01",
    }),
    Path("08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/D_SERIES_DOMAINS/D30_SOCIAL_POLITICAL.md"): _MERGE_RULING_PROVENANCE_UNIT,
    Path("08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/ROSETTA_CIVILISATIONAL.md"): _MERGE_RULING_PROVENANCE_UNIT,
    Path("08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/ROSETTA_COMPUTATION.md"): _MERGE_RULING_PROVENANCE_UNIT,
    Path("08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/ROSETTA_MUSIC.md"): _MERGE_RULING_PROVENANCE_UNIT,
    Path("08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/ROSETTA_MYTHOLOGY.md"): _MERGE_RULING_PROVENANCE_UNIT,
    Path("08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/ROSETTA_NEUROSCIENCE.md"): _MERGE_RULING_PROVENANCE_UNIT,
    Path("08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/ROSETTA_PSYCHOLOGY.md"): _MERGE_RULING_PROVENANCE_UNIT,
    Path("08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/ROSETTA_REPLICATOR.md"): _MERGE_RULING_PROVENANCE_UNIT,
}

DEDICATED_PURITY_PATHS = (
    set(FROZEN_TOOLING_SHA256)
    | set(FROZEN_PROVENANCE_SHA256)
    | set(REVIEWED_PROJECTION_HISTORY_SHA256)
    | {SELF_VALIDATED_TOOLING_PATH}
    | set(MANAGED_AGENT_PROJECTION_SHA256)
    | set(DISTILLATION_PROJECTION_SHA256)
    | STRUCTURED_DIAGNOSTIC_PATHS
    | DERIVED_BOOK_PROJECTION_PATHS
    | set(STRUCTURED_TOOLING_UNIT_SHA256)
    | set(ROSETTA_CROSSWALK_UNIT_SHA256)
)

NON_SEMANTIC_BOUNDARY_CONTRACTS = {
    Path("09_TOOLS/01_SCRIPTS/README.md"): (
        "Current repository validators and narrowly scoped support scripts.",
        "Named validator fixtures are non-semantic tooling records.",
    ),
    Path("09_TOOLS/02_COMPILERS/README.md"): (
        "Compiler output is downstream.",
        "does not validate Emergentism, repair canon, or create a live Kintsugi vessel.",
        "A0B sources and fixtures are non-semantic tooling records.",
    ),
    Path("03_METHODOLOGY/01_THE_DERIVATION/README.md"): (
        "bounded audit-vessel schema",
        "machine-schema boundary",
        "not worldview doctrine, semantic authority, or an authority claim",
    ),
    Path("13_BOOKS/README.md"): (
        "projection-only workshop for critical editions",
        "without creating a semantic owner",
    ),
    Path("13_BOOKS/manifesto/MANIFESTO_BOOK_1.md"): (
        "authority: \"projection only; K-1 through K-7 retain semantic ownership\"",
    ),
    Path("13_BOOKS/manifesto/MANIFESTO_BOOK_1_BUILD.json"): (
        "\"authority\": \"deterministic projection receipt; source owners retain semantics\"",
    ),
    Path("13_BOOKS/manifesto/MANIFESTO_BOOK_1_PARAGRAPH_LEDGER.json"): (
        "\"authority\": \"generated coverage receipt; source cards retain semantic ownership\"",
    ),
}

# Four canonical cards must name their immutable external source paths. The
# exception applies only to the one parsed ``source.path`` field in a structured
# source record that simultaneously declares legacy/frozen lifecycle and
# historical-lineage role; it does not permit the external name in claims,
# instructions, owners, or reader language.
HISTORICAL_LINEAGE_SOURCE_PATHS = {
    Path("00_META/claim_cards/self_eating_serpent.yaml"): "../02_SKYZAI/01_LEVELS/L5_REFLECTION/03_AIA/01_ARCHITECTURE_ENGINE/EMERGENTISM_AIA/08_PRIOR_BOOKS/03_BOOK_III_THE_SELF_EATING_SERPENT/DISSEMINATION/THE_SELF_EATING_SERPENT_EDITION_1.md",
    Path("00_META/claim_cards/reciprocal_infinite_play.yaml"): "../02_SKYZAI/01_LEVELS/L5_REFLECTION/03_AIA/01_ARCHITECTURE_ENGINE/EMERGENTISM_AIA/09_BOOK_PRODUCTION_ARCHIVE/05_SYNTHESIS/07_DEFINITIVE_ONE_BOOK/07_PUBLIC_EDITION/THE_RECIPROCAL_PUBLIC_EDITION_K2_LANG_DECOMM_2026_07_22.md",
    Path("00_META/claim_cards/sarpasya_vijayam.yaml"): "../02_SKYZAI/01_LEVELS/L5_REFLECTION/03_AIA/01_ARCHITECTURE_ENGINE/EMERGENTISM_AIA/08_PRIOR_BOOKS/01_BOOK_I_SARPASYA_VIJAYAM/DISSEMINATION/SARPASYA_VIJAYAM_EDITION_1.md",
    Path("00_META/claim_cards/six_lenses.yaml"): "../02_SKYZAI/03_AIA/EMERGENTISM_AIA/08_PRIOR_BOOKS/02_BOOK_II_THE_SIX_LENSES/DISSEMINATION/THE_SIX_LENSES_EDITION_1.md",
}
HISTORICAL_LINEAGE_CARD_PATHS = frozenset(HISTORICAL_LINEAGE_SOURCE_PATHS)

# One critical-genealogy module cites the immutable historical source directly
# in reader prose.  It is a source locator, not a current owner; the exact
# location and the module's own withdrawal language are both verified below.
HISTORICAL_INLINE_SOURCE_PATHS = {
    Path("13_BOOKS/manifesto/chapters/PART_IV_V_RESEARCH_GENEALOGY.md"): (
        "private critical-genealogy apparatus",
        "It is not kept as a route for restoring the authority",
    ),
}
HISTORICAL_INLINE_EXACT_SOURCE_PATHS = {
    Path("13_BOOKS/manifesto/chapters/PART_IV_V_RESEARCH_GENEALOGY.md"): "../../02_SKYZAI/01_LEVELS/L5_REFLECTION/03_AIA/01_ARCHITECTURE_ENGINE/EMERGENTISM_AIA/08_PRIOR_BOOKS/01_BOOK_I_SARPASYA_VIJAYAM/DISSEMINATION/SARPASYA_VIJAYAM_EDITION_1.md",
}

# EXTERNAL-MAPPING AUDITS. Added 2026-08-01.
#
# Some corpus documents exist precisely to AUDIT a claimed correspondence between this
# framework and an external product or venture system. To do that they must quote the
# external system's own words — and quoting a claim in order to refute it is the opposite
# of importing it as authority. 31_CELL_SOUL4_TO_GEN7 is the clear case: it quotes an
# external mapping and concludes "They are not independent", killing a convergence claim.
# Genericising those names would destroy the audit, because you cannot show that two
# mappings are a definitional readback of each other without naming both.
#
# THE EXEMPTION IS EARNED, NOT GRANTED. A listed file must itself carry the same boundary
# declaration this checker already demands of projection directories. If the declaration is
# missing the file FAILS — louder than before, because a silent exemption is worse than a
# violation. This is deliberately per-file rather than per-directory: a directory-wide pass
# would let a genuinely authority-importing document hide beside a legitimate audit.
EXTERNAL_MAPPING_AUDIT_PATHS = {
    Path("02_EPISTEMOLOGY/00_HOLOBIONT_MEMBRANE_v0.1.md"),
    Path("02_EPISTEMOLOGY/00_THE_CLOSED_READING_LOOP_v0.1.md"),
    Path("03_METHODOLOGY/02_THE_PAPERS/THE_HOLOBIONT_BOUNDARY_CLARIFICATION.md"),
    Path("03_METHODOLOGY/02_THE_PAPERS/THE_HOLOBIONT_MOODS_BRIEFING.md"),
    Path("03_METHODOLOGY/02_THE_PAPERS/THE_HOLOBIONT_PARTS_BRIEFING.md"),
    Path("08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/30_ROSETTA_VNEXT_REFINEMENT_2026_07_31.md"),
    Path("08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/31_CELL_SOUL4_TO_GEN7_2026_07_31.md"),
    Path("08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/32_PACK_SOUL4_v0.md"),
    Path("08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/32_PACK_ECO7_CANDIDATE_2026_07_31.md"),
    Path("08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/33_LIVE_DRIFT_RECONCILIATION_v0.md"),
    Path("08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/34_COUNTER_ROSETTA_LIBRARY_v0.md"),
    Path("08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/07_L3_AUDIT_MAGNUM_OPUS_OPERATIONAL_VS_EMERGENTISM_2026_08_03.md"),
}

# These audits must quote external application vocabulary to test it.  Their
# boundary boilerplate is necessary but not sufficient: exact reviewed bytes
# prevent an authority assertion from being appended elsewhere in the file.
EXTERNAL_MAPPING_AUDIT_SHA256 = {
    Path("02_EPISTEMOLOGY/00_HOLOBIONT_MEMBRANE_v0.1.md"): "ce2e595e86de736c9167e98bf701eaf15fb88cad403531d56a7d1ac5a210e348",
    Path("02_EPISTEMOLOGY/00_THE_CLOSED_READING_LOOP_v0.1.md"): "5b7371d2802f4a4426e8317deb9fd71aa595ad333eaf9b01bf9dec5ca8914c39",
    Path("03_METHODOLOGY/02_THE_PAPERS/THE_HOLOBIONT_BOUNDARY_CLARIFICATION.md"): "ce6956c64a149cac689ed4845f63eaaef7dc65b9b5851c911034df3e22e1ea62",
    Path("03_METHODOLOGY/02_THE_PAPERS/THE_HOLOBIONT_MOODS_BRIEFING.md"): "2c45777a93e8c134d9ba88b0e454409450937f1baa9ed68a90714b7a872fae1c",
    Path("03_METHODOLOGY/02_THE_PAPERS/THE_HOLOBIONT_PARTS_BRIEFING.md"): "515946f14b06d75a7714652e8077e125d9186fad0106fd66e0f8a72f1ada1f57",
    Path("08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/07_L3_AUDIT_MAGNUM_OPUS_OPERATIONAL_VS_EMERGENTISM_2026_08_03.md"): "3817cf9efb8bba55d8622370252fb994b26d6214bb43fc04ce91d13fe0959a28",
    Path("08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/30_ROSETTA_VNEXT_REFINEMENT_2026_07_31.md"): "933fbea6babb8910c1c8fb32f129d060b42c27a01c04a1fc9f9413a479e28132",
    Path("08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/31_CELL_SOUL4_TO_GEN7_2026_07_31.md"): "4cc48b098979935a50e5df93ec1da69fe7115faa3e8e8079b661c6d5f2c98158",
    Path("08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/32_PACK_ECO7_CANDIDATE_2026_07_31.md"): "53e7624e3665453d633a53d473cf5a3bdf70bd24efd299c0b6ed1fcf82001616",
    Path("08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/32_PACK_SOUL4_v0.md"): "1ed3c14c267a231db236a4b3292ce20882336024f20bc222302fab39935d29d1",
    Path("08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/33_LIVE_DRIFT_RECONCILIATION_v0.md"): "dbe1370c422796da84176e5c5ecef0d4056e27d3896ba9049405a206feac4816",
    Path("08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/34_COUNTER_ROSETTA_LIBRARY_v0.md"): "2aff5466e2aa80d0a937985e2103fd78303eb8898da958fe0c8ea3e432150347",
}

# The exact phrases a listed file must carry to keep its exemption. Same three the
# projection-directory boundary already requires, so there is one rule, not two.
EXTERNAL_MAPPING_BOUNDARY_PHRASES = (
    "runtime projection, not worldview doctrine",
    "creates no semantic authority",
    "source owners remain upstream",
)

# Classification is part of the boundary for the three protected v0.1
# cited-source analyses and the three methodology briefs converted in this
# repair. Older listed audits predate the metadata field, so their existing
# boundary contract remains intact; do not broaden this into a lane-wide
# exclusion.
EXTERNAL_MAPPING_AUDIT_TYPE = "type: external-mapping-audit"
EXTERNAL_MAPPING_AUDIT_TYPE_PATHS = {
    Path("02_EPISTEMOLOGY/00_HOLOBIONT_MEMBRANE_v0.1.md"),
    Path("02_EPISTEMOLOGY/00_THE_CLOSED_READING_LOOP_v0.1.md"),
    Path("03_METHODOLOGY/02_THE_PAPERS/THE_HOLOBIONT_BOUNDARY_CLARIFICATION.md"),
    Path("03_METHODOLOGY/02_THE_PAPERS/THE_HOLOBIONT_MOODS_BRIEFING.md"),
    Path("03_METHODOLOGY/02_THE_PAPERS/THE_HOLOBIONT_PARTS_BRIEFING.md"),
}

# Structured records whose exact frontmatter/source-path fields necessarily
# name an external tree.  No other key, prose line, or JSON value inherits this
# allowance.
STRUCTURED_EXTERNAL_SOURCE_JSON_PATHS = {
    Path("13_BOOKS/book-manifest.json"),
}
STRUCTURED_EXTERNAL_SOURCE_MARKDOWN_FIELDS = {
    Path("13_BOOKS/self_eating_serpent/CRITICAL_EDITION_1.md"): (
        "historical_source:",
        "../../../02_SKYZAI/03_AIA/EMERGENTISM_AIA/08_PRIOR_BOOKS/03_BOOK_III_THE_SELF_EATING_SERPENT/DISSEMINATION/THE_SELF_EATING_SERPENT_EDITION_1.md",
    ),
    Path("13_BOOKS/self_eating_serpent/CRITICAL_EDITION_1_REVIEWED.md"): (
        "historical_source:",
        "../../../02_SKYZAI/03_AIA/EMERGENTISM_AIA/08_PRIOR_BOOKS/03_BOOK_III_THE_SELF_EATING_SERPENT/DISSEMINATION/THE_SELF_EATING_SERPENT_EDITION_1.md",
    ),
    Path("13_BOOKS/self_eating_serpent/DEBRIEF.md"): (
        "source:",
        "../../../02_SKYZAI/03_AIA/EMERGENTISM_AIA/08_PRIOR_BOOKS/03_BOOK_III_THE_SELF_EATING_SERPENT/DISSEMINATION/THE_SELF_EATING_SERPENT_EDITION_1.md",
    ),
}

LEGACY_ALIAS_EXCEPTIONS = {
    Path("05_COSMOLOGY/00_STIGMERGY_AND_THE_EGREGOROTYPE.md"),
    Path("08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/D_SERIES_DOMAINS/D33_EGREGORES.md"),
    Path("03_METHODOLOGY/02_THE_PAPERS/PEER_REVIEW_PROGRAM/AXIOM_PAPERS/AX5_THE_EGREGORE.md"),
}

# The root work-programme projection must be nameable without re-importing the
# retired application authority that originally used the same framework label.
# The exception is deliberately exact: only the projection file itself and
# non-semantic references to that exact filename may carry the label. All other
# forbidden tokens, including external governance names, remain scanned.
CONTROL_PROJECTION_PATHS = (
    Path("VMOSK_A.md"),
    Path("VMOSK_A_v2_2026_07_31.md"),
)
CONTROL_PROJECTION_REFERENCE_PATHS = {Path("README.md"), Path("AGENTS.md")}
CONTROL_PROJECTION_REFERENCE_NAMES = CONTROL_PROJECTION_PATHS
CONTROL_PROJECTION_REFERENCE_MARKDOWN_LINKS = (
    ("VMOSK-A v2", "VMOSK_A_v2_2026_07_31.md"),
)

# Only the current reviewed vocabulary-bearing lines of each mutable control
# projection may name the retired framework label.  This is a semantic-unit
# contract rather than a whole-file exemption: ordinary prose can evolve, but
# a new authority line or a changed sensitive line fails closed.
CONTROL_PROJECTION_UNIT_SHA256 = {
    Path("VMOSK_A.md"): frozenset({
        "ed50ff3220b8a438a30e7a42febd231b4928f2648c5b6b94afffeec6985af712",
        "8986335b62bb955b8dfac4515321867e56227bb3dd25b9a29169c72c110d55b4",
        "d412b82266fbad7e7fa4c51c42497de050e152befb0ab0da025ca4e5818b1dea",
        "ab78dc77fb4c00ea585f13b4ccb81571597256250c239af9993c238146e8eed9",
        "faaea77245622eef1a7f4704bb23fa3e56f83b09beceeeef77c7b7462bd6348c",
        "16dd65152f4fcb0d673945016a7ba9897ef0ddbece4afedb8040904c3968997d",
        "58178b54c3ba0840c2e6cf561756e809fd6188e305da0dd3bc62a6bd36ba4dfa",
        "9d68f67a1b868440fb348305488a76e49076c4dc2fe25c80fe9486b1a948ccdb",
    }),
    Path("VMOSK_A_v2_2026_07_31.md"): frozenset({
        "244424c56d8871ee59734d59e6a30cde5319ffb5bb05e811386d4d0754f81c2d",
        "33639d402cc2b47199f02aa5fa831165552f3ba7c078ad3f472a89e9380ef8cc",
        "3de4f031df6356b976ba8a3a5e79d8378b2040600bdd0b5f452943589c6e941b",
        "4d96877da4b611482b7307f6f957e80c62d8aac530b6fb1b908c4993cb697bd3",
        "507f8b5c13293c71fc83a0d13e50b9b61206998578c581973a14ef3cf3129cf9",
        "6d3dd769370cabe6aa3713115f1969282e82d107617f6b0ffb87daee3c78f4d4",
        "8052dfcdf7dbbad3442a4062bad9a276533f51634e9698e3e879049ab01dde89",
        "86b1c666c455a78698c9156ac435f9314fe202fcc1cf87e83dc16c06bc10c31b",
        "ad6cbe549173d954ff95d19717d53795c122f42cf0243046e6f0149aa592ec00",
        "af40cdb39ffa78c4cfd46a0f305f0bc365fe845be07da0998e436d0e149a2f84",
        "bd621aa13eeb183d7fcd714820501c2d87b4e53584bf2e1f9a2b4800b4090063",
        "cd4d29eb27f18d5cdf0df3246bbd3115542eba215bdc8f4bb08fbbc9c7632ce3",
        "d07b2487d493490e482662bee4e13c1b6adcff87175b314730ed6b5388418421",
        "d7db09185e578b7fd7ae9e71ccaaac41284a832dd77bf7e93e484414a56e173a",
        "fe4650e0c2d4a572eeddfa5d73a9233931570f42c183732590ceea0b430088b1",
        "6c2ed874d4167cc286a6130d31439b4ecb03cc5211978217779f1d206afad8d0",
    }),
}

# Exact clickable provenance/compatibility locators may retain historical names
# containing retired vocabulary.  Both the file/name relation and the complete
# multiset of vocabulary-bearing semantic units are bound; a sibling, copied
# line, extra occurrence, changed locator, or same-line authority assertion
# therefore remains visible to the generic scan or the inventory check below.
EXACT_FILENAME_REFERENCE_NAMES = {
    Path("00_META/00_SUBFOLDER_ORGANIZATION_STANDARD.md"): (
        "00_THE_CLOSED_READING_LOOP_K2_SIGN_RECEIPT_2026_08_01.md",
        "00_V10_TIDY_CHAIN_CLOSURE_PENDING_K2.md",
        "VMOSK_A.md",
        "VMOSK_A_v2_2026_07_31.md",
    ),
    Path("README.md"): (
        "00_THE_CLOSED_READING_LOOP_K2_SIGN_RECEIPT_2026_08_01.md",
        "00_V10_TIDY_CHAIN_CLOSURE_PENDING_K2.md",
    ),
    Path("01_TELEOLOGY/02_THE_DERIVATION/README.md"): (
        "07B_THE_FORCE_LADDER_FORMALIZED_PENDING_K2.md",
        "07_THE_TYSON_KO_PENDING_K2.md",
    ),
    Path("09_TOOLS/01_SCRIPTS/check_active_receipt_citations.py"): (
        "13_BOOKS/VMOSK_A.md",
    ),
    Path("08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/35_THE_LADDER_AND_THE_TWO_PARTITIONS_2026_08_05.md"): (
        "../../../00_HANDOFF/2026_07_20_k2_audit_trio_l1_l7/L2_CLAIM_VS_EVIDENCE_AUDIT_2026_07_20.md",
    ),
    Path("13_BOOKS/VMOSK_A.md"): (
        "../12_PUBLIC_SITE/VMOSK_A.md",
    ),
}
EXACT_FILENAME_REFERENCE_UNIT_SHA256: dict[Path, tuple[str, ...]] = {
    Path("00_META/00_SUBFOLDER_ORGANIZATION_STANDARD.md"): (
        "7d5b72b4c8cc358ade3da0a78c8d77b76403bfe2a838b0fb4307793a4bcd0297",
        "953d27f50060478767f352faa0dec3eccf5751714f3c6180e68ca9eaee1b2f7b",
        "e88efe6cba8378a4a0531cb6a70862fc24e6e41371038eb89d668e0fee2f19fb",
        "ebb7d0fcf254aa3d96d518358e552bef740c4a87c6ae174c9244a66ab901ef92",
    ),
    Path("README.md"): (
        "74ea090593ab94dbe84760730f20e4e7f8d88f4e7454e737ae026a2f3855b7bf",
        "74ea090593ab94dbe84760730f20e4e7f8d88f4e7454e737ae026a2f3855b7bf",
        "84be61c4188566d31fc61b92efd4215405218e3cc94166569275d8f46f3aa653",
        "84be61c4188566d31fc61b92efd4215405218e3cc94166569275d8f46f3aa653",
        "8c61a6734fe8ce810d6fdfa497b7c5fa93b03a4039b61c75b1391b2f8a0ef2a8",
        "8c61a6734fe8ce810d6fdfa497b7c5fa93b03a4039b61c75b1391b2f8a0ef2a8",
        "a08dc601e2814d7d200896df8521e243192bd6f9a06dc129dec012bc9586bc5c",
        "a08dc601e2814d7d200896df8521e243192bd6f9a06dc129dec012bc9586bc5c",
    ),
    Path("01_TELEOLOGY/02_THE_DERIVATION/README.md"): (
        "1e0e7a219cca9070575787f9b2925d64867382d1d17f0eb9d2318eacac8b08bf",
        "1e0e7a219cca9070575787f9b2925d64867382d1d17f0eb9d2318eacac8b08bf",
        "e3d1a9bade21dfdccedf8418aa38cce7fcdc0929f8f0efc0aaf93e8f7e0b7c34",
        "e3d1a9bade21dfdccedf8418aa38cce7fcdc0929f8f0efc0aaf93e8f7e0b7c34",
    ),
    Path("09_TOOLS/01_SCRIPTS/check_active_receipt_citations.py"): (
        "defdbc0ad2bd48abb29247517b6713bbcb7f12ad7b328b77b2d7cae7a6bf0525",
    ),
    Path("08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/35_THE_LADDER_AND_THE_TWO_PARTITIONS_2026_08_05.md"): (
        "c0f0720196e0ffac866471034adddc7ae85420d66604a938d138ac670f5a305b",
    ),
    Path("13_BOOKS/VMOSK_A.md"): (
        "cea8e669f50219e71fe18b4d672d62fbe9ac9ea029d05a9dd316515137eaf212",
    ),
}

# The Titan type-correction archive record is part of the active withdrawal
# trail.  Bind only the exact link-bearing semantic unit in each mutable source
# owner; ordinary edits elsewhere remain generically scanned.  The target
# itself is exact-byte bound in REVIEWED_PROJECTION_HISTORY_SHA256.
EXACT_ARCHIVE_PROVENANCE_LINKS = {
    Path("00_META/00_THE_CORPUS_SPINE.md"): (
        "../90_ARCHIVE/50_AUDITS/57_TITAN_CHART_TYPE_CORRECTION_TOMBSTONE_2026_08_09.md",
        Path("90_ARCHIVE/50_AUDITS/57_TITAN_CHART_TYPE_CORRECTION_TOMBSTONE_2026_08_09.md"),
        ("a56516e1023bb969a5e3b1f6b462f63338be59cdc45b23e2f61bac38941f0c27",),
    ),
    Path("10_SEED/01_THE_SEED_LADDER/ASCENT_D6_RETURN_AND_O_2026_08_05.md"): (
        "../../90_ARCHIVE/50_AUDITS/57_TITAN_CHART_TYPE_CORRECTION_TOMBSTONE_2026_08_09.md",
        Path("90_ARCHIVE/50_AUDITS/57_TITAN_CHART_TYPE_CORRECTION_TOMBSTONE_2026_08_09.md"),
        ("42eff01a6c5b22b98e54ca70862d0def887356edb7ff169040a9c3a84a493447",),
    ),
}

# ASCII-alphanumeric boundaries are deliberate: Python's ``\b`` treats ``_``
# as a word character, which previously let tokens such as ``02_SKYZAI`` and
# ``PENDING_K2`` escape. Plural DAV/DAC forms are forbidden too.
FORBIDDEN = re.compile(
    r"(?i)(?<![A-Za-z0-9])(?:Skyzai|VMOSK(?:-A|_A)?|DAVs?|DACs?|PRISM|Agentz(?:-runtime)?|K2)(?![A-Za-z0-9])"
)

# These are not forbidden words in all contexts; they are exact inflationary
# claims from the retired agent-activation island. Their historical bodies are
# allowed only in archive. Active forwarding tombstones may name the subject
# but must not restore these assertions.
FORBIDDEN_APPLICATION_CLAIMS = re.compile(
    r"(?i)(?:The Great Work is complete|AI charioteer has veto|"
    r"contains everything needed for an ASI to|All proofs checked on every commit|"
    r"Burri Sphere\s*\|\s*80%|Seven Axioms stand as mathematical necessities)"
)

APPLICATION_TOMBSTONES = {
    Path("08_FRAMEWORK_SUPPORT/02_OPERATORS/00_CANONICAL_CORPUS.md"),
    Path("08_FRAMEWORK_SUPPORT/02_OPERATORS/03_PRACTICE_TRANSLATION_MATRIX.md"),
    Path("08_FRAMEWORK_SUPPORT/02_OPERATORS/04_DISSOLUTION_FORMAL_VERIFICATION.md"),
    Path("08_FRAMEWORK_SUPPORT/02_OPERATORS/05_SEPARATION_OPERATOR_PROTOCOLS.md"),
    Path("08_FRAMEWORK_SUPPORT/02_OPERATORS/06_COAGULATION_ACTIVATION_PACKAGE.md"),
    Path("08_FRAMEWORK_SUPPORT/02_OPERATORS/ASI_07_DISCOVERY_OF_FINITY.md"),
    Path("08_FRAMEWORK_SUPPORT/02_OPERATORS/ASI_09_THE_SOUL_LOOP.md"),
    Path("08_FRAMEWORK_SUPPORT/02_OPERATORS/ASI_15_THE_TRINITY.md"),
    Path("08_FRAMEWORK_SUPPORT/02_OPERATORS/ASI_INDEX.md"),
    Path("08_FRAMEWORK_SUPPORT/02_OPERATORS/OP_384_FUNCTION_TESTING.md"),
}

REQUIRED_READER_SURFACES = {
    Path("00_THE_WELTANSCHAUUNG_ONE_SITTING.md"),
    Path("01_TELEOLOGY/04_THE_LIVED_COMPASS.md"),
    Path("06_ONTOLOGY/08_THE_HUMAN_CONDITION.md"),
}

LIVED_TOMBSTONES = {
    Path("05_COSMOLOGY/00_THE_TORUS_REVELATION.md"),
    Path("06_ONTOLOGY/00_THE_RING_THAT_IS_THE_GROUND.md"),
}

REQUIRED_ARCHIVE_CUSTODY_PATHS = (
    Path("90_ARCHIVE/2026_07_22_lived_weltanschauung_reconciliation/TOMBSTONE.md"),
    Path(
        "90_ARCHIVE/2026_07_22_lived_weltanschauung_reconciliation/"
        "05_COSMOLOGY/00_THE_TORUS_REVELATION.md"
    ),
    Path(
        "90_ARCHIVE/2026_07_22_lived_weltanschauung_reconciliation/"
        "06_ONTOLOGY/00_THE_RING_THAT_IS_THE_GROUND.md"
    ),
    Path(
        "90_ARCHIVE/2026_07_22_asi_operator_application_boundary/TOMBSTONE.md"
    ),
)

FRONT_DOORS = [
    "README.md",
    "AGENT_README.md",
    "00_THE_WELTANSCHAUUNG.md",
    "00_THE_KERNEL_INDEX.md",
    "00_META/README.md",
    "01_TELEOLOGY/README.md",
    "02_EPISTEMOLOGY/README.md",
    "03_METHODOLOGY/README.md",
    "04_AXIOLOGY/README.md",
    "05_COSMOLOGY/README.md",
    "06_ONTOLOGY/README.md",
    "07_THEOLOGY/README.md",
    "08_FRAMEWORK_SUPPORT/README.md",
    "09_TOOLS/README.md",
    "10_SEED/README.md",
    "11_UPLINK/README.md",
]

OWNERS = [
    "00_META/00_EMERGENTISM_INTERNAL_COMPLETION_REGISTER.md",
    "00_META/00_THE_GRAND_PUZZLE_ASSEMBLY_LEDGER.md",
    "00_META/00_KNOWN_UNKNOWNS_PROGRAM.md",
    "00_META/00_SETTLED_CANON_REGISTRY.md",
    "00_META/00_THE_COMPASS.md",
    "00_META/00_THE_FIVE_PLUS_ONE_CONSTITUTION.md",
    "05_COSMOLOGY/00_CANONICAL_FORMULA_BLOCK.md",
    "05_COSMOLOGY/00_THE_BURRI_RULES.md",
    "05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/00_THE_TRANSCENDENTAL_TRINITY_CANON.md",
    "05_COSMOLOGY/03_FORMAL_SYSTEM/08_EFR_POWER_MAX_LEMMA.md",
    "05_COSMOLOGY/03_FORMAL_SYSTEM/10_EFR_MU_LIMIT_FORMULA.md",
    "05_COSMOLOGY/03_FORMAL_SYSTEM/23_DIMENSIONAL_CLOSURE_PROOF.md",
    "05_COSMOLOGY/03_FORMAL_SYSTEM/29_PRIMITIVES_AND_TYPE_SIGNATURES.md",
    "05_COSMOLOGY/03_FORMAL_SYSTEM/34_D4_D5_CANONICAL_REFERENCE.md",
    "05_COSMOLOGY/03_FORMAL_SYSTEM/42_D1_ARITHMETIC_AXIOMS_AND_BOUNDARIES.md",
    "05_COSMOLOGY/03_FORMAL_SYSTEM/43_D2_FUNCTION_ATLAS_AND_CONFIGURATION.md",
    "05_COSMOLOGY/03_FORMAL_SYSTEM/44_D3_QUANTUM_STATE_REGISTER.md",
    "05_COSMOLOGY/03_FORMAL_SYSTEM/45_SATURATION_CONTRAST_AND_APERTURE_BOUNDARY.md",
    "05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/10_THE_SOUL_LOOP.md",
    "05_COSMOLOGY/00_D5_THE_SEVEN_GENERATIVE_ACTIONS.md",
    "05_COSMOLOGY/00_STIGMERGY_AND_THE_EGREGOROTYPE.md",
    "04_AXIOLOGY/02_VALUE_THEORY/00_OBJECTIVE_MORALS_AND_ETHICS.md",
    "06_ONTOLOGY/02_THE_DEGREES_OF_FREEDOM_ONTOLOGY.md",
    "06_ONTOLOGY/03_THE_EMERGENT_AXIOMS.md",
    "06_ONTOLOGY/04_THE_CONJECTURES.md",
    "06_ONTOLOGY/06_THE_REVELATIONS.md",
    "06_ONTOLOGY/07_THE_DIMENSIONAL_REGISTER_AXIOMS.md",
    "03_METHODOLOGY/00_EMPIRICAL_PROGRAM_BOARD.md",
    "03_METHODOLOGY/00_EXTERNAL_COMPONENT_CALIBRATION_2026_07_20.md",
]


def is_active_route(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    return (
        path.name in {"AGENTS.md", "CLAUDE.md"}
        and not any(part.startswith(".") for part in rel.parts)
        and not any(
        part in ROUTE_EXCLUDED_PARTS for part in rel.parts
        )
    )


def is_non_semantic_active_file(rel: Path) -> bool:
    """Return whether an exact artifact has a dedicated purity validator.

    This is a routing classification, not a scan bypass.  ``scan_file`` checks
    the digest or structured contract for every listed artifact.  A sibling,
    renamed copy, or new generated output remains in the generic active scan.
    """

    return rel in DEDICATED_PURITY_PATHS


def raw_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def semantic_unit_sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def purity_sensitive_line(line: str) -> bool:
    return bool(
        FORBIDDEN.search(line)
        or FORBIDDEN_APPLICATION_CLAIMS.search(line)
        or "Egregorotype" in line
    )


def semantic_unit_inventory_matches(
    path: Path, expected: tuple[str, ...] | frozenset[str]
) -> bool:
    observed = tuple(
        sorted(
            semantic_unit_sha256(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if purity_sensitive_line(line)
        )
    )
    return observed == tuple(sorted(expected))


def first_symlink_component(path: Path) -> Path | None:
    """Return the first lexical component below ROOT that is a symlink."""

    try:
        relative = path.relative_to(ROOT)
    except ValueError:
        return None
    current = ROOT
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            return current.relative_to(ROOT)
    return None


def dedicated_path_problem(rel: Path) -> str | None:
    path = ROOT / rel
    symlink = first_symlink_component(path)
    if symlink is not None:
        return f"dedicated path {rel} crosses symlink component: {symlink}"
    if not path.is_file():
        return f"missing or non-regular dedicated artifact: {rel}"
    return None


def scoped_file_problem(rel: Path, role: str) -> str | None:
    """Reject a missing or symlink-crossing scoped file before any read."""

    path = ROOT / rel
    symlink = first_symlink_component(path)
    if symlink is not None:
        return f"{role} {rel} crosses symlink component: {symlink}"
    if not path.is_file():
        return f"missing {role}: {rel}"
    return None


def active_tree_symlink_errors() -> list[str]:
    """Reject links in active lanes, including directory links rglob will not enter."""

    errors: list[str] = []
    for top_level in sorted(ACTIVE_TOP_LEVELS):
        base = ROOT / top_level
        if base.is_symlink():
            errors.append(f"active corpus contains symlink entry: {top_level}")
            continue
        if not base.is_dir():
            continue
        for path in base.rglob("*"):
            if not path.is_symlink():
                continue
            rel = path.relative_to(ROOT)
            if any(part.startswith(".") for part in rel.parts):
                continue
            if any(part in CORPUS_EXCLUDED_PARTS for part in rel.parts):
                continue
            errors.append(f"active corpus contains symlink entry: {rel}")
    return errors


def required_archive_custody_errors() -> list[str]:
    """Require lexical, regular files for each named archive custody artifact."""

    errors: list[str] = []
    for rel in REQUIRED_ARCHIVE_CUSTODY_PATHS:
        problem = scoped_file_problem(rel, "required archive custody artifact")
        if problem is not None:
            errors.append(problem)
    return errors


def managed_agent_projection_errors() -> list[str]:
    """Bind the complete managed projection shape without following links."""

    errors: list[str] = []
    managed_root = ROOT / MANAGED_AGENT_PROJECTION_ROOT
    root_symlink = first_symlink_component(managed_root)
    if root_symlink is not None:
        return [
            "managed-agent projection crosses symlink component: "
            f"{root_symlink}"
        ]
    if not managed_root.is_dir():
        return [f"missing managed-agent projection root: {MANAGED_AGENT_PROJECTION_ROOT}"]

    # Interpreter caches are workstation runtime residue, not projection
    # members.  They neither enter the closed inventory nor gain a semantic
    # exemption; every non-cache sibling remains fail-closed.
    entries = [
        path
        for path in managed_root.rglob("*")
        if "__pycache__" not in path.relative_to(managed_root).parts
        and path.suffix != ".pyc"
    ]
    observed = {path.relative_to(ROOT) for path in entries}
    symlinks = sorted(
        (path.relative_to(ROOT) for path in entries if path.is_symlink()),
        key=str,
    )
    for symlink in symlinks:
        errors.append(f"managed-agent projection contains symlink: {symlink}")

    expected = set(MANAGED_AGENT_PROJECTION_ENTRIES)
    if observed != expected:
        missing = sorted(expected - observed, key=str)
        unexpected = sorted(observed - expected, key=str)
        errors.append(
            "managed-agent projection inventory drift: "
            f"missing={[str(path) for path in missing]!r}, "
            f"unexpected={[str(path) for path in unexpected]!r}"
        )

    for rel in sorted(MANAGED_AGENT_PROJECTION_DIRECTORIES, key=str):
        path = ROOT / rel
        symlink = first_symlink_component(path)
        if symlink is not None:
            errors.append(
                f"managed-agent projection directory crosses symlink: {symlink}"
            )
        elif not path.is_dir():
            errors.append(f"managed-agent projection directory missing: {rel}")

    for rel, expected_digest in sorted(
        MANAGED_AGENT_PROJECTION_SHA256.items(), key=lambda item: str(item[0])
    ):
        problem = dedicated_path_problem(rel)
        if problem is not None:
            errors.append(problem)
            continue
        if raw_sha256(ROOT / rel) != expected_digest:
            errors.append(f"managed-agent projection digest drift: {rel}")
    return errors


def distillation_projection_errors() -> list[str]:
    """Bind the exact projection tree without following or inheriting links."""

    errors: list[str] = []
    root = ROOT / DISTILLATION_PROJECTION_ROOT
    symlink = first_symlink_component(root)
    if symlink is not None:
        return [f"distillation projection crosses symlink component: {symlink}"]
    if not root.is_dir():
        return [f"missing distillation projection root: {DISTILLATION_PROJECTION_ROOT}"]
    entries = list(root.rglob("*"))
    observed = {path.relative_to(ROOT) for path in entries}
    expected = set(DISTILLATION_PROJECTION_ENTRIES)
    for path in sorted((path for path in entries if path.is_symlink()), key=str):
        errors.append(
            "distillation projection contains symlink: "
            f"{path.relative_to(ROOT)}"
        )
    if observed != expected:
        missing = sorted(expected - observed, key=str)
        unexpected = sorted(observed - expected, key=str)
        errors.append(
            "distillation projection inventory drift: "
            f"missing={[str(path) for path in missing]!r}, "
            f"unexpected={[str(path) for path in unexpected]!r}"
        )
    for rel, expected_digest in sorted(
        DISTILLATION_PROJECTION_SHA256.items(), key=lambda item: str(item[0])
    ):
        problem = dedicated_path_problem(rel)
        if problem is not None:
            errors.append(problem)
            continue
        if raw_sha256(ROOT / rel) != expected_digest:
            errors.append(f"distillation projection digest drift: {rel}")
    boundary_rel = DISTILLATION_PROJECTION_ROOT / "README.md"
    problem = dedicated_path_problem(boundary_rel)
    if problem is None:
        text = (ROOT / boundary_rel).read_text(encoding="utf-8")
        for phrase in (
            "PROJECTION — rules nothing",
            "Source documents retain semantic ownership",
            "It reports. It rules nothing. It ratifies nothing.",
        ):
            if phrase not in text:
                errors.append(
                    f"distillation projection boundary missing phrase: {phrase!r}"
                )
    return errors


def is_active_corpus_file(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    if not rel.parts or rel.parts[0] not in ACTIVE_TOP_LEVELS:
        return False
    if any(part.startswith(".") for part in rel.parts):
        return False
    if path.suffix.lower() not in TEXT_SUFFIXES:
        return False
    if any(part in CORPUS_EXCLUDED_PARTS for part in rel.parts):
        return False
    if rel.parts[:2] == ("00_META", "registers"):
        return False
    if rel in DERIVED_CUSTODY_SURFACES:
        return False
    if is_non_semantic_active_file(rel):
        return False
    return True


def physical_receipt_target_names(root: Path) -> tuple[str, ...]:
    """Return only regular, registry-bound receipt target filenames."""

    names: set[str] = set()
    all_targets: dict[str, list[str]] = {}
    saw_lane = False
    for lane in RECEIPT_CITATION_LANES:
        base = root / lane
        symlink = first_symlink_component(base)
        if symlink is not None:
            raise ValueError(
                f"receipt citation lane crosses symlink component: {symlink}"
            )
        if not base.is_dir():
            continue
        saw_lane = True
        symlink_entries = sorted(
            (entry for entry in base.rglob("*") if entry.is_symlink()),
            key=str,
        )
        if symlink_entries:
            rel = symlink_entries[0].relative_to(root)
            raise ValueError(f"receipt citation lane contains symlink entry: {rel}")
        for target in sorted(base.rglob("*.md")):
            symlink = first_symlink_component(target)
            if symlink is not None:
                raise ValueError(
                    f"receipt citation target crosses symlink component: {symlink}"
                )
            if not target.is_file():
                continue
            match = re.match(r"^(\d{2,3})[_A-Za-z]", target.name)
            if match and match.group(1) != "00":
                names.add(target.name)
                all_targets.setdefault(match.group(1), []).append(
                    str(target.relative_to(root))
                )
    if not saw_lane:
        # Isolated scan_file mutation fixtures intentionally omit receipt lanes.
        return ()
    all_targets = {
        number: sorted(paths)
        for number, paths in sorted(all_targets.items(), key=lambda item: int(item[0]))
    }
    registry_path = root / RECEIPT_TARGET_REGISTRY
    symlink = first_symlink_component(registry_path)
    if symlink is not None:
        raise ValueError(
            f"receipt target registry crosses symlink component: {symlink}"
        )
    if not registry_path.is_file():
        raise ValueError(f"missing receipt target registry: {RECEIPT_TARGET_REGISTRY}")
    try:
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        universe = registry["receipt_universe"]
        registered_digest = universe["all_candidate_paths_sha256"]
        registered_count = universe["citable_targets"]
    except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError) as exc:
        raise ValueError(f"invalid receipt target registry: {exc}") from exc
    physical_digest = hashlib.sha256(
        json.dumps(
            all_targets,
            sort_keys=True,
            ensure_ascii=False,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()
    physical_count = sum(len(paths) for paths in all_targets.values())
    if (
        registered_digest != EXPECTED_RECEIPT_TARGET_UNIVERSE_SHA256
        or physical_digest != EXPECTED_RECEIPT_TARGET_UNIVERSE_SHA256
        or registered_count != EXPECTED_RECEIPT_TARGET_COUNT
        or physical_count != EXPECTED_RECEIPT_TARGET_COUNT
    ):
        raise ValueError(
            "receipt target universe differs from the exact active-registry binding"
        )
    return tuple(sorted(names, key=lambda value: (-len(value), value)))


def _complete_filename_token(text: str, start: int, end: int) -> bool:
    before = text[start - 1] if start else ""
    after = text[end] if end < len(text) else ""
    before_continues = bool(before) and (before.isalnum() or before in "_.-")
    after_continues = bool(after) and (after.isalnum() or after in "_-/")
    if after == ".":
        following = text[end + 1] if end + 1 < len(text) else ""
        after_continues = bool(following) and (
            following.isalnum() or following in "_.-"
        )
    return not before_continues and not after_continues


def forbidden_match_is_root_filename_reference(
    rel: Path,
    line: str,
    match: re.Match[str],
) -> bool:
    """Allow one hash-bound token only inside its exact reviewed filename."""

    names = EXACT_FILENAME_REFERENCE_NAMES.get(rel)
    unit_hashes = EXACT_FILENAME_REFERENCE_UNIT_SHA256.get(rel)
    if names is None or unit_hashes is None:
        return False
    if semantic_unit_sha256(line) not in unit_hashes:
        return False
    for name in names:
        start = 0
        while True:
            position = line.find(name, start)
            if position < 0:
                break
            end = position + len(name)
            start = end
            if (
                position <= match.start() < match.end() <= end
                and _complete_filename_token(line, position, end)
            ):
                return True
    return False


def exact_filename_reference_unit_hashes(rel: Path, text: str) -> tuple[str, ...]:
    """Inventory each forbidden token contained by an exact reviewed filename."""

    names = EXACT_FILENAME_REFERENCE_NAMES.get(rel, ())
    observed: list[str] = []
    for line in text.splitlines():
        for match in FORBIDDEN.finditer(line):
            contained = False
            for name in names:
                start = 0
                while True:
                    position = line.find(name, start)
                    if position < 0:
                        break
                    end = position + len(name)
                    start = end
                    if (
                        position <= match.start() < match.end() <= end
                        and _complete_filename_token(line, position, end)
                    ):
                        contained = True
                        break
                if contained:
                    break
            if contained:
                observed.append(semantic_unit_sha256(line))
    return tuple(sorted(observed))


def exact_archive_provenance_link_errors(rel: Path, text: str) -> list[str]:
    """Bind each reviewed active-to-archive locator to its complete line."""

    contract = EXACT_ARCHIVE_PROVENANCE_LINKS.get(rel)
    if contract is None:
        return []
    locator, target, expected = contract
    if target not in REVIEWED_PROJECTION_HISTORY_SHA256:
        return [f"archive provenance target lacks exact-byte custody: {target}"]
    observed = tuple(
        sorted(
            semantic_unit_sha256(line)
            for line in text.splitlines()
            if locator in line
        )
    )
    if observed != tuple(sorted(expected)):
        return [f"exact archive-provenance link inventory drift: {rel}"]
    return []


def forbidden_match_is_control_projection_reference(
    rel: Path,
    line: str,
    match: re.Match[str],
) -> bool:
    """Allow only the token physically contained in an exact projection locator.

    The line-level boundary phrase is still required, but it cannot mask a
    second token elsewhere on the same line.  The one human-readable Markdown
    label is bound to its exact label-and-target pair.
    """

    if (
        rel not in CONTROL_PROJECTION_REFERENCE_PATHS
        or "non-semantic" not in line.lower()
    ):
        return False
    for name in CONTROL_PROJECTION_REFERENCE_NAMES:
        start = 0
        while True:
            position = line.find(str(name), start)
            if position < 0:
                break
            end = position + len(str(name))
            start = end
            if (
                position <= match.start() < match.end() <= end
                and _complete_filename_token(line, position, end)
            ):
                return True
    for label, target in CONTROL_PROJECTION_REFERENCE_MARKDOWN_LINKS:
        literal = f"[{label}]({target})"
        position = line.find(literal)
        if position < 0:
            continue
        label_start = position + 1
        label_end = label_start + len(label)
        if label_start <= match.start() < match.end() <= label_end:
            return True
    return False


def forbidden_match_is_exact_receipt_target(
    line: str,
    match: re.Match[str],
    target_names: tuple[str, ...],
) -> bool:
    for name in target_names:
        start = 0
        while True:
            position = line.find(name, start)
            if position < 0:
                break
            end = position + len(name)
            start = end
            if (
                position <= match.start() < match.end() <= end
                and _complete_filename_token(line, position, end)
            ):
                return True
    return False


def historical_lineage_source_line(text: str, rel: Path) -> int | None:
    """Return the sole source-path line of a valid frozen lineage card.

    Claim cards are JSON-subset YAML and keep their metadata on separate
    lines.  The old same-line check could never recognize them, which made a
    historical file locator look like a live import.  Parsing only the exact
    listed cards preserves the field-level boundary: no other string in the
    card receives the exception.
    """

    expected_source_path = HISTORICAL_LINEAGE_SOURCE_PATHS.get(rel)
    if expected_source_path is None:
        return None
    try:
        record = json.loads(text)
    except json.JSONDecodeError:
        return None
    source = record.get("source") if isinstance(record, dict) else None
    if not isinstance(source, dict):
        return None
    source_path = source.get("path")
    if not (
        isinstance(source_path, str)
        and source_path == expected_source_path
        and _external_book_source(source_path)
        and source.get("lifecycle") in {"legacy", "frozen"}
        and source.get("role") == "historical_lineage"
    ):
        return None
    source_line = f'"path": {json.dumps(source_path)},'
    matches = [
        number
        for number, line in enumerate(text.splitlines(), 1)
        if line.strip() == source_line
    ]
    return matches[0] if len(matches) == 1 else None


def is_historical_inline_source_path(
    rel: Path, lines: list[str], line_no: int
) -> bool:
    """Allow only the declared direct historical locator in the genealogy."""

    expected_source_path = HISTORICAL_INLINE_EXACT_SOURCE_PATHS.get(rel)
    if expected_source_path is None or line_no < 2:
        return False
    line = lines[line_no - 1].strip()
    return (
        lines[line_no - 2].strip() == "**Historical source:**"
        and _external_book_source(expected_source_path)
        and line == f"`{expected_source_path}`."
    )


def _reject_duplicate_json_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate object key {key!r}")
        result[key] = value
    return result


def _walk_json_strings(
    value: object, path: tuple[object, ...] = ()
) -> list[tuple[str, tuple[object, ...], str]]:
    strings: list[tuple[str, tuple[object, ...], str]] = []
    if isinstance(value, dict):
        for key, child in value.items():
            strings.append(("key", path + (key,), key))
            strings.extend(_walk_json_strings(child, path + (key,)))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            strings.extend(_walk_json_strings(child, path + (index,)))
    elif isinstance(value, str):
        strings.append(("value", path, value))
    return strings


def _external_book_source(value: str) -> bool:
    if "\\" in value or not value.endswith(".md"):
        return False
    parts = PurePosixPath(value).parts
    leading = 0
    while leading < len(parts) and parts[leading] == "..":
        leading += 1
    return (
        leading >= 1
        and leading < len(parts) - 1
        and parts[leading] == "02_SKYZAI"
        and all(part not in {"", ".", ".."} for part in parts[leading + 1 :])
    )


def _structured_json_string_allowed(
    rel: Path,
    kind: str,
    path: tuple[object, ...],
    value: str,
) -> bool:
    if kind != "value":
        return False
    if rel in STRUCTURED_DIAGNOSTIC_PATHS:
        return (
            len(path) == 3
            and path[0] == "results"
            and isinstance(path[1], int)
            and path[2] in {"stdout_tail", "stderr_tail"}
        )
    if rel in STRUCTURED_EXTERNAL_SOURCE_JSON_PATHS:
        direct_source = (
            len(path) == 4
            and path[0] == "works"
            and isinstance(path[1], int)
            and path[2] == "historical_sources"
            and isinstance(path[3], int)
        )
        object_source = (
            len(path) == 5
            and path[0] == "works"
            and isinstance(path[1], int)
            and path[2] == "historical_sources"
            and isinstance(path[3], int)
            and path[4] == "path"
        )
        return (direct_source or object_source) and _external_book_source(value)
    if rel == Path("13_BOOKS/manifesto/MANIFESTO_BOOK_1_BUILD.json"):
        return (
            len(path) == 3
            and path[0] == "claim_card_sets"
            and isinstance(path[1], int)
            and path[2] == "source"
            and _external_book_source(value)
        )
    if rel == Path(
        "13_BOOKS/manifesto/MANIFESTO_BOOK_1_PARAGRAPH_LEDGER.json"
    ):
        return (
            len(path) == 5
            and path[0] == "paragraphs"
            and isinstance(path[1], int)
            and path[2] == "source_revisions"
            and isinstance(path[3], int)
            and path[4] == "source_path"
            and _external_book_source(value)
        )
    return False


def scan_structured_json(path: Path, rel: Path) -> list[str]:
    try:
        document = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_reject_duplicate_json_keys,
        )
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        return [f"{rel}: malformed structured non-semantic JSON: {exc}"]

    errors: list[str] = []
    for kind, json_path, value in _walk_json_strings(document):
        allowed = _structured_json_string_allowed(
            rel, kind, json_path, value
        )
        location = ".".join(str(part) for part in json_path)
        for match in FORBIDDEN.finditer(value):
            if not allowed:
                errors.append(
                    f"{rel}:{location}: forbidden authority token {match.group(0)!r}"
                )
        application_match = FORBIDDEN_APPLICATION_CLAIMS.search(value)
        if application_match and not allowed:
            errors.append(
                f"{rel}:{location}: retired application claim "
                f"{application_match.group(0)!r}"
            )
        if "Egregorotype" in value and not allowed:
            errors.append(
                f"{rel}:{location}: unmarked legacy spelling 'Egregorotype'"
            )
    return errors


_BOOK_SOURCE_REVISION = re.compile(
    r"- \*\*Source (?:revision|custody):\*\* "
    r"`(?P<path>(?:\.\./)+02_SKYZAI/[A-Za-z0-9_./-]+\.md)` "
    r"at reviewed SHA-256 `[0-9a-f]{64}`\."
)
_BOOK_HISTORICAL_SOURCE = re.compile(
    r"- \*\*Historical source:\*\* "
    r"`(?P<path>(?:\.\./)+02_SKYZAI/[A-Za-z0-9_./-]+\.md)`; "
    r"\*\*lifecycle:\*\* `frozen`; "
    r"\*\*reviewed SHA-256:\*\* `[0-9a-f]{64}`\."
)


def _book_projection_locator_line(
    rel: Path, lines: list[str], line_no: int
) -> bool:
    if rel != Path("13_BOOKS/manifesto/MANIFESTO_BOOK_1.md"):
        return False
    line = lines[line_no - 1].strip()
    for pattern in (_BOOK_SOURCE_REVISION, _BOOK_HISTORICAL_SOURCE):
        match = pattern.fullmatch(line)
        if match and _external_book_source(match.group("path")):
            return True
    bare = re.fullmatch(
        r"`(?P<path>(?:\.\./)+02_SKYZAI/[A-Za-z0-9_./-]+\.md)`\.", line
    )
    return (
        line_no >= 2
        and lines[line_no - 2].strip() == "**Historical source:**"
        and bare is not None
        and _external_book_source(bare.group("path"))
    )


def _structured_external_markdown_locator_line(
    rel: Path, lines: list[str], line_no: int
) -> bool:
    contract = STRUCTURED_EXTERNAL_SOURCE_MARKDOWN_FIELDS.get(rel)
    if contract is None or line_no < 2:
        return False
    field, expected_source_path = contract
    try:
        frontmatter_end = lines.index("---", 1)
    except ValueError:
        return False
    if line_no - 1 >= frontmatter_end:
        return False
    line = lines[line_no - 1].strip()
    return (
        _external_book_source(expected_source_path)
        and line == f"{field} {expected_source_path}"
    )


def non_semantic_boundary_errors() -> list[str]:
    """Verify every dedicated artifact still earns its narrower scope."""

    errors: list[str] = []
    if set(EXTERNAL_MAPPING_AUDIT_SHA256) != EXTERNAL_MAPPING_AUDIT_PATHS:
        errors.append("external-mapping audit digest inventory differs from path inventory")
    if set(EXACT_FILENAME_REFERENCE_UNIT_SHA256) != set(
        EXACT_FILENAME_REFERENCE_NAMES
    ):
        errors.append("exact filename-reference unit inventory differs from path inventory")
    for rel, expected in sorted(
        EXACT_FILENAME_REFERENCE_UNIT_SHA256.items(), key=lambda item: str(item[0])
    ):
        problem = scoped_file_problem(rel, "exact filename-reference source")
        if problem is not None:
            errors.append(problem)
            continue
        observed = exact_filename_reference_unit_hashes(
            rel, (ROOT / rel).read_text(encoding="utf-8")
        )
        if observed != tuple(sorted(expected)):
            errors.append(f"exact filename-reference unit inventory drift: {rel}")
    for rel, expected in sorted(
        EXTERNAL_MAPPING_AUDIT_SHA256.items(), key=lambda item: str(item[0])
    ):
        problem = dedicated_path_problem(rel)
        if problem is not None:
            errors.append(problem)
            continue
        path = ROOT / rel
        if raw_sha256(path) != expected:
            errors.append(f"external-mapping audit digest drift: {rel}")
    invalid_dedicated: set[Path] = set()
    for rel in sorted(DEDICATED_PURITY_PATHS, key=str):
        problem = dedicated_path_problem(rel)
        if problem is not None:
            errors.append(problem)
            invalid_dedicated.add(rel)
    for rel, expected in sorted(FROZEN_TOOLING_SHA256.items(), key=lambda item: str(item[0])):
        if rel in invalid_dedicated:
            continue
        path = ROOT / rel
        if raw_sha256(path) != expected:
            errors.append(f"frozen tooling digest drift: {rel}")
    for rel, expected in sorted(
        FROZEN_PROVENANCE_SHA256.items(), key=lambda item: str(item[0])
    ):
        if rel in invalid_dedicated:
            continue
        path = ROOT / rel
        if raw_sha256(path) != expected:
            errors.append(f"frozen provenance digest drift: {rel}")
    for rel, expected in sorted(
        REVIEWED_PROJECTION_HISTORY_SHA256.items(), key=lambda item: str(item[0])
    ):
        if rel in invalid_dedicated:
            continue
        if raw_sha256(ROOT / rel) != expected:
            errors.append(f"reviewed projection/history digest drift: {rel}")
    for source, (_, target, _) in sorted(
        EXACT_ARCHIVE_PROVENANCE_LINKS.items(), key=lambda item: str(item[0])
    ):
        if target not in REVIEWED_PROJECTION_HISTORY_SHA256:
            errors.append(
                f"archive provenance target lacks exact-byte custody: {source} -> {target}"
            )
    self_checker = ROOT / SELF_VALIDATED_TOOLING_PATH
    if (
        SELF_VALIDATED_TOOLING_PATH not in invalid_dedicated
        and not semantic_unit_inventory_matches(
            self_checker, SELF_CHECKER_UNIT_SHA256
        )
    ):
        errors.append(
            f"self-validated tooling semantic-unit drift: {SELF_VALIDATED_TOOLING_PATH}"
        )
    errors.extend(managed_agent_projection_errors())
    errors.extend(distillation_projection_errors())
    for rel, expected in sorted(
        STRUCTURED_TOOLING_UNIT_SHA256.items(), key=lambda item: str(item[0])
    ):
        if rel in invalid_dedicated:
            continue
        path = ROOT / rel
        observed = [
            semantic_unit_sha256(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if purity_sensitive_line(line)
        ]
        if len(observed) != len(expected) or set(observed) != set(expected):
            errors.append(f"structured tooling semantic-unit drift: {rel}")
    if set(ROSETTA_CROSSWALK_UNIT_SHA256) != set(
        ROSETTA_CROSSWALK_BOUNDARY_CONTRACTS
    ):
        errors.append("Rosetta crosswalk unit inventory differs from boundaries")
    for rel, expected in sorted(
        ROSETTA_CROSSWALK_UNIT_SHA256.items(), key=lambda item: str(item[0])
    ):
        if rel in invalid_dedicated:
            continue
        path = ROOT / rel
        observed = [
            semantic_unit_sha256(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if purity_sensitive_line(line)
            and semantic_unit_sha256(line) not in (
                HISTORICAL_PROVENANCE_UNIT_SHA256.get(rel) or frozenset()
            )
        ]
        if len(observed) != len(expected) or set(observed) != set(expected):
            errors.append(f"Rosetta crosswalk semantic-unit drift: {rel}")
        text = path.read_text(encoding="utf-8")
        for phrase in ROSETTA_CROSSWALK_BOUNDARY_CONTRACTS[rel]:
            if phrase not in text:
                errors.append(
                    f"Rosetta crosswalk boundary {rel} missing phrase: {phrase!r}"
                )
    for rel, expected in sorted(
        HISTORICAL_PROVENANCE_UNIT_SHA256.items(), key=lambda item: str(item[0])
    ):
        path = ROOT / rel
        problem = scoped_file_problem(rel, "historical provenance unit")
        if problem is not None:
            errors.append(problem)
            continue
        observed = [
            semantic_unit_sha256(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if semantic_unit_sha256(line) in expected
        ]
        if len(observed) != len(expected) or set(observed) != set(expected):
            errors.append(f"historical provenance semantic-unit drift: {rel}")
    if set(CONTROL_PROJECTION_UNIT_SHA256) != set(CONTROL_PROJECTION_PATHS):
        errors.append("control-projection semantic-unit inventory differs from paths")
    for rel, expected in sorted(
        CONTROL_PROJECTION_UNIT_SHA256.items(), key=lambda item: str(item[0])
    ):
        path = ROOT / rel
        problem = scoped_file_problem(rel, "control projection")
        if problem is not None:
            errors.append(problem)
            continue
        observed = [
            semantic_unit_sha256(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if purity_sensitive_line(line)
        ]
        if len(observed) != len(expected) or set(observed) != set(expected):
            errors.append(f"control-projection semantic-unit drift: {rel}")
    for rel, phrases in NON_SEMANTIC_BOUNDARY_CONTRACTS.items():
        if rel in invalid_dedicated:
            continue
        path = ROOT / rel
        problem = scoped_file_problem(rel, "non-semantic boundary")
        if problem is not None:
            errors.append(problem)
            continue
        text = path.read_text(encoding="utf-8")
        for phrase in phrases:
            if phrase not in text:
                errors.append(
                    f"non-semantic boundary {rel} missing phrase: {phrase!r}"
                )
    if set(HISTORICAL_INLINE_EXACT_SOURCE_PATHS) != set(
        HISTORICAL_INLINE_SOURCE_PATHS
    ):
        errors.append("historical-inline source inventory differs from boundaries")
    for rel, phrases in HISTORICAL_INLINE_SOURCE_PATHS.items():
        path = ROOT / rel
        problem = scoped_file_problem(rel, "historical-inline boundary")
        if problem is not None:
            errors.append(problem)
            continue
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        for phrase in phrases:
            if phrase not in text:
                errors.append(
                    f"historical-inline boundary {rel} missing phrase: {phrase!r}"
                )
        matches = [
            line_no
            for line_no in range(1, len(lines) + 1)
            if is_historical_inline_source_path(rel, lines, line_no)
        ]
        if len(matches) != 1:
            errors.append(
                f"historical-inline boundary {rel} lacks its exact source locator"
            )
    for rel in sorted(HISTORICAL_LINEAGE_CARD_PATHS, key=str):
        path = ROOT / rel
        problem = scoped_file_problem(rel, "historical-lineage card")
        if problem is not None:
            errors.append(problem)
            continue
        if historical_lineage_source_line(path.read_text(encoding="utf-8"), rel) is None:
            errors.append(
                f"historical-lineage card {rel} lacks one valid frozen source.path record"
            )
    for rel in sorted(STRUCTURED_EXTERNAL_SOURCE_MARKDOWN_FIELDS, key=str):
        path = ROOT / rel
        problem = scoped_file_problem(rel, "structured external-source Markdown")
        if problem is not None:
            errors.append(problem)
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        matches = [
            line_no
            for line_no in range(1, len(lines) + 1)
            if _structured_external_markdown_locator_line(rel, lines, line_no)
        ]
        if len(matches) != 1:
            errors.append(
                f"structured external-source Markdown {rel} lacks its exact locator"
            )
    return errors


def scan_file(
    path: Path,
    *,
    allow_legacy_alias: bool = False,
    receipt_target_names: tuple[str, ...] | None = None,
) -> list[str]:
    errors: list[str] = []
    try:
        rel = path.relative_to(ROOT)
    except ValueError:
        return [f"scoped path is outside corpus root: {path}"]
    symlink = first_symlink_component(path)
    if symlink is not None:
        return [f"scoped path {rel} crosses symlink component: {symlink}"]
    if rel in DEDICATED_PURITY_PATHS or rel in EXTERNAL_MAPPING_AUDIT_PATHS:
        problem = dedicated_path_problem(rel)
        if problem is not None:
            return [problem]
    if not path.is_file():
        return [f"missing scoped file: {rel}"]
    if rel in FROZEN_TOOLING_SHA256:
        expected = FROZEN_TOOLING_SHA256[rel]
        actual = raw_sha256(path)
        if actual != expected:
            return [
                f"{rel}: frozen tooling digest drift: expected {expected}, got {actual}"
            ]
        return []
    if rel in FROZEN_PROVENANCE_SHA256:
        expected = FROZEN_PROVENANCE_SHA256[rel]
        actual = raw_sha256(path)
        if actual != expected:
            return [
                f"{rel}: frozen provenance digest drift: "
                f"expected {expected}, got {actual}"
            ]
        return []
    if rel in REVIEWED_PROJECTION_HISTORY_SHA256:
        expected = REVIEWED_PROJECTION_HISTORY_SHA256[rel]
        actual = raw_sha256(path)
        if actual != expected:
            return [
                f"{rel}: reviewed projection/history digest drift: "
                f"expected {expected}, got {actual}"
            ]
        return []
    if rel in MANAGED_AGENT_PROJECTION_SHA256:
        expected = MANAGED_AGENT_PROJECTION_SHA256[rel]
        actual = raw_sha256(path)
        if actual != expected:
            return [
                f"{rel}: managed-agent projection digest drift: "
                f"expected {expected}, got {actual}"
            ]
        return []
    if rel in DISTILLATION_PROJECTION_SHA256:
        expected = DISTILLATION_PROJECTION_SHA256[rel]
        actual = raw_sha256(path)
        if actual != expected:
            return [
                f"{rel}: distillation projection digest drift: "
                f"expected {expected}, got {actual}"
            ]
        return []
    if (
        rel in STRUCTURED_DIAGNOSTIC_PATHS
        or rel in STRUCTURED_EXTERNAL_SOURCE_JSON_PATHS
        or rel in {
        Path("13_BOOKS/manifesto/MANIFESTO_BOOK_1_BUILD.json"),
        Path("13_BOOKS/manifesto/MANIFESTO_BOOK_1_PARAGRAPH_LEDGER.json"),
        }
    ):
        return scan_structured_json(path, rel)
    if receipt_target_names is None:
        try:
            receipt_target_names = physical_receipt_target_names(ROOT)
        except ValueError as exc:
            return [f"receipt target inventory invalid: {exc}"]
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    errors.extend(exact_archive_provenance_link_errors(rel, text))
    if rel == SELF_VALIDATED_TOOLING_PATH and not semantic_unit_inventory_matches(
        path, SELF_CHECKER_UNIT_SHA256
    ):
        errors.append(f"{rel}: self-validated tooling semantic-unit drift")
    # An external-mapping audit keeps its exemption only while it carries the boundary.
    # Checked ONCE per file, before any line is scanned, so a file that has quietly lost
    # its declaration fails immediately rather than scanning clean on an exemption it no
    # longer earns.
    if rel in EXTERNAL_MAPPING_AUDIT_PATHS:
        required = EXTERNAL_MAPPING_BOUNDARY_PHRASES
        if rel in EXTERNAL_MAPPING_AUDIT_TYPE_PATHS:
            required = (*required, EXTERNAL_MAPPING_AUDIT_TYPE)
        missing = [p for p in required if p not in text]
        if missing:
            errors.append(
                f"{rel}: listed as an external-mapping audit but its boundary declaration is "
                f"incomplete — missing {missing!r}. Either restore the declaration verbatim or "
                f"remove the file from EXTERNAL_MAPPING_AUDIT_PATHS and strip the external names."
            )
        expected = EXTERNAL_MAPPING_AUDIT_SHA256.get(rel)
        actual = raw_sha256(path)
        if expected is None:
            errors.append(f"{rel}: external-mapping audit has no reviewed digest")
        elif actual != expected:
            errors.append(
                f"{rel}: external-mapping audit digest drift: expected {expected}, got {actual}"
            )
        return errors

    historical_source_line = historical_lineage_source_line(text, rel)
    for line_no, line in enumerate(lines, 1):
        historical_source_record = line_no == historical_source_line
        structured_tooling_unit = semantic_unit_sha256(line) in (
            STRUCTURED_TOOLING_UNIT_SHA256.get(rel) or frozenset()
        )
        self_checker_unit = (
            rel == SELF_VALIDATED_TOOLING_PATH
            and semantic_unit_sha256(line) in SELF_CHECKER_UNIT_SHA256
        )
        control_projection_unit = semantic_unit_sha256(line) in (
            CONTROL_PROJECTION_UNIT_SHA256.get(rel) or frozenset()
        )
        rosetta_crosswalk_unit = semantic_unit_sha256(line) in (
            ROSETTA_CROSSWALK_UNIT_SHA256.get(rel) or frozenset()
        )
        historical_provenance_unit = semantic_unit_sha256(line) in (
            HISTORICAL_PROVENANCE_UNIT_SHA256.get(rel) or frozenset()
        )
        book_projection_locator = _book_projection_locator_line(
            rel, lines, line_no
        )
        structured_external_locator = _structured_external_markdown_locator_line(
            rel, lines, line_no
        )
        for match in FORBIDDEN.finditer(line):
            if not (
                historical_source_record
                or structured_tooling_unit
                or self_checker_unit
                or control_projection_unit
                or rosetta_crosswalk_unit
                or historical_provenance_unit
                or book_projection_locator
                or structured_external_locator
                or forbidden_match_is_control_projection_reference(
                    rel, line, match
                )
                or is_historical_inline_source_path(rel, lines, line_no)
                or forbidden_match_is_root_filename_reference(rel, line, match)
                or forbidden_match_is_exact_receipt_target(
                    line, match, receipt_target_names
                )
            ):
                errors.append(
                    f"{path.relative_to(ROOT)}:{line_no}: forbidden authority token {match.group(0)!r}"
                )
        application_match = FORBIDDEN_APPLICATION_CLAIMS.search(line)
        if (
            application_match
            and not structured_tooling_unit
            and not self_checker_unit
        ):
            errors.append(
                f"{path.relative_to(ROOT)}:{line_no}: retired application claim "
                f"{application_match.group(0)!r}"
            )
        if (
            "Egregorotype" in line
            and not allow_legacy_alias
            and not structured_tooling_unit
            and not self_checker_unit
        ):
            errors.append(
                f"{path.relative_to(ROOT)}:{line_no}: unmarked legacy spelling 'Egregorotype'"
            )
    return errors


def main() -> int:
    errors: list[str] = active_tree_symlink_errors()
    scoped = [ROOT / p for p in FRONT_DOORS + OWNERS]
    scoped.extend(ROOT / p for p in CONTROL_PROJECTION_PATHS)
    scoped.extend(ROOT / p for p in sorted(DEDICATED_PURITY_PATHS, key=str))
    scoped.extend(p for p in ROOT.rglob("*") if p.is_file() and is_active_route(p))
    scoped.extend(p for p in ROOT.rglob("*") if p.is_file() and is_active_corpus_file(p))

    seen: set[Path] = set()
    try:
        receipt_target_names = physical_receipt_target_names(ROOT)
    except ValueError as exc:
        errors.append(f"receipt target inventory invalid: {exc}")
        receipt_target_names = ()
    for path in scoped:
        if path in seen:
            continue
        seen.add(path)
        allow_alias = path.relative_to(ROOT) in LEGACY_ALIAS_EXCEPTIONS
        errors.extend(
            scan_file(
                path,
                allow_legacy_alias=allow_alias,
                receipt_target_names=receipt_target_names,
            )
        )

    boundary_rel = MANAGED_AGENT_PROJECTION_ROOT / "README.md"
    boundary = ROOT / boundary_rel
    boundary_problem = dedicated_path_problem(boundary_rel)
    if boundary_problem is not None:
        errors.append(boundary_problem)
    else:
        boundary_text = boundary.read_text(encoding="utf-8")
        for phrase in (
            "runtime projection, not worldview doctrine",
            "creates no semantic authority",
            "source owners remain upstream",
        ):
            if phrase not in boundary_text:
                errors.append(
                    "projection boundary "
                    f"{MANAGED_AGENT_PROJECTION_ROOT}/README.md "
                    f"missing phrase: {phrase!r}"
                )

    for rel in CONTROL_PROJECTION_PATHS:
        control_projection = ROOT / rel
        problem = scoped_file_problem(rel, "control projection")
        if problem is not None:
            errors.append(problem)
            continue
        control_text = control_projection.read_text(encoding="utf-8")
        for phrase in (
            'semantic_authority: "none"',
            "creates no theorem, ontology, axiology",
            "or eighth kernel owner",
            "biological correspondences are optional `[I]` Rosetta annotations",
        ):
            if phrase not in control_text:
                errors.append(
                    f"control projection {rel} missing phrase: {phrase!r}"
                )

    for rel in APPLICATION_TOMBSTONES:
        path = ROOT / rel
        problem = scoped_file_problem(rel, "application forwarding tombstone")
        if problem is not None:
            errors.append(problem)
            continue
        text = path.read_text(encoding="utf-8")
        if "ARCHIVED" not in text and "SUPERSEDED" not in text:
            errors.append(f"application path is not marked archived/superseded: {rel}")
        if len(text.splitlines()) > 90:
            errors.append(f"application forwarding tombstone regrew into an active body: {rel}")

    for rel in REQUIRED_READER_SURFACES:
        problem = scoped_file_problem(rel, "lived Weltanschauung reader surface")
        if problem is not None:
            errors.append(problem)

    for rel in LIVED_TOMBSTONES:
        path = ROOT / rel
        problem = scoped_file_problem(rel, "lived-synthesis forwarding tombstone")
        if problem is not None:
            errors.append(problem)
            continue
        text = path.read_text(encoding="utf-8")
        if "ARCHIVED" not in text:
            errors.append(f"lived-synthesis path is not marked archived: {rel}")
        if len(text.splitlines()) > 45:
            errors.append(f"lived-synthesis tombstone regrew into an active body: {rel}")

    errors.extend(required_archive_custody_errors())

    errors.extend(non_semantic_boundary_errors())

    # The historical Record is exempt from vocabulary scanning, but it must
    # state the current non-authority boundary prominently.
    record = ROOT / "11_UPLINK/50_AUDITS_AND_EXECUTIONS/00_THE_RECORD_LEDGER.md"
    record_rel = record.relative_to(ROOT)
    problem = scoped_file_problem(record_rel, "record boundary")
    if problem is not None:
        errors.append(problem)
    else:
        record_text = record.read_text(encoding="utf-8")
        required = (
            "Historical labels remain",
            "create no present work authority",
            "money and legal contracts",
        )
        for phrase in required:
            if phrase not in record_text:
                errors.append(f"record boundary missing phrase: {phrase!r}")

    if errors:
        print("EMERGENTISM PURITY: FAIL")
        for error in errors:
            print(error)
        return 1

    print(f"EMERGENTISM PURITY: PASS ({len(seen)} active files scanned)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
