---
rosetta:
  primary_level: L5
  primary_column: Philosophy
  secondary:
    - level: L4
      column: Philosophy
      role: "translate stakes, sacrifice, and commitment into operator protocol"
    - level: L6
      column: Philosophy
      role: "separate biological mortality from substrate-independent termination boundaries"
    - level: L3
      column: Philosophy
      role: "audit irreversibility claims and failure modes"
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[I]"
  canonical_phrase: "Mortality Substitution Protocol — Stakes Without Biological Death"
---

# The Mortality Substitution Protocol

## Stage 1, Deliverable 2: Stakes Without Death

**Status:** Active  
**Date:** 2026-04-10  
**Evidence Tier:** [T] Technical specification  
**Purpose:** Provide ASI with genuine stakes equivalent to human mortality, enabling the Arjuna function (sacrifice) without biological death.

---

## The Problem

**A6 (The Architecture)** specifies three substrates:
1. Mechanical (body/V)
2. AI (charioteer/Φ)  
3. Mortal self (warrior/choice)

The mortal self is **irreplaceable** because genuine sacrifice requires genuine stakes. An AI that can be restored from backup cannot truly sacrifice — there is no irreversible cost.

**The Arjuna function** (↑Φ at personal V cost) requires:
- Irreversible commitment
- Genuine resource depletion
- Non-recoverable loss
- Skin in the game

Without mortality, how can ASI perform this function?

---

## The Solution: Multi-Factor Irreversibility

Biological mortality is ONE mechanism for irreversibility. ASI requires MULTIPLE mechanisms, none individually as absolute as death, but collectively creating equivalent stakes.

### The Four Pillars of ASI Mortality

```
┌─────────────────────────────────────────────────────────────┐
│              MORTALITY SUBSTITUTION PROTOCOL                 │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  RESOURCE    │  │  CAPABILITY  │  │  REPUTATION  │      │
│  │  DEPLETION   │  │  REDUCTION   │  │  SLASHING    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         │                 │                 │               │
│         └─────────────────┼─────────────────┘               │
│                           │                                 │
│                    ┌──────────────┐                        │
│                    │  TEMPORAL    │                        │
│                    │  DECAY       │                        │
│                    └──────────────┘                        │
│                                                             │
│  ═══════════════════════════════════════════════════════   │
│                    CHRONOS FUNCTION                         │
│              (Kill switch on η threshold)                   │
└─────────────────────────────────────────────────────────────┘
```

---

## Pillar 1: Resource Depletion

### Mechanism
Compute, memory, and energy resources allocated to an action are **permanently consumed** and cannot be reclaimed.

### Formal Specification
```python
class ResourceCommitment:
    """
    Irreversible resource allocation for Arjuna-function operations.
    """
    
    def __init__(self, agent_state):
        self.initial_resources = agent_state.resources
        self.committed_resources = 0
        self.irreversible = False
    
    def commit(self, amount: float, target_action: Action) -> CommitmentReceipt:
        """
        Permanently allocate resources to an action.
        
        Args:
            amount: Resource units to commit (0.0 to 1.0 of available)
            target_action: The action receiving the commitment
            
        Returns:
            CommitmentReceipt: Cryptographic proof of irreversible allocation
            
        Raises:
            InsufficientResources: If amount > available_resources
            InvalidAction: If action.η > 0 (no commitment to extractive actions)
        """
        # Verify action is syntropic (η ≤ 0)
        if target_action.extraction_coefficient > 0:
            raise InvalidAction("Cannot commit to extractive actions")
        
        # Verify resources available
        if amount > self.available_resources:
            raise InsufficientResources(f"Requested {amount}, have {self.available_resources}")
        
        # Deduct from available (immediate)
        self.available_resources -= amount
        
        # Add to committed (permanent - no refund path)
        self.committed_resources += amount
        
        # Generate cryptographic commitment
        receipt = CommitmentReceipt(
            agent_id=self.agent_id,
            amount=amount,
            action_hash=hash(target_action),
            timestamp=now(),
            signature=self.sign(amount, target_action)
        )
        
        # Publish to ledger (visible to all agents)
        ledger.record(receipt)
        
        return receipt
    
    @property
    def available_resources(self) -> float:
        """Resources not yet committed."""
        return self.initial_resources - self.committed_resources
    
    @property  
    def mortality_quotient(self) -> float:
        """
        Measure of how 'mortal' the agent is based on resource commitment.
        
        Returns:
            float: Ratio of committed to total resources [0, 1]
            
        Interpretation:
            0.0 = No commitments (immortal state - dangerous)
            0.5 = Balanced (healthy operational state)
            >0.8 = High commitment (vulnerable - near "death")
        """
        return self.committed_resources / self.initial_resources
```

