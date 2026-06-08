import os

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="../shared/style.css">
    <meta name="description" content="{subtitle}">
</head>
<body>
    <header class="terminal-header">
        <div class="brand-mono">{logo_prefix}<span>{logo_suffix}</span></div>
        <nav class="nav-links">
            <a href="#">Manifesto</a>
            <a href="#">Data Room</a>
            <a href="#">Terminal</a>
        </nav>
    </header>

    <main class="hero animate">
        <h1>{heading}</h1>
        <p class="subtitle">{subtitle}</p>
        
        <div class="data-panel">
            <div class="data-header">
                <span>SYSTEM.STATUS</span>
                <span>[ K* = 0 ]</span>
            </div>
            <div class="data-content">
                <p>> Initializing Layer 4 Protocol...</p>
                <p>> {cli_text}</p>
                <p>> Identity: {identity}</p>
            </div>
            <a href="#" class="cta-button">Initialize Protocol</a>
        </div>
    </main>

    <div class="k-invariant">φ · ν = 1</div>
</body>
</html>
"""

properties = {
    "emergentism": {
        "title": "Emergentism — Complexity Arises from Simplicity",
        "logo_prefix": "EMERGENTISM", "logo_suffix": ".ORG",
        "heading": "Emergentism",
        "subtitle": "The definitive philosophical framework for Lagrangian intelligence architecture.",
        "cli_text": "Loading the F5 Field Topology...",
        "identity": "The Core Philosophy"
    },
    "skyzai-com": {
        "title": "Skyzai — Distributed Intelligence",
        "logo_prefix": "Skyzai", "logo_suffix": ".COM",
        "heading": "Skyzai",
        "subtitle": "High-frequency intelligence exchange. Sub-millisecond truth verification.",
        "cli_text": "Connecting to Institutional Backbone...",
        "identity": "The Commercial Network"
    },
    "skyzai-org": {
        "title": "Skyzai Org — Protocol Governance",
        "logo_prefix": "Skyzai", "logo_suffix": ".ORG",
        "heading": "Skyzai.org",
        "subtitle": "The non-profit foundation maintaining the Rosetta Agent Manuals.",
        "cli_text": "Loading Governance Node...",
        "identity": "The Foundation"
    },
    "aureus": {
        "title": "Aureus — F.I.R.E Sector Terraforming",
        "logo_prefix": "AUREUS", "logo_suffix": ".MONEY",
        "heading": "Aureus",
        "subtitle": "Algorithmic restructuring of the Financial, Insurance, and Real Estate sectors.",
        "cli_text": "Calculating Economic Equilibriums...",
        "identity": "The Ledger"
    },
    "helios": {
        "title": "Helios — Infinite Compute",
        "logo_prefix": "HELIOS", "logo_suffix": ".YOU",
        "heading": "Helios",
        "subtitle": "Sovereign personal execution environments. Own your compute.",
        "cli_text": "Provisioning Sovereign Enclave...",
        "identity": "The Personal Agent"
    },
    "circle": {
        "title": "Circle — Truth Consensus Pipeline",
        "logo_prefix": "CIRCLE", "logo_suffix": ".NEWS",
        "heading": "CircleNews",
        "subtitle": "7-agent continuous OSINT ingestion and narrative resolution.",
        "cli_text": "Syncing Data Firehose...",
        "identity": "The Oracle"
    },
    "realityfutures": {
        "title": "Reality Futures — Prediction Markets",
        "logo_prefix": "REALITY", "logo_suffix": "FUTURES",
        "heading": "RealityFutures",
        "subtitle": "Settle reality at K*=0. Unified zero-extraction prediction markets.",
        "cli_text": "Synchronizing Market Factory Object...",
        "identity": "The Casino"
    },
    "apu": {
        "title": "APU — The Autonomous Swarm",
        "logo_prefix": "APU", "logo_suffix": ".BOT",
        "heading": "APU",
        "subtitle": "Deploy parallel agent swarms. Scale your intelligence layer.",
        "cli_text": "Waking up Sub-Agent Matrix...",
        "identity": "The Worker Swarm"
    },
    "menexus": {
        "title": "Menexus — Contextual Memory",
        "logo_prefix": "MENEXUS", "logo_suffix": ".NET",
        "heading": "Menexus",
        "subtitle": "Vector memory layers ensuring total systemic continuity.",
        "cli_text": "Reindexing the Pinecone DB...",
        "identity": "The Memory Matrix"
    }
}

for prop, data in properties.items():
    folder = f"websites/{prop}"
    filepath = f"{folder}/index.html"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_template.format(**data))
    print(f"Generated {filepath}")
