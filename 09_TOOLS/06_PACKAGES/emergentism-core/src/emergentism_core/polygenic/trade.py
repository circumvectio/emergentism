"""Inter-DAC trade theory: receipts, comparative advantage, and specialisation maps.

Trade is the selective pressure that drives economic specialisation. Each trade
receipt records not just the transaction but the economic specialisation that
made it possible. Over time, receipts build a comparative advantage map.

Key concepts:
  - Comparative advantage: Φ×ν efficiency differential between DACs
  - Specialisation receipt: FLOW receipt augmented with economic genotype data
  - Trade fitness: API_PAY volume / total ecosystem output
  - Opportunity cost: what a DAC gives up by producing one service vs. another
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .genotype import EconomicBlock


# ─────────────────────────────────────────────────────────────────────────────
# TRADE RECEIPT
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class TradeReceipt:
    receipt_id: str
    buyer_dac: str
    seller_dac: str
    buyer_chapter: str
    seller_chapter: str
    service_type: str
    currency: str  # API_PAY, SKY, ZAI, PRISM, QST
    amount: float
    timestamp: str

    # Economic specialisation at time of trade
    seller_economic: Optional[EconomicBlock] = None
    buyer_economic: Optional[EconomicBlock] = None

    # Comparative advantage basis
    seller_phi_nu: float = 0.0
    buyer_phi_nu_alternative: float = 0.0
    opportunity_cost_ratio: float = 0.0

    # Constitutional checks
    eta_check: str = "pending"  # pass | fail | pending
    k2_buyer: str = ""
    k2_seller: str = ""

    # Metadata
    notes: str = ""

    def to_dict(self) -> dict:
        return {
            "receipt_id": self.receipt_id,
            "buyer_dac": self.buyer_dac,
            "seller_dac": self.seller_dac,
            "buyer_chapter": self.buyer_chapter,
            "seller_chapter": self.seller_chapter,
            "service_type": self.service_type,
            "currency": self.currency,
            "amount": self.amount,
            "timestamp": self.timestamp,
            "seller_economic": self.seller_economic.to_dict() if self.seller_economic else None,
            "buyer_economic": self.buyer_economic.to_dict() if self.buyer_economic else None,
            "seller_phi_nu": self.seller_phi_nu,
            "buyer_phi_nu_alternative": self.buyer_phi_nu_alternative,
            "opportunity_cost_ratio": self.opportunity_cost_ratio,
            "eta_check": self.eta_check,
            "k2_buyer": self.k2_buyer,
            "k2_seller": self.k2_seller,
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "TradeReceipt":
        seller_econ = None
        if d.get("seller_economic"):
            seller_econ = EconomicBlock.from_dict(d["seller_economic"])
        buyer_econ = None
        if d.get("buyer_economic"):
            buyer_econ = EconomicBlock.from_dict(d["buyer_economic"])
        return cls(
            receipt_id=d["receipt_id"],
            buyer_dac=d["buyer_dac"],
            seller_dac=d["seller_dac"],
            buyer_chapter=d["buyer_chapter"],
            seller_chapter=d["seller_chapter"],
            service_type=d["service_type"],
            currency=d["currency"],
            amount=d["amount"],
            timestamp=d["timestamp"],
            seller_economic=seller_econ,
            buyer_economic=buyer_econ,
            seller_phi_nu=d.get("seller_phi_nu", 0.0),
            buyer_phi_nu_alternative=d.get("buyer_phi_nu_alternative", 0.0),
            opportunity_cost_ratio=d.get("opportunity_cost_ratio", 0.0),
            eta_check=d.get("eta_check", "pending"),
            k2_buyer=d.get("k2_buyer", ""),
            k2_seller=d.get("k2_seller", ""),
            notes=d.get("notes", ""),
        )


# ─────────────────────────────────────────────────────────────────────────────
# COMPARATIVE ADVANTAGE MAP
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class ComparativeAdvantageMap:
    """Aggregates trade receipts to compute who has comparative advantage in what."""

    receipts: list[TradeReceipt] = field(default_factory=list)

    def add_receipt(self, receipt: TradeReceipt):
        self.receipts.append(receipt)

    def get_advantage_for_service(self, service_type: str) -> dict[str, dict]:
        """Return {dac_id: {avg_phi_nu, trade_volume, receipt_count}} for a service."""
        service_receipts = [r for r in self.receipts if r.service_type == service_type]
        by_seller: dict[str, list[TradeReceipt]] = {}
        for r in service_receipts:
            by_seller.setdefault(r.seller_dac, []).append(r)

        result = {}
        for seller, receipts in by_seller.items():
            avg_phi_nu = sum(r.seller_phi_nu for r in receipts) / len(receipts) if receipts else 0
            total_volume = sum(r.amount for r in receipts)
            result[seller] = {
                "avg_phi_nu": round(avg_phi_nu, 4),
                "trade_volume": round(total_volume, 4),
                "receipt_count": len(receipts),
            }
        return result

    def get_all_services(self) -> list[str]:
        return sorted(set(r.service_type for r in self.receipts))

    def get_specialisation_leaderboard(self) -> dict[str, str]:
        """For each service type, return the DAC with highest avg Φ×ν."""
        leaderboard = {}
        for service in self.get_all_services():
            advantages = self.get_advantage_for_service(service)
            if advantages:
                best = max(advantages.items(), key=lambda x: x[1]["avg_phi_nu"])
                leaderboard[service] = best[0]
        return leaderboard

    def get_trade_intensity(self, dac_id: str) -> dict:
        """Compute trade intensity metrics for a DAC."""
        as_buyer = [r for r in self.receipts if r.buyer_dac == dac_id]
        as_seller = [r for r in self.receipts if r.seller_dac == dac_id]
        total_volume = sum(r.amount for r in as_buyer + as_seller)
        ecosystem_volume = sum(r.amount for r in self.receipts)

        return {
            "buyer_receipts": len(as_buyer),
            "seller_receipts": len(as_seller),
            "total_volume": round(total_volume, 4),
            "ecosystem_volume": round(ecosystem_volume, 4),
            "trade_intensity": round(total_volume / ecosystem_volume, 4) if ecosystem_volume > 0 else 0.0,
            "services_bought": list(set(r.service_type for r in as_buyer)),
            "services_sold": list(set(r.service_type for r in as_seller)),
        }

    def to_dict(self) -> dict:
        return {
            "receipt_count": len(self.receipts),
            "services": self.get_all_services(),
            "leaderboard": self.get_specialisation_leaderboard(),
            "receipts": [r.to_dict() for r in self.receipts[-50:]],  # last 50 only
        }
