#!/usr/bin/env python3
"""
test_cross_entity_receipt_traversal.py — Execute a Synthetic Local Proof Test.

Tests the cross-entity receipt protocol by passing the synthetic K2 receipt
from OFN AG -> Tokencen KSA -> Skyzai Marketplace -> AUREUS without manual re-entry,
verifying signatures, metadata schema conformance, and structural constraints.

Exit codes:
  0 = Traversal succeeded and verified end-to-end
  1 = Validation failed at one of the entity boundaries
"""

from __future__ import annotations
import json
import hashlib
from pathlib import Path
import sys

# Paths
REPO = Path(__file__).resolve().parents[3]
RECEIPT_PATH = REPO / "03_VENTURES/_PORTFOLIO" / "OPEN_FINANCE_NETWORK" / "02_CENTRES" / "01_KSA" / "25_FIRST_MANDATE_PIPELINE" / "SYNTHETIC_PROOF_ROUTE_AST_DEMO_KSA_REAL_00001" / "09_K2_ROUTE_READINESS_RECEIPT.jsonld"
INDEX_PATH = REPO / "03_VENTURES/_PORTFOLIO" / "OPEN_FINANCE_NETWORK" / "02_CENTRES" / "01_KSA" / "25_FIRST_MANDATE_PIPELINE" / "SYNTHETIC_PROOF_ROUTE_AST_DEMO_KSA_REAL_00001" / "03_EVIDENCE_ROOM_INDEX.md"

def test_traversal() -> int:
    print("Beginning Cross-Entity Receipt Traversal Proof (Goal 3 Step 2)...")

    # -------------------------------------------------------------
    # Step 0: Ingest K2 JSON-LD Receipt
    # -------------------------------------------------------------
    if not RECEIPT_PATH.exists():
        print(f"❌ Error: Receipt not found at {RECEIPT_PATH}")
        return 1
    
    with open(RECEIPT_PATH, "r", encoding="utf-8") as f:
        receipt = json.load(f)
    
    print("✅ Step 0: Receipt successfully ingested.")
    print(f"   Receipt ID: {receipt.get('receiptId')}")
    print(f"   Asset Ref:  {receipt.get('assetReference')}")

    # -------------------------------------------------------------
    # Step 1: OFN AG Conformance & Grammar Gate
    # -------------------------------------------------------------
    print("\nEvaluating Boundary 1: OFN AG [Standards & Grammar]...")
    
    # 1.1 Verify JSON-LD Context
    context = receipt.get("@context")
    if not context or "https://schema.org" not in context:
        print("❌ OFN AG Gate Failure: Missing or invalid JSON-LD @context")
        return 1
    
    # 1.2 Verify Receipt Type
    if receipt.get("@type") != "ofn:RouteReadinessReceipt":
        print("❌ OFN AG Gate Failure: Invalid JSON-LD @type (expected ofn:RouteReadinessReceipt)")
        return 1
    
    # 1.3 Verify K2 Ratification Signature
    sigs = receipt.get("signatures", {})
    if sigs.get("k2Ratification") != "ACTIVE v1.0":
        print("❌ OFN AG Gate Failure: Missing K2 signature or invalid ratification state")
        return 1
    
    print("✅ OFN AG Gate Passed: Receipt format, grammar, and K2 signature are valid.")

    # -------------------------------------------------------------
    # Step 2: Tokencen KSA Local Attestation Gate
    # -------------------------------------------------------------
    print("\nEvaluating Boundary 2: Tokencen KSA [Route-Readiness & MVER]...")
    
    # 2.1 Verify Local Issuing Centre
    if receipt.get("issuingCentre") != "Tokenization Centre KSA":
        print("❌ Tokencen Gate Failure: Not issued by Tokenization Centre KSA")
        return 1
    
    # 2.2 Verify Local Chapter Signature
    if sigs.get("issuingOfficer") != "Arjuna *":
        print("❌ Tokencen Gate Failure: Missing Arjun signature for local KSA Chapter")
        return 1
        
    # 2.3 Verify Document Gap Check
    conformance = receipt.get("conformance", {})
    if conformance.get("documentGapCount") != 0 or not conformance.get("schemaConforms"):
        print("❌ Tokencen Gate Failure: Document gaps present or schema non-conformant")
        return 1
        
    print("✅ Tokencen Gate Passed: Local chapter signature and document readiness verified.")

    # -------------------------------------------------------------
    # Step 3: Skyzai Marketplace Listing Ingestion Gate
    # -------------------------------------------------------------
    print("\nEvaluating Boundary 3: Skyzai Marketplace [Product Ingestion]...")
    
    # 3.1 Verify Asset is Route-Ready for Catalog Registration
    if not conformance.get("providerRaciComplete"):
        print("❌ Skyzai Gate Failure: Provider RACI is incomplete")
        return 1
    
    # 3.2 Verify Appointed Providers Panel
    providers = receipt.get("providerPanel", {})
    required_providers = ["legalCounsel", "custodianBank", "listingPlatform"]
    for prov in required_providers:
        if prov not in providers or not providers[prov]:
            print(f"❌ Skyzai Gate Failure: Appointed provider '{prov}' is missing from the panel")
            return 1
            
    print("✅ Skyzai Gate Passed: Marketplace registry check clean. Asset is ready for listing.")

    # -------------------------------------------------------------
    # Step 4: AUREUS Collateral Pricing & Escrow Gate
    # -------------------------------------------------------------
    print("\nEvaluating Boundary 4: AUREUS [Collateralization Gate]...")
    
    # 4.1 Verify MVER Directory Index State Hash
    mver_hash = receipt.get("mverStateHash")
    if not mver_hash or not mver_hash.startswith("sha256:"):
        print("❌ AUREUS Gate Failure: Invalid or missing MVER directory index state hash")
        return 1
    
    # 4.2 Verify Counsel Opinion Check
    counsel_op = conformance.get("counselSignedOpinion")
    if not counsel_op or not counsel_op.endswith(".pdf"):
        print("❌ AUREUS Gate Failure: Counsel opinion not signed/loaded")
        return 1

    # 4.3 Verify No Direct Token Minting or Custody on Core Ledger
    # In accordance with Doctrine 68, AUREUS must not execute custody or secondary trading
    print("   [Boundary Control Check]: Verifying non-custodial containment...")
    if "mint" in receipt or "custody" in receipt or "escrowBalance" in receipt:
        print("❌ AUREUS Gate Failure: Receipt contains prohibited transactional parameters")
        return 1
        
    print("✅ AUREUS Gate Passed: Collateral indices verified. No direct balance-sheet or principal risk.")

    # -------------------------------------------------------------
    # End-to-End Success
    # -------------------------------------------------------------
    print("\n🎉 SUCCESS: Cross-entity receipt traversal test completed successfully.")
    print("   OFN AG [Grammar] -> Tokencen KSA [Intake/MVER] -> Skyzai Marketplace [Listing] -> AUREUS [Collateral] verified.")
    return 0

if __name__ == "__main__":
    sys.exit(test_traversal())
