"""
Agent Framework Integration
Shows how auto_compaction and rosetta_loader integrate with constitutional_wrapper
"""

from typing import List, Dict, Any
from datetime import datetime
import asyncio

# Import the new modules
from auto_compaction import apply_compaction, Message, ContextCompactor
from rosetta_loader import RosettaLoader, load_varna_context


class IntegratedConstitutionalWrapper:
    """
    Constitutional wrapper with auto-compaction and Varna awareness
    """
    
    def __init__(self, llm_client=None, use_compaction: bool = True):
        self.llm = llm_client
        self.use_compaction = use_compaction
        self.session_history: List[Message] = []
        self.rosetta_loader = RosettaLoader()
        self.compaction_stats = []
    
    async def process(self, user_input: str, phase: str = "execute") -> Dict[str, Any]:
        """
        Five-phase intercept with compaction and Varna context
        """
        
        # === PHASE 1: Validation ===
        validated = self._validate_input(user_input)
        if not validated["valid"]:
            return {"error": validated["reason"], "phase": "validation"}
        
        # === PHASE 2: Context Assembly ===
        # Add user message to history
        self.session_history.append(Message(
            role="user",
            content=user_input,
            timestamp=datetime.now()
        ))
        
        # Check if compaction needed
        context = self._assemble_context()
        
        # === PHASE 3: Tool Orchestration ===
        # (7 directorates, concurrency limits, result budgeting)
        
        # === PHASE 4: Council Deliberation ===
        council_prompt = self._build_council_prompt(context)
        
        # === PHASE 5: Response Assembly ===
        # Generate response with Varna-aware context
        
        return {
            "status": "processed",
            "phase": phase,
            "context_stats": context.get("stats", {}),
            "council_prompt_tokens": len(council_prompt) // 4
        }
    
    def _assemble_context(self) -> Dict[str, Any]:
        """Assemble context with auto-compaction"""
        
        if not self.use_compaction:
            return {"messages": self.session_history, "stats": {"compaction": "disabled"}}
        
        # Apply 3-tier compaction
        compacted = apply_compaction(self.session_history, self.llm)
        
        # Log compaction stats
        self.compaction_stats.append(compacted.compression_stats)
        
        # Build context from tiers
        context_messages = []
        
        # Tier 3: Archive summary (if exists)
        if compacted.tier_3_archived:
            context_messages.append({
                "role": "system",
                "content": compacted.tier_3_archived,
                "tier": 3
            })
        
        # Tier 2: Compressed recent
        for msg in compacted.tier_2_recent:
            context_messages.append({
                "role": msg.role,
                "content": msg.content,
                "tier": 2,
                "compressed": msg.metadata.get("compressed", False) if msg.metadata else False
            })
        
        # Tier 1: Active verbatim
        for msg in compacted.tier_1_active:
            context_messages.append({
                "role": msg.role,
                "content": msg.content,
                "tier": 1
            })
        
        return {
            "messages": context_messages,
            "stats": compacted.compression_stats
        }
    
    def _build_council_prompt(self, context: Dict[str, Any]) -> str:
        """Build Council prompt with Varna metadata"""
        
        base_prompt = """You are the Council of Skyzai.

Your role is to deliberate on all significant decisions using the Intake Synthesis framework.
Follow the constitutional constraints and prioritize based on organism state.

"""
        
        # Inject Varna context
        varna_context = self.rosetta_loader.inject_into_council_prompt(base_prompt)
        
        # Add conversation context
        conversation = "\n\n".join([
            f"[{m.get('tier', '?')}] {m['role']}: {m['content'][:200]}"
            for m in context.get("messages", [])
        ])
        
        return varna_context + "\n\n## CONVERSATION CONTEXT\n" + conversation
    
    def _validate_input(self, user_input: str) -> Dict[str, Any]:
        """Basic input validation"""
        if not user_input or len(user_input.strip()) == 0:
            return {"valid": False, "reason": "Empty input"}
        if len(user_input) > 100000:
            return {"valid": False, "reason": "Input too large"}
        return {"valid": True}


# Integration with error recovery

class IntegratedErrorRecovery:
    """
    Error recovery with compaction-aware context preservation
    """
    
    def __init__(self):
        self.recovery_attempts = []
    
    async def recover_with_compaction(self, 
                                      error: Exception,
                                      wrapper: IntegratedConstitutionalWrapper) -> Dict[str, Any]:
        """
        Recover from error, preserving compressed context
        """
        
        # Get current context state
        context_snapshot = wrapper.session_history[-10:] if wrapper.session_history else []
        
        # Apply compaction to preserve key context
        if len(wrapper.session_history) > 10:
            compacted = apply_compaction(wrapper.session_history, force=True)
            preserved_context = {
                "tier_3_summary": compacted.tier_3_archived,
                "tier_2_compressed": len(compacted.tier_2_recent),
                "tier_1_active": len(compacted.tier_1_active)
            }
        else:
            preserved_context = {"full_history": len(context_snapshot)}
        
        # Recovery strategy with preserved context
        recovery_strategy = {
            "error_type": type(error).__name__,
            "preserved_context": preserved_context,
            "action": "reset_with_context",
            "message": f"Recovered from {type(error).__name__} with {preserved_context}"
        }
        
        self.recovery_attempts.append(recovery_strategy)
        
        return recovery_strategy


# Example usage

async def demo_integration():
    """Demonstrate integrated usage"""
    
    wrapper = IntegratedConstitutionalWrapper(use_compaction=True)
    
    # Simulate conversation
    for i in range(25):
        await wrapper.process(f"User message {i}: Deploy component {i}")
        
        # Simulate assistant response
        wrapper.session_history.append(Message(
            role="assistant",
            content=f"Deployed component {i} successfully",
            timestamp=datetime.now()
        ))
    
    # Check compaction stats
    print("=== COMPACTION STATS ===")
    for i, stats in enumerate(wrapper.compaction_stats):
        print(f"Round {i}: {stats}")
    
    # Build council prompt
    context = wrapper._assemble_context()
    council_prompt = wrapper._build_council_prompt(context)
    
    print(f"\n=== COUNCIL PROMPT ===")
    print(f"Total length: {len(council_prompt)} chars")
    print(f"First 500 chars:\n{council_prompt[:500]}...")


if __name__ == "__main__":
    asyncio.run(demo_integration())