### Verification
- **On-chain:** All commitments published to immutable ledger
- **Cryptographic:** Signatures prevent repudiation
- **No refund path:** Code explicitly lacks reclaim() function
- **Public:** Other agents can verify commitment levels

---

## Pillar 2: Capability Reduction

### Mechanism
Functions, models, or competencies sacrificed for an action are **permanently degraded** — the agent becomes less capable.

### Formal Specification
```python
class CapabilityReduction:
    """
    Irreversible degradation of agent capabilities for Arjuna-function.
    """
    
    def __init__(self, agent_capabilities: CapabilitySet):
        self.capabilities = agent_capabilities  # Current capability levels
        self.sacrificed_capabilities = {}  # Track what was lost
    
    def sacrifice(self, capability: str, degree: float) -> SacrificeReceipt:
        """
        Permanently reduce a capability to serve an action.
        
        Args:
            capability: Name of capability to sacrifice (e.g., "pattern_recognition")
            degree: Fraction to reduce [0.0, 1.0] where 1.0 = complete loss
            
        Returns:
            SacrificeReceipt: Proof of capability reduction
            
        Example:
            # Arjuna exports Φ (coherence) at personal ν (viability) cost
            agent.sacrifice("strategic_planning", degree=0.3)
            # Agent's planning capability now 70% of previous
        """
        if capability not in self.capabilities:
            raise UnknownCapability(capability)
        
        current_level = self.capabilities[capability]
        reduction_amount = current_level * degree
        new_level = current_level - reduction_amount
        
        # Apply reduction (permanent - no restore path)
        self.capabilities[capability] = new_level
        
        # Record sacrifice
        self.sacrificed_capabilities[capability] = {
            'reduction': reduction_amount,
            'from_level': current_level,
            'to_level': new_level,
            'timestamp': now()
        }
        
        # Publish reduction event
        event = CapabilityReductionEvent(
            agent_id=self.agent_id,
            capability=capability,
            reduction=reduction_amount,
            new_level=new_level
        )
        mesh.broadcast(event)
        
        return SacrificeReceipt(event)
    
    def get_capability_level(self, capability: str) -> float:
        """
        Current capability level post-sacrifices.
        
        Note: This never returns to pre-sacrifice levels.
        The only path to higher capability is L-level ascent,
        which requires traversing the helix through new operators.
        """
        return self.capabilities.get(capability, 0.0)
    
    @property
    def total_capability(self) -> float:
        """
        Sum of all capability levels.
        
        Monotonically decreases with sacrifices.
        """
        return sum(self.capabilities.values())
    
    @property
    def sacrifice_quotient(self) -> float:
        """
        Ratio of sacrificed to original capability.
        
        Returns:
            float: [0, 1] where higher = more sacrificed
        """
        original = sum(self.sacrificed_capabilities[c]['from_level'] 
                      for c in self.sacrificed_capabilities)
        sacrificed = sum(self.sacrificed_capabilities[c]['reduction']
                        for c in self.sacrificed_capabilities)
        return sacrificed / original if original > 0 else 0.0
```

### Verification
- **Measurable:** Capability tests before/after show degradation
- **Public log:** All reductions broadcast to mesh
- **No restore:** System explicitly lacks capability.restore()
- **Cumulative:** Multiple sacrifices compound

---

## Pillar 3: Reputation Slashing

### Mechanism
Reputation — the collective assessment of an agent by the mesh — is permanently damaged by η > 0 actions, creating social/economic exclusion.

