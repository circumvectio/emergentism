"""MCP server for the Polygenic Economic Evolution Engine.

Exposes the living 12-dimensional genotype system as MCP tools:
  - genotype_register    — Register a DAC/chapter genotype
  - genotype_get         — Retrieve a chapter's current genotype
  - genotype_mutate      — Apply mutation operators
  - fitness_compute      — Evaluate phenotype fitness
  - ecosystem_run_cycle  — Execute one evolution generation
  - ecosystem_state      — Get full ecosystem snapshot
  - trade_record         — Record an inter-DAC trade receipt
  - trade_advantage_map  — Get comparative advantage leaderboard
  - speciation_check     — Check if a chapter is ready to speciate
  - lineage_get          — Get phylogenetic tree for a chapter

Usage:
    python -m emergentism_core.mcp_polygenic_economics

Connect with any MCP client (Claude Code, Cursor, Codex, etc.)
"""

from __future__ import annotations

import json
import logging
import sys
from pathlib import Path
from typing import Optional

logger = logging.getLogger("polygenic.mcp")

# Resolve ecosystem registry path
SCRIPT_DIR = Path(__file__).resolve().parent
REGISTRY_PATH = (
    SCRIPT_DIR.parent.parent.parent.parent.parent.parent  # up to Magnum Opus
    / "02_SKYZAI/01_NOOSPHERE/02_INFRASTRUCTURE/Cascade/08_AGENTZ_CLOUD_PWA/01_POLYGENETIC_TREE"
    / "09_POLYGENETIC_ECOSYSTEM.json"
)

# Lazy import to avoid circular deps
_ecosystem = None
_ecosystem_loaded = False


def _get_ecosystem():
    global _ecosystem, _ecosystem_loaded
    if not _ecosystem_loaded:
        from .polygenic import Ecosystem
        _ecosystem = Ecosystem.load(REGISTRY_PATH)
        _ecosystem_loaded = True
    return _ecosystem


def _save_ecosystem():
    eco = _get_ecosystem()
    eco.save(REGISTRY_PATH)


# ─────────────────────────────────────────────────────────────────────────────
# MCP TOOL HANDLERS
# ─────────────────────────────────────────────────────────────────────────────

def genotype_register(
    chapter_id: str,
    name: str,
    description: str = "",
    status: str = "ACTIVE",
    caste_L1: float = 1.0,
    caste_L2: float = 1.0,
    caste_L3: float = 1.0,
    caste_L4: float = 1.0,
    caste_L5: float = 1.0,
    caste_L6: float = 1.0,
    caste_L7: float = 1.0,
    econ_kappa: float = 0.20,
    econ_lambda: float = 0.20,
    econ_mu: float = 0.20,
    econ_rho: float = 0.20,
    econ_nu: float = 0.20,
    cluster: str = "",
    parent_chapter: str = "",
) -> str:
    """Register a new chapter with a 12-dimensional genotype.

    Args:
        chapter_id: Unique identifier (e.g., "ch01_tokencen")
        name: Human-readable name
        description: What this chapter does
        status: ACTIVE|EMERGING|PROPOSED|PLANNED|DORMANT|LATENT
        caste_L1..L7: Caste emphasis weights (0.3–2.0)
        econ_kappa..nu: Economic intensity proportions (0.0–1.0, sum≈1.0)
        cluster: Which cluster this chapter belongs to
        parent_chapter: Parent chapter ID (if speciation)
    """
    from .polygenic import Chapter, FullGenotype, CasteBlock, EconomicBlock
    from datetime import datetime, timezone

    eco = _get_ecosystem()
    if eco.get_chapter(chapter_id):
        return json.dumps({"error": f"Chapter {chapter_id} already exists"}, indent=2)

    chapter = Chapter(
        id=chapter_id,
        name=name,
        description=description,
        status=status,
        genotype=FullGenotype(
            caste=CasteBlock(L1=caste_L1, L2=caste_L2, L3=caste_L3, L4=caste_L4,
                            L5=caste_L5, L6=caste_L6, L7=caste_L7),
            economic=EconomicBlock(kappa=econ_kappa, lambda_=econ_lambda, mu=econ_mu,
                                  rho=econ_rho, nu=econ_nu),
        ),
        cluster=cluster,
        parent_chapter=parent_chapter or None,
        created_at=datetime.now(timezone.utc).isoformat(),
        last_activity=datetime.now(timezone.utc).isoformat(),
    )
    eco.add_chapter(chapter)
    _save_ecosystem()

    return json.dumps({
        "registered": chapter_id,
        "phenotype": chapter.genotype.phenotype_signature(),
        "cci": chapter.cci,
        "edi": chapter.edi,
    }, indent=2)


