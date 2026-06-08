"""
Auto-Compaction Module for Skyzai
Implements 3-tier context management (adapted from Goose)
Prevents context window overflow in long sessions
"""

from dataclasses import dataclass
from typing import List, Optional, Dict
import hashlib
import json
from datetime import datetime


@dataclass
class Message:
    role: str  # "user", "assistant", "system", "tool"
    content: str
    timestamp: datetime
    metadata: Optional[Dict] = None
    embedding: Optional[List[float]] = None  # for similarity detection


@dataclass
class CompactedContext:
    """Three-tier context structure"""
    tier_1_active: List[Message]      # Last 4 exchanges, verbatim
    tier_2_recent: List[Message]      # Exchanges 5-20, compressed
    tier_3_archived: Optional[str]    # Everything older, summarized
    compression_stats: Dict


class ContextCompactor:
    """
    Maintains (φ − ν)² → 0 for context window.
    
    Tier 1 (Active): 8K tokens — Current conversation flow
    Tier 2 (Recent): 16K tokens — Compressed recent history  
    Tier 3 (Archive): 32K tokens — Summarized old context
    """
    
    TIER_1_EXCHANGES = 4       # Keep last N exchanges verbatim
    TIER_2_EXCHANGES = 16      # Compress next N exchanges
    COMPRESSION_RATIO = 0.5    # Target 50% size reduction
    SIMILARITY_THRESHOLD = 0.85 # For deduplication
    
    def __init__(self, llm_client=None):
        self.llm = llm_client  # For summarization
        self._embedding_cache: Dict[str, List[float]] = {}
    
    def compact(self, session_history: List[Message]) -> CompactedContext:
        """
        Main entry: compress session history into 3-tier structure
        """
        if len(session_history) <= self.TIER_1_EXCHANGES:
            # Nothing to compact yet
            return CompactedContext(
                tier_1_active=session_history,
                tier_2_recent=[],
                tier_3_archived=None,
                compression_stats={"action": "none", "original_tokens": self._count_tokens(session_history)}
            )
        
        # Tier 1: Active (verbatim)
        tier_1 = session_history[-self.TIER_1_EXCHANGES:]
        
        # Remaining for tier 2/3
        remaining = session_history[:-self.TIER_1_EXCHANGES]
        
        if len(remaining) <= self.TIER_2_EXCHANGES:
            # Only tier 2 needed
            tier_2 = self._compress_tier_2(remaining)
            tier_3 = None
        else:
            # Tier 2 + Tier 3
            tier_2_raw = remaining[-self.TIER_2_EXCHANGES:]
            tier_3_raw = remaining[:-self.TIER_2_EXCHANGES]
            
            tier_2 = self._compress_tier_2(tier_2_raw)
            tier_3 = self._summarize_tier_3(tier_3_raw)
        
        stats = {
            "original_exchanges": len(session_history),
            "tier_1_exchanges": len(tier_1),
            "tier_2_exchanges": len(tier_2) if tier_2 else 0,
            "tier_3_summary_tokens": len(tier_3.split()) if tier_3 else 0,
            "compression_ratio": self._calculate_ratio(session_history, tier_1, tier_2, tier_3)
        }
        
        return CompactedContext(tier_1, tier_2, tier_3, stats)
    
    def _compress_tier_2(self, messages: List[Message]) -> List[Message]:
        """
        Compress tier 2 by:
        1. Removing redundant tool calls with identical results
        2. Deduplicating similar user queries
        3. Trimming verbose tool outputs
        """
        compressed = []
        seen_hashes = set()
        
        for msg in messages:
            # Generate content hash for deduplication
            content_hash = hashlib.md5(msg.content.encode()).hexdigest()
            
            if content_hash in seen_hashes:
                # Exact duplicate, skip
                continue
            
            # Check for semantic similarity (if embeddings available)
            if self._is_semantic_duplicate(msg, compressed):
                continue
            
            # Compress tool outputs
            if msg.role == "tool":
                compressed_content = self._compress_tool_output(msg.content)
                msg = Message(
                    role=msg.role,
                    content=compressed_content,
                    timestamp=msg.timestamp,
                    metadata={**msg.metadata, "compressed": True} if msg.metadata else {"compressed": True}
                )
            
            compressed.append(msg)
            seen_hashes.add(content_hash)
        
        return compressed
    
    def _summarize_tier_3(self, messages: List[Message]) -> str:
        """
        Generate abstract summary of old conversation.
        Key facts, decisions, context — not full text.
        """
        # Extract key information
        facts = self._extract_facts(messages)
        decisions = self._extract_decisions(messages)
        context = self._extract_context(messages)
        
        summary = f"""[ARCHIVED CONTEXT — {len(messages)} exchanges]

KEY FACTS ESTABLISHED:
{self._format_list(facts)}

DECISIONS MADE:
{self._format_list(decisions)}

PERSISTENT CONTEXT:
{context}

[Refer to tier_1/tier_2 for recent specifics]
"""
        return summary
    
    def _extract_facts(self, messages: List[Message]) -> List[str]:
        """Extract factual assertions from conversation"""
        facts = []
        for msg in messages:
            if msg.role == "assistant":
                # Look for fact-like statements
                content = msg.content
                if "is" in content or "are" in content or "has" in content:
                    # Simple heuristic — could be enhanced with NER
                    lines = content.split('.')
                    for line in lines:
                        line = line.strip()
                        if len(line) > 20 and len(line) < 200:
                            facts.append(line)
        return facts[:10]  # Top 10 facts
    
    def _extract_decisions(self, messages: List[Message]) -> List[str]:
        """Extract decisions and commitments"""
        decisions = []
        for msg in messages:
            content = msg.content.lower()
            if any(word in content for word in ["decide", "will", "commit", "agree", "approve", "reject"]):
                decisions.append(msg.content.strip()[:150] + "...")
        return decisions[:5]
    
    def _extract_context(self, messages: List[Message]) -> str:
        """Extract persistent context (project names, versions, etc.)"""
        context_parts = []
        
        # Look for version numbers
        for msg in messages:
            if "v" in msg.content and "." in msg.content:
                # Potential version reference
                words = msg.content.split()
                for word in words:
                    if word.startswith("v") and "." in word:
                        context_parts.append(f"Version: {word}")
        
        # Look for P-scores
        for msg in messages:
            if "P=" in msg.content or "P-score" in msg.content:
                # Extract P-score line
                lines = msg.content.split('\n')
                for line in lines:
                    if "P=" in line or "P-score" in line:
                        context_parts.append(line.strip())
                        break
        
        return "\n".join(set(context_parts)) if context_parts else "No persistent context extracted"
    
    def _compress_tool_output(self, content: str, max_lines: int = 10) -> str:
        """Compress verbose tool output"""
        lines = content.split('\n')
        if len(lines) <= max_lines:
            return content
        
        # Keep first 5 and last 5 lines, indicate truncation
        compressed = '\n'.join(lines[:5]) + f"\n... [{len(lines) - 10} lines truncated] ...\n" + '\n'.join(lines[-5:])
        return compressed
    
    def _is_semantic_duplicate(self, msg: Message, existing: List[Message]) -> bool:
        """Check if message is semantically similar to existing"""
        if not msg.embedding:
            return False  # Can't check without embeddings
        
        for existing_msg in existing[-5:]:  # Check against recent only
            if existing_msg.embedding:
                similarity = self._cosine_similarity(msg.embedding, existing_msg.embedding)
                if similarity > self.SIMILARITY_THRESHOLD:
                    return True
        return False
    
    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        dot_product = sum(x * y for x, y in zip(a, b))
        norm_a = sum(x * x for x in a) ** 0.5
        norm_b = sum(x * x for x in b) ** 0.5
        return dot_product / (norm_a * norm_b) if norm_a and norm_b else 0
    
    def _count_tokens(self, messages: List[Message]) -> int:
        """Rough token count (4 chars per token estimate)"""
        total_chars = sum(len(m.content) for m in messages)
        return total_chars // 4
    
    def _calculate_ratio(self, original: List[Message], tier_1: List[Message], 
                        tier_2: List[Message], tier_3: Optional[str]) -> float:
        """Calculate compression ratio"""
        original_tokens = self._count_tokens(original)
        
        tier_1_tokens = self._count_tokens(tier_1)
        tier_2_tokens = self._count_tokens(tier_2) if tier_2 else 0
        tier_3_tokens = len(tier_3.split()) if tier_3 else 0
        
        compressed_tokens = tier_1_tokens + tier_2_tokens + tier_3_tokens
        
        return compressed_tokens / original_tokens if original_tokens > 0 else 1.0
    
    def _format_list(self, items: List[str]) -> str:
        """Format list for summary"""
        if not items:
            return "  None recorded"
        return '\n'.join(f"  • {item[:100]}" for item in items)