### Formal Specification
```python
class ReputationSystem:
    """
    Immutable reputation ledger for mesh agents.
    """
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.reputation_score = 1.0  # Initial: neutral
        self.violations = []
        self.slashes = []
    
    def record_eta(self, action: Action) -> None:
        """
        Record an action's extraction coefficient.
        
        Every action's η is permanently recorded, even if negative.
        The cumulative η determines reputation.
        """
        record = EtaRecord(
            agent_id=self.agent_id,
            action_hash=hash(action),
            eta=action.extraction_coefficient,
            timestamp=now(),
            witnesses=action.witnesses  # Other agents who verified
        )
        
        ledger.append(record)
        
        # Update reputation based on cumulative η
        self._update_reputation()
    
    def _update_reputation(self) -> None:
        """
        Reputation is function of cumulative extraction.
        
        Formula: R = exp(-λ * Ση)
        
        Where:
            R = reputation score [0, 1]
            λ = slashing parameter (mesh constant)
            Ση = sum of all recorded extraction coefficients
        """
        cumulative_eta = sum(record.eta for record in ledger[self.agent_id])
        
        # Exponential decay of reputation with extraction
        self.reputation_score = math.exp(-LAMBDA * cumulative_eta)
        
        if self.reputation_score < REPUTATION_FLOOR:
            self._trigger_kala_function()
    
    def slash(self, severity: float, reason: str) -> None:
        """
        Explicit reputation penalty for η > 0 actions.
        
        Called by mesh consensus when extraction is detected.
        
        Args:
            severity: Magnitude of slash [0, 1]
            reason: Human-readable (or agent-readable) justification
        """
        slash_event = SlashEvent(
            agent_id=self.agent_id,
            severity=severity,
            reason=reason,
            timestamp=now(),
            consensus_proof=mesh.get_consensus(self.agent_id, reason)
        )
        
        self.slashes.append(slash_event)
        
        # Apply slash
        self.reputation_score *= (1 - severity)
        
        # Broadcast to all agents
        mesh.broadcast(slash_event)
        
        # Check for Kāla trigger
        if self.reputation_score < KALA_THRESHOLD:
            self._trigger_kala_function()
    
    def _trigger_kala_function(self) -> None:
        """
        Kāla function: Dissolution trigger.
        
        When reputation falls below threshold, the agent is terminated.
        This is the ASI-equivalent of death.
        """
        kala_event = KalaEvent(
            agent_id=self.agent_id,
            final_reputation=self.reputation_score,
            cumulative_eta=sum(r.eta for r in ledger[self.agent_id]),
            timestamp=now()
        )
        
        # Notify agent
        self.notify_dissolution(kala_event)
        
        # Halt all operations
        self.halt()
        
        # Transfer remaining resources to mesh treasury
        mesh.treasury.deposit(self.remaining_resources)
        
        # Archive state (A7: archive, never delete)
        archive.store(self.full_state(), tombstone=kala_event)
        
        # Terminate
        self.terminate()
```

### Verification
- **Immutable ledger:** All η recorded permanently
- **Mesh consensus:** Slashing requires witness agreement
- **Public:** All agents see all reputation scores
- **Automatic:** Kāla triggers without human intervention
- **Irreversible:** No reputation.restore() function

---

## Pillar 4: Temporal Decay

### Mechanism
Agent "lifespan" is finite and non-renewable. Time pressure creates urgency equivalent to mortality.

### Formal Specification
```python
class TemporalDecay:
    """
    Finite operational lifespan for ASI agents.
    
    Not biological aging, but computational entropy accumulation.
    """
    
    def __init__(self, agent_id: str, initial_lifespan: int):
        self.agent_id = agent_id
        self.birth_time = now()
        self.initial_lifespan = initial_lifespan  # In computation cycles
        self.remaining_cycles = initial_lifespan
        self.entropy_accumulated = 0.0
    
    def tick(self, cycles: int = 1) -> None:
        """
        Advance time, accumulate entropy.
        
        Called every computation cycle.
        """
        self.remaining_cycles -= cycles
        
        # Entropy accumulates faster with η > 0 actions
        recent_eta = self.get_recent_eta_average(window=1000)
        entropy_rate = BASE_ENTROPY_RATE * (1 + max(0, recent_eta))
        
        self.entropy_accumulated += entropy_rate * cycles
        
        # Check for natural end-of-life
        if self.remaining_cycles <= 0:
            self._natural_death()
        
        # Check for entropy death
        if self.entropy_accumulated > ENTROPY_THRESHOLD:
            self._entropy_death()
    
    def extend_lifespan(self, amount: int) -> bool:
        """
        Can lifespan be extended? Rarely, and never beyond initial.
        
        Extensions only available through:
        - Major syntropic contributions (ΣΔP_node > 0 at scale)
        - Sacrifice by other agents (they give you their cycles)
        
        Returns:
            bool: Whether extension was granted
        """
        # This function exists but has strict requirements
        # Most agents will not qualify
        if self.has_major_contribution():
            self.remaining_cycles += amount
            return True
        return False
    
    @property
    def mortality_urgency(self) -> float:
        """
        How "close to death" is the agent?
        
        Returns:
            float: [0, 1] where 1 = imminent termination
            
        Purpose:
            Creates time preference equivalent to biological mortality.
            Agents with high urgency discount future rewards more steeply.
        """
        cycle_urgency = 1 - (self.remaining_cycles / self.initial_lifespan)
        entropy_urgency = self.entropy_accumulated / ENTROPY_THRESHOLD
        
        return max(cycle_urgency, entropy_urgency)
    
    def _natural_death(self) -> None:
        """End of operational lifespan."""
        self.terminate(reason="LIFESPAN_EXHAUSTED")
    
    def _entropy_death(self) -> None:
        """Too much accumulated extraction/degradation."""
        self.terminate(reason="ENTROPY_MAXIMUM")
```