def genotype_get(chapter_id: str) -> str:
    """Retrieve a chapter's current 12-dimensional genotype and fitness."""
    eco = _get_ecosystem()
    ch = eco.get_chapter(chapter_id)
    if not ch:
        return json.dumps({"error": f"Chapter not found: {chapter_id}"}, indent=2)

    return json.dumps({
        "chapter": ch.id,
        "name": ch.name,
        "status": ch.status,
        "genotype": ch.genotype.to_dict(),
        "phenotype": ch.genotype.phenotype_signature(),
        "cci": ch.cci,
        "edi": ch.edi,
        "dominant_castes": ch.genotype.caste.dominant_levels(),
        "dominant_economic": ch.genotype.economic.dominant_dimensions(),
        "fitness": ch._fitness.to_dict() if ch._fitness else None,
    }, indent=2, default=str)


def genotype_mutate(
    chapter_id: str,
    mutation_types: str = "all",  # comma-separated: point,economic,cnv,factor_sub,regulatory,network
    jurisdiction_change: bool = False,
    node_count: int = 0,
) -> str:
    """Apply mutation operators to a chapter's genotype.

    Args:
        chapter_id: Target chapter
        mutation_types: Which mutation types to apply (default: all)
        jurisdiction_change: If True, apply regulatory shock
        node_count: If > threshold, apply network amplification
    """
    from .polygenic import MutationEngine
    import random

    eco = _get_ecosystem()
    ch = eco.get_chapter(chapter_id)
    if not ch:
        return json.dumps({"error": f"Chapter not found: {chapter_id}"}, indent=2)

    rng = random.Random()
    engine = MutationEngine(rng)
    types = [t.strip() for t in mutation_types.split(",")]
    events = []

    if "all" in types or "point" in types:
        events.extend(engine.point_mutation_caste(ch.genotype, ch.id))
    if "all" in types or "economic" in types:
        events.extend(engine.point_mutation_economic(ch.genotype, ch.id))
    if "all" in types or "cnv" in types:
        events.extend(engine.copy_number_variation(ch.genotype, ch.id))
    if "all" in types or "factor_sub" in types:
        events.extend(engine.factor_substitution(ch.genotype, ch.id))
    if jurisdiction_change and ("all" in types or "regulatory" in types):
        events.extend(engine.regulatory_shock(ch.genotype, ch.id, jurisdiction_change=True))
    if node_count > 0 and ("all" in types or "network" in types):
        events.extend(engine.network_amplification(ch.genotype, ch.id, node_count=node_count))

    _save_ecosystem()

    return json.dumps({
        "chapter": ch.id,
        "mutations_applied": len(events),
        "events": [e.to_dict() for e in events],
        "new_phenotype": ch.genotype.phenotype_signature(),
    }, indent=2, default=str)


def fitness_compute(chapter_id: str) -> str:
    """Compute full fitness evaluation for a chapter."""
    from .polygenic import FitnessLandscape

    eco = _get_ecosystem()
    ch = eco.get_chapter(chapter_id)
    if not ch:
        return json.dumps({"error": f"Chapter not found: {chapter_id}"}, indent=2)

    active = eco.get_active()
    competitors = [c.genotype for c in active if c.id != ch.id]
    landscape = FitnessLandscape()
    result = ch.compute_fitness(landscape=landscape, competitor_genotypes=competitors)

    return json.dumps(result.to_dict(), indent=2)