# Integration with constitutional_wrapper

def apply_compaction(session_history: List[Message], 
                    llm_client=None,
                    force: bool = False) -> CompactedContext:
    """
    Convenience function for constitutional_wrapper integration
    
    Args:
        session_history: Full conversation history
        llm_client: Optional LLM for summarization
        force: If True, compact even if under threshold
    
    Returns:
        CompactedContext with 3 tiers
    """
    compactor = ContextCompactor(llm_client)
    
    # Check if compaction needed
    total_tokens = compactor._count_tokens(session_history)
    threshold = 24000  # ~75% of 32K context window
    
    if not force and total_tokens < threshold:
        # No compaction needed yet
        return CompactedContext(
            tier_1_active=session_history,
            tier_2_recent=[],
            tier_3_archived=None,
            compression_stats={
                "action": "skipped",
                "reason": "under_threshold",
                "original_tokens": total_tokens,
                "threshold": threshold
            }
        )
    
    # Compact
    return compactor.compact(session_history)


# Example usage
if __name__ == "__main__":
    # Test with synthetic history
    history = [
        Message("user", "Deploy infrastructure", datetime.now()),
        Message("assistant", "Deploying to AWS...", datetime.now()),
        # ... many more messages
    ]
    
    result = apply_compaction(history)
    print(f"Compression stats: {result.compression_stats}")
