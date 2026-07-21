#!/usr/bin/env python3
from pathlib import Path

BASES = [
    Path("SKYZAI_ORG/09_PWAs/skyzai_org/site/docs"),
    Path("SKYZAI_ORG/09_PWAs/skyzai_org/wiki"),
]

replacements = [
    # --- Demurrage ---
    (
        "Unstaked ZAI incurs demurrage. This is not a penalty and not destruction -- it is **redistribution**.",
        "Unstaked ZAI is targeted to incur demurrage (frozen claim until reconciliation complete). This is not a penalty and not destruction — it is **redistribution**.",
    ),
    (
        "- ZAI that is not staked (not actively participating in governance or infrastructure) gradually flows to stakers.",
        "- Target design: ZAI that is not staked (not actively participating in governance or infrastructure) would gradually flow to stakers (frozen claim until reconciliation complete).",
    ),
    (
        "- **Escape valve**: Running a SPECTRE node (contributing mesh infrastructure to the network) exempts a holder from demurrage. You participate in the organism's nervous system; the organism does not tax your holding.",
        "- **Escape valve**: Target design: running a SPECTRE node (contributing mesh infrastructure to the network) would exempt a holder from demurrage. You participate in the organism's nervous system; the organism does not tax your holding (frozen claim until reconciliation complete).",
    ),
    (
        "Land that sits idle produces nothing. ZAI demurrage ensures that equity continuously flows toward those who maintain the organism.",
        "Land that sits idle produces nothing. Target design: ZAI demurrage is intended to ensure that equity continuously flows toward those who maintain the organism (frozen claim until reconciliation complete).",
    ),
    (
        "| Demurrage | Yes (redistribute to stakers) |",
        "| Demurrage | Target design (redistribute to stakers) — frozen claim until reconciliation complete |",
    ),
    (
        "Staking ZAI activates governance rights and exempts from demurrage.",
        "Staking ZAI activates governance rights and would exempt from demurrage (frozen claim until reconciliation complete).",
    ),
    (
        "ZAI has built-in demurrage -- idle capital decays toward the Prism floor. But\nZAI staked to a SPECTRE node is not idle. It is working capital, actively\nearning routing fees. The node stake exempts that ZAI from demurrage as long\nas the node maintains minimum uptime (95%).",
        "Target design: ZAI would have built-in demurrage — idle capital would decay toward the Prism floor. ZAI staked to a SPECTRE node would not be idle. It would be working capital, actively earning routing fees. The node stake would exempt that ZAI from demurrage as long as the node maintains minimum uptime (95%) (frozen claim until reconciliation complete).",
    ),
    (
        "Running a node is not charity. It is demurrage escape -- your ZAI earns its\nkeep instead of decaying.",
        "Running a node is not charity. Target design: it would be demurrage escape — your ZAI would earn its keep instead of decaying (frozen claim until reconciliation complete).",
    ),
    (
        "This creates a clean incentive: either put your ZAI to work, or watch it decay.",
        "Target design: this would create a clean incentive: either put your ZAI to work, or watch it decay (frozen claim until reconciliation complete).",
    ),
    (
        "- Unstaked LP-100 incurs demurrage (redistribution to stakers). Active participation is expected.",
        "- Unstaked LP-100 is targeted to incur demurrage (redistribution to stakers) (frozen claim until reconciliation complete). Active participation is expected.",
    ),
    (
        "Demurrage collected is redistributed to stakers proportionally:",
        "Target design: demurrage collected would be redistributed to stakers proportionally (frozen claim until reconciliation complete):",
    ),
    (
        "- **Demurrage**: Unstaked LP-100 tokens flow to stakers. This is redistribution, not destruction. Running a SPECTRE node exempts holders from demurrage.",
        "- **Demurrage** (target design): Unstaked LP-100 tokens would flow to stakers. This is redistribution, not destruction. Running a SPECTRE node would exempt holders from demurrage (frozen claim until reconciliation complete).",
    ),
    (
        "demurrage rate (protocol constant)",
        "target demurrage rate (protocol constant)",
    ),
    (
        "Demurrage for unstaked balance `u_i`:",
        "Target design: demurrage for unstaked balance `u_i` (frozen claim until reconciliation complete):",
    ),
    # --- SKY interest flow ---
    (
        "- **Destination**: 100% of interest revenue flows to the protocol AMM (automated market maker), deepening liquidity. Interest does not enrich a treasury or a team -- it strengthens the market.",
        "- **Destination**: Target design: 100% of interest revenue would flow to the protocol AMM (automated market maker), deepening liquidity. Interest would not enrich a treasury or a team — it would strengthen the market (frozen claim until reconciliation complete).",
    ),
    (
        "| Interest destination | 100% to protocol AMM |",
        "| Interest destination | Target design: 100% to protocol AMM — frozen claim until reconciliation complete |",
    ),
    (
        "100% of Lombard Bridge interest flows to the protocol AMM, deepening liquidity for all participants. Interest does not fund a team, a treasury, or an investor. It makes the market more resilient.",
        "Target design: 100% of Lombard Bridge interest would flow to the protocol AMM, deepening liquidity for all participants. Interest would not fund a team, a treasury, or an investor. It would make the market more resilient (frozen claim until reconciliation complete).",
    ),
    # --- Lombard Bridge ---
    (
        "The Lombard Bridge enables LP-100 holders to borrow SKY by depositing their equity as collateral.",
        "Target design: The Lombard Bridge would enable LP-100 holders to borrow SKY by depositing their equity as collateral (frozen claim until reconciliation complete).",
    ),
    (
        "- **Lombard Bridge**: Deposit any LP-100 equity token as collateral, borrow SKY from willing lenders. This is credit intermediation, not monetary expansion.",
        "- **Lombard Bridge** (target design): Deposit any LP-100 equity token as collateral to borrow SKY from willing lenders. This is credit intermediation, not monetary expansion (frozen claim until reconciliation complete).",
    ),
    (
        "- **Lombard Bridge**: Any LP-100 can be deposited as collateral to borrow SKY.",
        "- **Lombard Bridge** (target design): Any LP-100 could be deposited as collateral to borrow SKY (frozen claim until reconciliation complete).",
    ),
    (
        "the Lombard Bridge, which is a **credit mechanism** (borrowing existing SKY from willing lenders).",
        "the Lombard Bridge, which is a target **credit mechanism** (borrowing existing SKY from willing lenders) (frozen claim until reconciliation complete).",
    ),
    (
        "the Lombard Bridge, which is credit (borrowing existing SKY).",
        "the Lombard Bridge, which is a target credit mechanism (borrowing existing SKY) (frozen claim until reconciliation complete).",
    ),
    (
        "Aureus: Lombard Bridge spread (cost of gold custody and collateralization)",
        "Aureus: Lombard Bridge spread (cost of gold custody and collateralization) — target design (frozen claim until reconciliation complete)",
    ),
    (
        "- Lombard Bridge liquidation",
        "- Lombard Bridge liquidation (target design)",
    ),
    (
        "## Application: Lombard Bridge Interest",
        "## Application: Lombard Bridge Interest (Target Design)",
    ),
    # --- LP-100 fixed supply ---
    (
        "- **Total supply**: 100 ZAI. Fixed forever. No minting. No burning. No inflation. No deflation.",
        "- **Total supply**: 100 ZAI. The \"fixed forever\" invariant is contradicted by the mint path in code and is a frozen claim until reconciliation complete.",
    ),
    (
        "- **Fixed supply**: 100 units per DAC. Forever. No minting beyond genesis (except Faucet dilution within the 3% cap, which redistributes, not inflates past the cap).",
        "- **Fixed supply**: 100 units per DAC. The \"forever\" invariant is contradicted by the mint path in code and is a frozen claim until reconciliation complete.",
    ),
    (
        "- **Fixed forever**: The 100-unit total cannot be changed by governance, admin keys, or protocol upgrades. It is a constant, not a parameter.",
        "- **Fixed forever**: Target design: the 100-unit total is intended to be fixed, but the \"forever\" invariant is contradicted by the mint path in code (frozen claim until reconciliation complete).",
    ),
    (
        "Total LP-100 per DAC = 100. Always. Total ZAI = 100. Always.",
        "Target design: Total LP-100 per DAC = 100 and Total ZAI = 100, but the \"forever\" invariant is contradicted by the mint path in code (frozen claim until reconciliation complete).",
    ),
    (
        "There is no inflation, no deflation, no hidden minting. Demurrage redistributes; it does not create or destroy.",
        "Target design: there would be no inflation, no deflation, no hidden minting. Demurrage would redistribute; it would not create or destroy (frozen claim until reconciliation complete).",
    ),
    (
        "- **Token conservation**: Total ZAI across all DACs is always exactly 100 per organism. No inflation, no deflation, no exceptions.",
        "- **Token conservation**: Target design: total ZAI across all DACs would be exactly 100 per organism, but the \"forever\" invariant is contradicted by the mint path in code (frozen claim until reconciliation complete).",
    ),
    (
        "| Supply | Fixed: 100 | Elastic |",
        "| Supply | Target design: fixed at 100 (frozen claim until reconciliation complete) | Elastic |",
    ),
    # --- Grace Exit ---
    (
        "- **R3 (Exit)**: Grace Exit at NAV. Always. Unconditionally. (See K4 / Grace Exit.)",
        "- **R3 (Exit)**: Grace Exit at NAV is a target design, not a live guarantee (frozen claim until reconciliation complete).",
    ),
    (
        "| R3 | Exit | Grace Exit at Net Asset Value. Always available. Unconditional. Cannot be suspended. (K4) |",
        "| R3 | Exit | Grace Exit at Net Asset Value is a target design (K4) — frozen claim until reconciliation complete |",
    ),
    (
        "Any LP-100 holder can leave at any time, for any reason, receiving their proportional share of Net Asset Value. No lock-up. No penalty. No governance approval. No waiting period. Full data export. The organism retains nothing.",
        "Target design: Any LP-100 holder would be able to leave at any time, for any reason, receiving their proportional share of Net Asset Value. No lock-up. No penalty. No governance approval. No waiting period. Full data export. The organism retains nothing (frozen claim until reconciliation complete).",
    ),
    (
        "The entire process is atomic. It completes in a single transaction or reverts entirely.",
        "Target design: the entire process would be atomic. It would complete in a single transaction or revert entirely (frozen claim until reconciliation complete).",
    ),
    (
        "There is no vesting period. There is no \"staking cooldown\" that delays exit. There is no governance vote that can suspend Grace Exit.",
        "Target design: there would be no vesting period, no \"staking cooldown\" that delays exit, and no governance vote that can suspend Grace Exit (frozen claim until reconciliation complete).",
    ),
    (
        "The exit is at NAV. Not at a discount. Not with a penalty fee. Not with a \"early exit tax.\" NAV means NAV.",
        "Target design: the exit would be at NAV. Not at a discount. Not with a penalty fee. Not with an \"early exit tax.\" NAV means NAV (frozen claim until reconciliation complete).",
    ),
    (
        "If the DAC's assets are worth 1,000 SKY and a holder owns 10 LP-100 (10%), they receive 100 SKY. Period.",
        "Target design: if the DAC's assets are worth 1,000 SKY and a holder owns 10 LP-100 (10%), they would receive 100 SKY (frozen claim until reconciliation complete).",
    ),
    (
        "- **NAV is calculated** on-chain from the DAC's treasury, receivables, and marked-to-market positions.",
        "- **NAV would be calculated** on-chain from the DAC's treasury, receivables, and marked-to-market positions (frozen claim until reconciliation complete).",
    ),
    (
        "- **SKY is transferred** to the exiting holder's wallet.",
        "- **SKY would be transferred** to the exiting holder's wallet (frozen claim until reconciliation complete).",
    ),
    (
        "- **LP-100 is returned** to the DAC (redistributed to remaining holders proportionally).",
        "- **LP-100 would be returned** to the DAC (redistributed to remaining holders proportionally) (frozen claim until reconciliation complete).",
    ),
    (
        "- **Data is exported**: All receipts, transaction history, governance votes, and personal data associated with the exiting holder are packaged and delivered.",
        "- **Data would be exported**: All receipts, transaction history, governance votes, and personal data associated with the exiting holder would be packaged and delivered (frozen claim until reconciliation complete).",
    ),
    (
        "- **Grants are revoked**: Any permissions, access rights, or delegations the holder had granted to the organism are revoked.",
        "- **Grants would be revoked**: Any permissions, access rights, or delegations the holder had granted to the organism would be revoked (frozen claim until reconciliation complete).",
    ),
    # Numbered Grace Exit items
    (
        "2. **NAV is calculated** on-chain from the DAC's treasury, receivables, and marked-to-market positions.",
        "2. **NAV would be calculated** on-chain from the DAC's treasury, receivables, and marked-to-market positions (frozen claim until reconciliation complete).",
    ),
    (
        "4. **SKY is transferred** to the exiting holder's wallet.",
        "4. **SKY would be transferred** to the exiting holder's wallet (frozen claim until reconciliation complete).",
    ),
    (
        "5. **LP-100 is returned** to the DAC (redistributed to remaining holders proportionally).",
        "5. **LP-100 would be returned** to the DAC (redistributed to remaining holders proportionally) (frozen claim until reconciliation complete).",
    ),
    (
        "6. **Data is exported**: All receipts, transaction history, governance votes, and personal data associated with the exiting holder are packaged and delivered.",
        "6. **Data would be exported**: All receipts, transaction history, governance votes, and personal data associated with the exiting holder would be packaged and delivered (frozen claim until reconciliation complete).",
    ),
    (
        "7. **Grants are revoked**: Any permissions, access rights, or delegations the holder had granted to the organism are revoked.",
        "7. **Grants would be revoked**: Any permissions, access rights, or delegations the holder had granted to the organism would be revoked (frozen claim until reconciliation complete).",
    ),
    # Numbered Lombard Bridge items
    (
        "1. **Deposit**: A borrower deposits LP-100 tokens (from any DAC) into the Lombard Bridge vault.",
        "1. **Deposit**: A borrower would deposit LP-100 tokens (from any DAC) into the Lombard Bridge vault (frozen claim until reconciliation complete).",
    ),
    (
        "2. **Borrow**: The borrower receives SKY from the lending pool -- SKY that lenders have voluntarily deposited to earn interest.",
        "2. **Borrow**: The borrower would receive SKY from the lending pool — SKY that lenders have voluntarily deposited to earn interest (frozen claim until reconciliation complete).",
    ),
    (
        "3. **Interest**: The borrower pays interest at base rate 5% * L(x), where x is pool utilization.",
        "3. **Interest**: The borrower would pay interest at base rate 5% * L(x), where x is pool utilization (frozen claim until reconciliation complete).",
    ),
    (
        "4. **Repay**: The borrower returns SKY + accrued interest to unlock their LP-100 collateral.",
        "4. **Repay**: The borrower would return SKY + accrued interest to unlock their LP-100 collateral (frozen claim until reconciliation complete).",
    ),
    (
        "5. **Liquidation**: If collateral value falls below the required ratio, the position is atomically unwound.",
        "5. **Liquidation**: If collateral value falls below the required ratio, the position would be atomically unwound (frozen claim until reconciliation complete).",
    ),
    (
        "Grace Exit pays from liquid assets first. If the DAC is undercollateralized, the exiting holder receives their pro-rata share of what exists, not a theoretical NAV.",
        "Target design: Grace Exit would pay from liquid assets first. If the DAC is undercollateralized, the exiting holder would receive their pro-rata share of what exists, not a theoretical NAV (frozen claim until reconciliation complete).",
    ),
    (
        "Grace Exit at NAV. Always.",
        "Grace Exit at NAV is a target design (frozen claim until reconciliation complete).",
    ),
    (
        "Gate C guarantees that any LP-100 holder can leave at any time, receiving their proportional share of Net Asset Value.",
        "Target design: Gate C would guarantee that any LP-100 holder can leave receiving their proportional share of Net Asset Value (frozen claim until reconciliation complete).",
    ),
    (
        "- **Unconditional**: No lock-up period. No governance approval. No waiting list. No penalty.",
        "- **Unconditional**: Target design: no lock-up period, no governance approval, no waiting list, no penalty (frozen claim until reconciliation complete).",
    ),
    (
        "- **Atomic**: The exit completes in a single transaction. LP-100 is returned, NAV share is paid in SKY.",
        "- **Atomic**: Target design: the exit would complete in a single transaction. LP-100 would be returned, NAV share paid in SKY (frozen claim until reconciliation complete).",
    ),
    (
        "Grace Exit available from day 1",
        "Target design: Grace Exit would be available from day 1 (frozen claim until reconciliation complete)",
    ),
    (
        "Positions always exitable",
        "Target design: positions would always be exitable (frozen claim until reconciliation complete)",
    ),
    (
        "The door is always open.",
        "Target design: the door would always be open (frozen claim until reconciliation complete).",
    ),
    (
        "The door always open is the door nobody walks through.",
        "Target design: the door always open is the door nobody walks through (frozen claim until reconciliation complete).",
    ),
    (
        "Grace Exit (K4). The protocol calculates NAV, divides by total LP-100, and pays the exiting holder their share.",
        "Target design: Grace Exit (K4) would calculate NAV and pay the exiting holder their share (frozen claim until reconciliation complete).",
    ),
    (
        "- **Grace Exit (K4)**: If extraction somehow emerged, any holder can exit at NAV immediately.",
        "- **Grace Exit (K4)**: Target design: if extraction somehow emerged, any holder would be able to exit at NAV immediately (frozen claim until reconciliation complete).",
    ),
    (
        "- The old DAC's Grace Exit was fully executed at dissolution.",
        "- Target design: the old DAC's Grace Exit would be fully executed at dissolution (frozen claim until reconciliation complete).",
    ),
    (
        "The old DAC's Grace Exit was fully executed at dissolution.",
        "Target design: the old DAC's Grace Exit would be fully executed at dissolution (frozen claim until reconciliation complete).",
    ),
    # Additional files found in final sweep
    (
        "- **Grace Exit (K4):** Ensures no participant is trapped at a phi/nu ratio they did not choose. [S]",
        "- **Grace Exit (K4):** Target design: ensures no participant would be trapped at a phi/nu ratio they did not choose (frozen claim until reconciliation complete). [S]",
    ),
    (
        "    ALL receive K2-signed instructions from the Trivium",
        "    Target design: all would receive K2-signed instructions from the Trivium (frozen claim until reconciliation complete).",
    ),
    (
        "    The K2 signature is the authorization",
        "    Target design: the K2 signature would be the authorization (frozen claim until reconciliation complete).",
    ),
    (
        "K2 applies at every level — the human signs, the constitution governs, or the owner authorizes within constitutional bounds. [S]",
        "Target design: K2 would apply at every level — the human would sign, the constitution would govern, or the owner would authorize within constitutional bounds (frozen claim until reconciliation complete). [S]",
    ),
    (
        "eta = 0 + Grace Exit. Users leave with everything. There is no lock-in, no switching cost, no data hostage.",
        "eta = 0 + Grace Exit (target design). Users would leave with everything. There would be no lock-in, no switching cost, no data hostage (frozen claim until reconciliation complete).",
    ),
    (
        "sovereign identity, Grace Exit always. [I]",
        "sovereign identity, Grace Exit as a target design (frozen claim until reconciliation complete). [I]",
    ),
    (
        "| ACT | ACT | HIT THE ASK (K2 sign, instant DAG settlement) |",
        "| ACT | ACT | HIT THE ASK (target design: K2 sign, instant DAG settlement — frozen claim until reconciliation complete) |",
    ),
    (
        "| ACT | ACT | YOU K2 sign, Skyzai executes via Carbon DeFi |",
        "| ACT | ACT | YOU K2 sign, Skyzai executes via Carbon DeFi (target design, frozen claim until reconciliation complete) |",
    ),
    (
        "3. **SHOULD never bypasses K2** — human signs every consequential action.",
        "3. **SHOULD never bypasses K2** — target design: human would sign every consequential action (frozen claim until reconciliation complete).",
    ),
    (
        "- **Enforcement**: Grace Exit function is always callable. Cannot be paused or gated.",
        "- **Enforcement**: Target design: Grace Exit function would always be callable and could not be paused or gated (frozen claim until reconciliation complete).",
    ),
    # --- K2 ---
    (
        "- **No delegation.** The owner signs every transaction. No agent can act without the owner's explicit approval.",
        "- **No delegation.** Target design: the owner would sign every transaction. No agent could act without the owner's explicit approval (frozen claim until reconciliation complete).",
    ),
    (
        "| Signing | Owner signs all | Multi-sig for consequential actions |",
        "| Signing | Target design: owner signs all (frozen claim until reconciliation complete) | Multi-sig for consequential actions |",
    ),
    (
        "| Agent autonomy | Zero (owner approves everything) | Within Lane A budget |",
        "| Agent autonomy | Target design: zero (owner would approve everything) — frozen claim until reconciliation complete | Within Lane A budget |",
    ),
    (
        "The human signs everything. Full sovereignty. Full responsibility.",
        "Target design: the human would sign everything. Full sovereignty. Full responsibility (frozen claim until reconciliation complete).",
    ),
    (
        "Transactions lacking any of the three substrates revert.",
        "Target design: transactions lacking any of the three substrates would revert (frozen claim until reconciliation complete).",
    ),
    (
        "4. **K2 checkpoint:** The mandatory human signature between SHOULD and ACT is the physical embodiment of Trivium separation — a gap that cannot be compiled away.",
        "4. **K2 checkpoint:** Target design: a mandatory human signature between SHOULD and ACT is the intended embodiment of Trivium separation (frozen claim until reconciliation complete).",
    ),
    (
        "Every allocation requires a wallet signature.",
        "Target design: every allocation would require a wallet signature (frozen claim until reconciliation complete).",
    ),
    # --- SPECTRE body/brain ---
    (
        "## Body / Brain Separation",
        "## Body / Brain Separation (Target Design)",
    ),
    (
        "Every SPECTRE node has two components:",
        "Target design: every SPECTRE node would have two components (frozen claim until reconciliation complete):",
    ),
    (
        "The brain fails gracefully; the body keeps working.",
        "Target design: the brain would fail gracefully; the body would keep working (frozen claim until reconciliation complete).",
    ),
    (
        "The brain makes the body faster and more resilient. If the brain fails, the body still works.",
        "Target design: the brain would make the body faster and more resilient. If the brain fails, the body would still work (frozen claim until reconciliation complete).",
    ),
    # --- ROI ---
    (
        "- **Telemetry ROI:** 1,232:1 (benefit of EBM routing vs. cost of telemetry overhead)",
        "- **Telemetry ROI:** 1,232:1 (benefit of EBM routing vs. cost of telemetry overhead) — simulation-only, frozen claim until reconciliation complete",
    ),
    (
        "## Telemetry ROI: 1,232:1",
        "## Telemetry ROI: 1,232:1 (simulation-only, frozen claim until reconciliation complete)",
    ),
    (
        "The ratio: 1,232 units of routing benefit per 1 unit of telemetry cost. The EBM pays for itself 1,232 times over.",
        "The ratio: 1,232 units of routing benefit per 1 unit of telemetry cost. This is a simulation-only figure and a frozen claim until reconciliation complete.",
    ),
    # --- Revenue projections ---
    (
        "These streams are live or near-live, independent of physical POS:",
        "These streams are target designs, not live or near-live (frozen claim until reconciliation complete):",
    ),
    (
        "## Revenue Projections by Store Count",
        "## Target Design Revenue Projections by Store Count (speculative, frozen claim until reconciliation complete)",
    ),
    (
        "These projections assume Southeast Asian market entry with average transaction values of $15-50 and PaaS subscription of $49-199/month per store.",
        "These projections are speculative target-design assumptions for Southeast Asian market entry with average transaction values of $15-50 and PaaS subscription of $49-199/month per store (frozen claim until reconciliation complete).",
    ),
    # --- Misc live claims ---
    (
        "- **Conservation (K1)**: The sum of all ZAI across all wallets always equals exactly 100. Any transaction that would violate this reverts.",
        "- **Conservation (K1)**: Target design: the sum of all ZAI across all wallets would always equal exactly 100. Any transaction that would violate this would revert (frozen claim until reconciliation complete).",
    ),
    (
        "- **Enforcement**: Any transaction that would change the sum of all LP-100 balances reverts.",
        "- **Enforcement**: Target design: any transaction that would change the sum of all LP-100 balances would revert (frozen claim until reconciliation complete).",
    ),
    (
        "This is why the equator is the operating point. Why demurrage pushes idle ZAI away from 0. Why the Faucet closes at low transparency (prevents x approaching 1). Why Grace Exit exists (escape before catastrophe).",
        "This is why the equator is the operating point. Target design: demurrage would push idle ZAI away from 0. The Faucet closes at low transparency (prevents x approaching 1). Grace Exit is a target design (escape before catastrophe).",
    ),
    (
        "- **F3 (APU -> Skyzai):** `ActionEnvelope` — K2-signed instructions with risk parameters and phi-split routing",
        "- **F3 (APU -> Skyzai):** `ActionEnvelope` — target design: K2-signed instructions with risk parameters and phi-split routing (frozen claim until reconciliation complete)",
    ),
    (
        "The user signs with K2. Skyzai executes the trade, streams SKY/second via FLOW, anchors the receipt on Arweave, and broadcasts via RELAY.",
        "The user would sign with K2 (frozen claim until reconciliation complete). Skyzai would execute the trade, stream SKY/second via FLOW, anchor the receipt on Arweave, and broadcast via RELAY (frozen claim until reconciliation complete).",
    ),
]

banner = "> **Frozen claim.** The Lombard Bridge is a target design, not a live canonical product. It currently means three incompatible things in internal documentation. The descriptions below are aspirational and subject to reconciliation.\n\n"

changed_files = []

for base in BASES:
    for path in base.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        original = text
        for old, new in replacements:
            if new in text:
                continue
            text = text.replace(old, new)
        # Inject banner into Lombard Bridge file if not already present
        if "lombard-bridge" in path.name.lower() and banner.strip() not in text:
            lines = text.splitlines()
            for i, line in enumerate(lines):
                if line.startswith("# "):
                    insert_idx = i + 1
                    if insert_idx < len(lines) and lines[insert_idx].strip() == "":
                        insert_idx += 1
                    lines.insert(insert_idx, "")
                    lines.insert(insert_idx + 1, banner.strip())
                    lines.insert(insert_idx + 2, "")
                    text = "\n".join(lines) + ("\n" if original.endswith("\n") else "")
                    break
        if text != original:
            path.write_text(text, encoding="utf-8")
            changed_files.append(str(path))

print(f"Changed {len(changed_files)} files")
for p in sorted(changed_files):
    print(p)