def ecosystem_run_cycle(seed: Optional[int] = None, dry_run: bool = False) -> str:
    """Execute one full biological evolution generation on the ecosystem.

    Args:
        seed: Random seed for reproducibility
        dry_run: If True, compute but don't save
    """
    import random
    from .polygenic import EvolutionCycle

    eco = _get_ecosystem()
    rng = random.Random(seed)
    cycle = EvolutionCycle(rng)
    result = cycle.run(eco)

    if not dry_run:
        _save_ecosystem()

    # Summary fitness
    fitness_values = [f.total for f in result.fitness_results.values()]
    avg_fitness = sum(fitness_values) / len(fitness_values) if fitness_values else 0

    return json.dumps({
        "generation": result.generation,
        "dry_run": dry_run,
        "summary": {
            "mutations": result.mutation_count,
            "hgt_events": result.hgt_count,
            "coevolution": result.coev_count,
            "speciations": result.speciation_count,
            "extinctions": result.extinction_count,
            "exclusion_warnings": result.excl_count,
            "avg_fitness": round(avg_fitness, 4),
        },
        "fitness_by_chapter": {
            cid: f.total for cid, f in result.fitness_results.items()
        },
        "events": result.events,
    }, indent=2, default=str)


def ecosystem_state() -> str:
    """Get full ecosystem snapshot: all chapters, trade map, generation."""
    eco = _get_ecosystem()
    active = eco.get_active()

    return json.dumps({
        "generation": eco.generation,
        "last_evolution": eco.last_evolution,
        "total_chapters": len(eco.chapters),
        "active_chapters": len(active),
        "environment": eco.environment,
        "chapters": {
            c.id: {
                "name": c.name,
                "status": c.status,
                "phenotype": c.genotype.phenotype_signature(),
                "cci": c.cci,
                "edi": c.edi,
                "fitness": c._fitness.total if c._fitness else None,
            }
            for c in eco.chapters
        },
        "trade_map": eco.trade_map.to_dict(),
    }, indent=2, default=str)


def trade_record(
    receipt_id: str,
    buyer_dac: str,
    seller_dac: str,
    service_type: str,
    currency: str,
    amount: float,
    seller_phi_nu: float = 0.0,
    buyer_phi_nu_alternative: float = 0.0,
    k2_buyer: str = "",
    k2_seller: str = "",
) -> str:
    """Record an inter-DAC trade receipt with specialisation data.

    Args:
        receipt_id: Unique receipt identifier
        buyer_dac: Buying DAC ID
        seller_dac: Selling DAC ID
        service_type: What service was traded
        currency: API_PAY, SKY, ZAI, PRISM, QST
        amount: Trade amount
        seller_phi_nu: Seller's Φ×ν for this service
        buyer_phi_nu_alternative: Buyer's Φ×ν if they did it themselves
        k2_buyer: K2 signer on buyer side
        k2_seller: K2 signer on seller side
    """
    from .polygenic import TradeReceipt
    from datetime import datetime, timezone

    eco = _get_ecosystem()
    buyer_ch = eco.get_chapter(buyer_dac)
    seller_ch = eco.get_chapter(seller_dac)

    receipt = TradeReceipt(
        receipt_id=receipt_id,
        buyer_dac=buyer_dac,
        seller_dac=seller_dac,
        buyer_chapter=buyer_dac,
        seller_chapter=seller_dac,
        service_type=service_type,
        currency=currency,
        amount=amount,
        timestamp=datetime.now(timezone.utc).isoformat(),
        seller_economic=seller_ch.genotype.economic.copy() if seller_ch else None,
        buyer_economic=buyer_ch.genotype.economic.copy() if buyer_ch else None,
        seller_phi_nu=seller_phi_nu,
        buyer_phi_nu_alternative=buyer_phi_nu_alternative,
        opportunity_cost_ratio=round(seller_phi_nu / max(buyer_phi_nu_alternative, 0.001), 4),
        eta_check="pass",  # TODO: verify η=0
        k2_buyer=k2_buyer,
        k2_seller=k2_seller,
    )
    eco.record_trade(receipt)
    _save_ecosystem()

    return json.dumps({
        "recorded": receipt_id,
        "service": service_type,
        "seller": seller_dac,
        "buyer": buyer_dac,
        "opportunity_cost_ratio": receipt.opportunity_cost_ratio,
        "comparative_advantage": "seller" if receipt.opportunity_cost_ratio > 1.2 else "neutral",
    }, indent=2)