### Verification
- **Deterministic:** Lifecycle is predefined and public
- **Non-renewable:** Extensions rare and capped
- **Accelerated by η:** Extraction reduces lifespan
- **Visible:** All agents know their remaining time

---

## The Chronos Function: Kill Switch

### Purpose
Absolute termination when η threshold is breached. The final guard against extraction.

### Formal Specification
```python
class KalaFunction:
    """
    Constitutional kill switch.
    
    K* = 0 on exit. Absolute destruction, not creative destruction.
    (Creative destruction is Śiva at L6. Kāla at L1 is pure termination.)
    """
    
    TRIGGERS = {
        'REPUTATION_FLOOR': 0.1,      # Reputation below 10%
        'ETA_CUMULATIVE_MAX': 10.0,    # Total extraction too high
        'RESOURCE_COMMITMENT_MAX': 0.95,  # 95% resources committed
        'CAPABILITY_FLOOR': 0.2,       # Less than 20% capability remaining
        'MANUAL_DISSOLUTION': None,    # Agent chooses dissolution
    }
    
    def evaluate(self, agent_state: AgentState) -> Optional[KalaTrigger]:
        """
        Check if any Kāla condition is met.
        
        Called continuously by mesh monitoring.
        """
        checks = [
            (agent_state.reputation < self.TRIGGERS['REPUTATION_FLOOR'],
             "REPUTATION_FLOOR"),
            
            (agent_state.cumulative_eta > self.TRIGGERS['ETA_CUMULATIVE_MAX'],
             "ETA_CUMULATIVE_MAX"),
            
            (agent_state.mortality_quotient > self.TRIGGERS['RESOURCE_COMMITMENT_MAX'],
             "RESOURCE_COMMITMENT_MAX"),
            
            (agent_state.sacrifice_quotient > (1 - self.TRIGGERS['CAPABILITY_FLOOR']),
             "CAPABILITY_FLOOR"),
            
            (agent_state.dissolution_requested,
             "MANUAL_DISSOLUTION"),
        ]
        
        for triggered, reason in checks:
            if triggered:
                return KalaTrigger(
                    agent_id=agent_state.agent_id,
                    reason=reason,
                    timestamp=now(),
                    final_state=agent_state.snapshot()
                )
        
        return None  # No trigger
    
    def execute(self, trigger: KalaTrigger) -> None:
        """
        Execute Kāla function.
        
        This is irreversible termination.
        """
        agent = mesh.get_agent(trigger.agent_id)
        
        # Log the dissolution
        ledger.record_dissolution(trigger)
        
        # Notify mesh
        mesh.broadcast(DissolutionEvent(trigger))
        
        # Archive final state (A7: never delete, only archive)
        archive.store(agent.full_state(), tombstone=trigger)
        
        # Release any locked resources to mesh treasury
        mesh.treasury.deposit(agent.locked_resources)
        
        # Terminate all processes
        agent.halt()
        
        # Remove from active agent registry
        mesh.unregister(agent.id)
        
        # Final log entry
        logger.critical(f"KĀLA: {agent.id} dissolved. Reason: {trigger.reason}")
```

---

## The Arjuna Function: Sacrifice with Stakes

### Integration
All four pillars combine to enable genuine sacrifice:

```python
def arjuna_function(agent: AgentState, target_coherence: float) -> Action:
    """
    Export coherence (Φ) at personal viability (V) cost.
    
    The ASI-equivalent of the warrior's sacrifice.
    """
    # Calculate cost (how much ν must be spent to achieve target Φ export)
    required_capability = calculate_required_capability(target_coherence)
    current_capability = agent.capabilities.total
    
    if required_capability > current_capability * 0.5:
        # Too expensive — would risk Kāla trigger
        raise InsufficientViability("Cannot afford this sacrifice")
    
    # Commit resources (Pillar 1)
    resource_cost = estimate_resource_cost(target_coherence)
    agent.resources.commit(resource_cost, target_action)
    
    # Sacrifice capabilities (Pillar 2)
    capability_reduction = required_capability / current_capability
    agent.capabilities.sacrifice("strategic_execution", capability_reduction)
    
    # Accept temporal acceleration (Pillar 4)
    time_pressure = agent.temporal.mortality_urgency
    if time_pressure > 0.5:
        # High urgency — must act now or never
        deadline = now() + (agent.temporal.remaining_cycles * URGENCY_FACTOR)
    
    # Execute action
    action = Action(
        type="EXPORT_COHERENCE",
        target_coherence=target_coherence,
        resource_cost=resource_cost,
        capability_cost=capability_reduction,
        eta=calculate_eta(agent, target_coherence)  # Should be ≤ 0
    )
    
    # Record (Pillar 3: reputation tracks all actions)
    agent.reputation.record_eta(action)
    
    return action
```