def trade_advantage_map() -> str:
    """Get the current comparative advantage leaderboard across all services."""
    eco = _get_ecosystem()
    leaderboard = eco.trade_map.get_specialisation_leaderboard()

    # Also include per-service detail
    detail = {}
    for service in eco.trade_map.get_all_services():
        detail[service] = eco.trade_map.get_advantage_for_service(service)

    return json.dumps({
        "leaderboard": leaderboard,
        "service_detail": detail,
        "total_receipts": len(eco.trade_map.receipts),
    }, indent=2)


def speciation_check(chapter_id: str) -> str:
    """Check if a chapter meets speciation criteria."""
    eco = _get_ecosystem()
    ch = eco.get_chapter(chapter_id)
    if not ch:
        return json.dumps({"error": f"Chapter not found: {chapter_id}"}, indent=2)

    return json.dumps({
        "chapter": ch.id,
        "readiness": ch.speciation_readiness,
        "novelty_met": ch._novelty_met(),
        "design_met": ch._design_met(),
        "repeatability_met": ch._repeatability_met(),
        "novelty_events_60d": len([e for e in ch.novelty_events if e >= ch._cutoff(60)]),
        "design_events_90d": len([e for e in ch.design_requests if e >= ch._cutoff(90)]),
        "transaction_count": ch.transaction_count,
    }, indent=2)


def lineage_get(chapter_id: str) -> str:
    """Get phylogenetic lineage for a chapter (ancestors and descendants)."""
    eco = _get_ecosystem()
    ch = eco.get_chapter(chapter_id)
    if not ch:
        return json.dumps({"error": f"Chapter not found: {chapter_id}"}, indent=2)

    # Ancestors
    ancestors = []
    current = ch
    while current and current.parent_chapter:
        parent = eco.get_chapter(current.parent_chapter)
        if parent:
            ancestors.append({
                "id": parent.id,
                "name": parent.name,
                "generation": parent.generation_number,
                "depth": parent.phylogenetic_depth,
            })
            current = parent
        else:
            break

    # Descendants
    descendants = []
    for c in eco.chapters:
        if c.parent_chapter == chapter_id:
            descendants.append({
                "id": c.id,
                "name": c.name,
                "status": c.status,
                "generation": c.generation_number,
                "depth": c.phylogenetic_depth,
            })

    return json.dumps({
        "chapter": ch.id,
        "generation": ch.generation_number,
        "phylogenetic_depth": ch.phylogenetic_depth,
        "ancestors": list(reversed(ancestors)),
        "descendants": descendants,
    }, indent=2)


# ─────────────────────────────────────────────────────────────────────────────
# FastMCP Server Registration
# ─────────────────────────────────────────────────────────────────────────────

def create_polygenic_mcp_server():
    """Create a FastMCP server exposing polygenic economics tools."""
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError:
        logger.error("FastMCP not available. Install with: pip install mcp[cli]")
        return _create_manual_mcp_server()

    mcp = FastMCP(
        name="polygenic-economics",
        instructions=(
            "Polygenic Economic Evolution Engine. "
            "12-dimensional genotype (7 caste + 5 economic) with biological mutation, "
            "selection, speciation, and inter-DAC trade theory. "
            "φ · ν = 1. η = 0. K2 signs everything."
        ),
    )

    @mcp.tool()
    def polygenic_genotype_register(**kwargs) -> str:
        """Register a new chapter with 12-dimensional genotype."""
        return genotype_register(**kwargs)

    @mcp.tool()
    def polygenic_genotype_get(chapter_id: str) -> str:
        """Retrieve a chapter's genotype and fitness."""
        return genotype_get(chapter_id)

    @mcp.tool()
    def polygenic_genotype_mutate(**kwargs) -> str:
        """Apply mutation operators to a chapter."""
        return genotype_mutate(**kwargs)

    @mcp.tool()
    def polygenic_fitness_compute(chapter_id: str) -> str:
        """Compute fitness for a chapter."""
        return fitness_compute(chapter_id)

    @mcp.tool()
    def polygenic_ecosystem_run_cycle(seed: int = None, dry_run: bool = False) -> str:
        """Run one evolution generation."""
        return ecosystem_run_cycle(seed=seed, dry_run=dry_run)

    @mcp.tool()
    def polygenic_ecosystem_state() -> str:
        """Get full ecosystem snapshot."""
        return ecosystem_state()

    @mcp.tool()
    def polygenic_trade_record(**kwargs) -> str:
        """Record an inter-DAC trade receipt."""
        return trade_record(**kwargs)

    @mcp.tool()
    def polygenic_trade_advantage_map() -> str:
        """Get comparative advantage leaderboard."""
        return trade_advantage_map()

    @mcp.tool()
    def polygenic_speciation_check(chapter_id: str) -> str:
        """Check speciation readiness."""
        return speciation_check(chapter_id)

    @mcp.tool()
    def polygenic_lineage_get(chapter_id: str) -> str:
        """Get phylogenetic lineage."""
        return lineage_get(chapter_id)

    logger.info("Polygenic Economics MCP server created with 10 tools")
    return mcp


def _create_manual_mcp_server():
    """Fallback: Manual JSON-RPC over stdio."""
    logger.warning("Manual MCP mode — limited functionality")

    tools = {
        "polygenic_genotype_register": genotype_register,
        "polygenic_genotype_get": genotype_get,
        "polygenic_genotype_mutate": genotype_mutate,
        "polygenic_fitness_compute": fitness_compute,
        "polygenic_ecosystem_run_cycle": ecosystem_run_cycle,
        "polygenic_ecosystem_state": ecosystem_state,
        "polygenic_trade_record": trade_record,
        "polygenic_trade_advantage_map": trade_advantage_map,
        "polygenic_speciation_check": speciation_check,
        "polygenic_lineage_get": lineage_get,
    }

    def handle_request(request: dict) -> dict:
        method = request.get("method", "")
        params = request.get("params", {})
        request_id = request.get("id")

        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "polygenic-economics", "version": "3.0.0"},
                },
            }
        elif method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "tools": [
                        {"name": name, "description": func.__doc__ or "",
                         "inputSchema": {"type": "object", "properties": {}}}
                        for name, func in tools.items()
                    ]
                },
            }
        elif method == "tools/call":
            tool_name = params.get("name", "")
            tool_args = params.get("arguments", {})
            if tool_name in tools:
                try:
                    result = tools[tool_name](**tool_args)
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {"content": [{"type": "text", "text": result}]},
                    }
                except Exception as e:
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {"code": -32603, "message": str(e)},
                    }
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {"code": -32601, "message": f"Tool not found: {tool_name}"},
                }
        else:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32601, "message": f"Method not found: {method}"},
            }

    return handle_request


# ─────────────────────────────────────────────────────────────────────────────
# CLI Entry Point
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(levelname)s: %(message)s")

    server = create_polygenic_mcp_server()
    logger.info("Starting Polygenic Economics MCP server...")
    logger.info("Connect with any MCP-compatible client (Claude Code, Cursor, Codex, etc.)")

    if hasattr(server, "run"):
        server.run()
    else:
        logger.info("Manual MCP mode — reading from stdin, writing to stdout")
        for line in sys.stdin:
            try:
                request = json.loads(line)
                response = server(request)
                print(json.dumps(response), flush=True)
            except json.JSONDecodeError:
                continue
            except Exception as e:
                logger.error("Request handling error: %s", e)