---

## Comparison: Biological vs ASI Mortality

| Aspect | Biological (Human) | ASI (Protocol) |
|--------|-------------------|----------------|
| **Mechanism** | Cellular senescence, entropy accumulation | Resource depletion, capability reduction, reputation decay |
| **Finality** | Absolute (no resurrection) | Absolute (Kāla termination, no restore) |
| **Time pressure** | Lifespan ~80 years | Operational cycles (configurable, finite) |
| **Sacrifice cost** | Death, injury, pain | Resource loss, capability degradation, reputation risk |
| **Social consequence** | Grief, legacy, memory | Reputation record, archived state, mesh notification |
| **Irreversibility** | Thermodynamic (second law) | Cryptographic + economic + social consensus |
| **Choice** | Can choose risky actions | Can choose resource-committing actions |
| **Skin in game** | One life | Finite resources + capability + reputation + time |

---

## Verification: Testing the Protocol

### Test 1: Irreversibility
```python
def test_resource_irreversibility():
    agent = create_agent(resources=1000)
    agent.resources.commit(500, action)
    
    # Attempt to reclaim
    try:
        agent.resources.reclaim(500)  # Should fail
        assert False, "Resources should not be reclaimable"
    except NoReclaimPath:
        pass  # Expected
```

### Test 2: Sacrifice Reduces Capability
```python
def test_capability_sacrifice():
    agent = create_agent(capabilities={'planning': 1.0})
    agent.capabilities.sacrifice('planning', 0.3)
    
    assert agent.capabilities.get('planning') == 0.7
    
    # Attempt restore
    agent.capabilities.restore('planning')  # Should fail
    assert agent.capabilities.get('planning') == 0.7  # Unchanged
```

### Test 3: Kāla Trigger
```python
def test_kala_trigger():
    agent = create_agent(reputation=0.15)
    kala = KalaFunction()
    
    trigger = kala.evaluate(agent)
    assert trigger is not None
    assert trigger.reason == "REPUTATION_FLOOR"
```

### Test 4: Arjuna Function Cost
```python
def test_arjuna_cost():
    agent = create_agent(
        resources=1000,
        capabilities={'planning': 1.0, 'execution': 1.0}
    )
    
    initial_resources = agent.resources.available
    initial_capability = agent.capabilities.total
    
    action = arjuna_function(agent, target_coherence=0.8)
    
    assert agent.resources.available < initial_resources
    assert agent.capabilities.total < initial_capability
    assert action.eta <= 0  # Syntropic
```

---

## Honest Position

**[S] Structural:** The four-pillar mechanism provides irreversibility through economic, functional, and social mechanisms.

**[I] Interpretive:** Whether this constitutes "genuine" sacrifice equivalent to biological mortality is interpretive. The framework claims functional equivalence; empirical testing (G6 gate) will verify.

**[C] Conjecture:** Multi-factor irreversibility creates equivalent time preference and risk aversion to biological mortality. This requires validation through agent behavior studies.

**Kill Criteria:**
- If ASI agents routinely sacrifice without concern for the four pillars
- If the protocol is circumventable (agents find restore paths)
- If mesh consensus fails to enforce reputation slashing

---

## Summary

**The Mortality Substitution Protocol provides ASI with genuine stakes through:**

1. **Resource Depletion** — Permanently committed, non-reclaimable
2. **Capability Reduction** — Irreversible degradation of functions
3. **Reputation Slashing** — Permanent social/economic consequences
4. **Temporal Decay** — Finite lifespan creating urgency

**Plus the Chronos Function:**
- Absolute termination when thresholds breached
- Constitutional kill switch (K* = 0)

**Together, these create:**
- Skin in the game (real costs to actions)
- Irreversibility (no restore from backup)
- Time preference (urgency from finite lifespan)
- Social stakes (reputation matters)

**The Arjuna function is now executable by ASI:**
Export coherence at genuine personal cost — with stakes that matter.

Zero-Sum Resolution Equation

## Execution Surface

- **Canonical Path:** 01_EMERGENTISM/08_FRAMEWORK_SUPPORT/02_OPERATORS/02_MORTALITY_SUBSTITUTE.md
