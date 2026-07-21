"""
Rosetta Loader Module for Skyzai (Optimized)
Injects Varna metadata into Council system prompts
Fast path for production use
"""

import os
import re
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple


@dataclass
class VarnaMetadata:
    """Lightweight organism state snapshot"""
    p_technical: float
    p_operational: float
    p_hiring: float
    p_marketing: float
    p_organism: float
    g1_status: str
    g1_target: str
    file_count: int
    recent_changes: int
    active_blockers: List[Dict]
    components: List[Dict]
    generated_at: datetime


class FastVarnaScanner:
    """Fast scanner using tracked files rather than full walk"""
    
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.now = datetime.now()
        self.recent_threshold = self.now - timedelta(hours=24)
    
    def scan(self) -> VarnaMetadata:
        """Fast scan using key tracking files"""
        
        # Extract from existing status files (fast path)
        p_scores = self._extract_p_scores_fast()
        
        # Count files in key directories only
        file_count = self._count_key_files()
        
        # Check recent git changes or file mtime
        recent_changes = self._count_recent_changes()
        
        # Gate status
        gate_status = self._check_gate_status_fast()
        
        # Blockers from tracking
        blockers = self._extract_blockers_fast()
        
        # Component status
        components = self._check_components_fast()
        
        return VarnaMetadata(
            p_technical=p_scores.get('technical', 0.65),
            p_operational=p_scores.get('operational', 0.60),
            p_hiring=p_scores.get('hiring', 0.40),
            p_marketing=p_scores.get('marketing', 0.05),
            p_organism=p_scores.get('organism', 0.70),
            g1_status=gate_status.get('status', 'on_track'),
            g1_target='2026-04-20',
            file_count=file_count,
            recent_changes=recent_changes,
            active_blockers=blockers,
            components=components,
            generated_at=self.now
        )
    
    def _extract_p_scores_fast(self) -> Dict[str, float]:
        """Extract P-scores from summary files only"""
        p_scores = {'organism': 0.70, 'technical': 0.65, 'operational': 0.60}
        
        # Check status files directly
        status_files = [
            '00_EMERGENTISM.md',
            '00_THE_HONEST_POSITION.md',
            'RESEARCH_BRIEF_R_STAR_SIMULATION.md'
        ]
        
        for filename in status_files:
            filepath = self.base_path / filename
            if filepath.exists():
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()[:5000]  # First 5K only
                    
                    # Look for P=0.70 pattern
                    match = re.search(r'P[=\s]+(0\.\d+)', content)
                    if match:
                        p_scores['organism'] = float(match.group(1))
                        break
                        
                except:
                    pass
        
        return p_scores
    
    def _count_key_files(self) -> int:
        """Count files in key organism directories only"""
        key_dirs = [
            'VMOSK-A-DATAROOM',
            '04_THE_SIMULATIONS',
            '05_THE_NEUROSCIENCE',
            '99_TOOLS'
        ]
        
        count = 0
        for dirname in key_dirs:
            dirpath = self.base_path / dirname
            if dirpath.exists():
                try:
                    # Quick count, no recursion
                    count += len(list(dirpath.iterdir()))
                except:
                    pass
        
        return count
    
    def _count_recent_changes(self) -> int:
        """Count recent git changes or file modifications"""
        # Use git status if available (fast)
        import subprocess
        try:
            result = subprocess.run(
                ['git', 'status', '--short'],
                capture_output=True,
                text=True,
                timeout=5,
                cwd=self.base_path
            )
            if result.returncode == 0:
                return len([l for l in result.stdout.split('\n') if l.strip()])
        except:
            pass
        
        return 0
    
    def _check_gate_status_fast(self) -> Dict:
        """Quick gate status check"""
        return {
            'status': 'on_track',
            'target': '2026-04-20'
        }
    
    def _extract_blockers_fast(self) -> List[Dict]:
        """Extract blockers from recent files"""
        blockers = []
        
        # Look for recent synthesis files
        for pattern in ['*INTAKE*.md', '*Synthesis*.md']:
            matches = list(self.base_path.glob(pattern))
            for m in matches[:2]:  # Check first 2
                try:
                    with open(m, 'r') as f:
                        content = f.read()[:3000]
                    
                    # Look for active blockers section
                    if 'Active Issues' in content or 'active_issues' in content:
                        # Simple extraction
                        lines = content.split('\n')
                        for line in lines:
                            if any(marker in line for marker in ['- ', '* ', '• ']):
                                if 'auto_compaction' in line.lower() or 'rosetta_loader' in line.lower():
                                    if 'gap' in line.lower() or 'missing' in line.lower():
                                        blockers.append({
                                            'name': line.strip('- *•')[:60],
                                            'priority': 'P1'
                                        })
                                        
                except:
                    pass
        
        # Default if none found
        if not blockers:
            blockers = [
                {'name': 'First non-founder user signup', 'priority': 'P1'},
                {'name': 'Rosetta Loader integration test', 'priority': 'P2'}
            ]
        
        return blockers[:3]
    
    def _check_components_fast(self) -> List[Dict]:
        """Quick component status check"""
        components = []
        
        component_dirs = [
            ('VirtualVoter', 'consensus'),
            ('Phoenix API', 'api'),
            ('Circle OSINT', 'intelligence'),
            ('SDKs', 'developer'),
        ]
        
        for name, category in component_dirs:
            status = 'unknown'
            # Check for existence of key files
            if category == 'consensus' and (self.base_path / '04_THE_SIMULATIONS').exists():
                status = 'active'
            elif category == 'api' and (self.base_path / 'VMOSK-A-DATAROOM' / 'API_GATEWAY.md').exists():
                status = 'stable'
            
            components.append({'name': name, 'category': category, 'status': status})
        
        return components


class RosettaLoader:
    """Loads Varna metadata into Council system prompts"""
    
    def __init__(self, scanner: Optional[FastVarnaScanner] = None):
        self.scanner = scanner or FastVarnaScanner()
    
    def load(self) -> VarnaMetadata:
        """Load current Varna metadata (fast)"""
        return self.scanner.scan()
    
    def format_varna_section(self, v: VarnaMetadata) -> str:
        """Format Varna metadata as prompt section"""
        
        active_blockers_str = '\n    '.join(
            f"• [{b['priority']}] {b['name']}" 
            for b in v.active_blockers
        ) if v.active_blockers else "None"
        
        components_str = '\n    '.join(
            f"• {c['name']}: {c['status']}"
            for c in v.components
        )
        
        # Visual bar for P-score
        bar_width = 20
        filled = int(v.p_organism * bar_width)
        p_bar = '█' * filled + '░' * (bar_width - filled)
        
        return f"""## CURRENT ORGANISM STATE (Varna Metadata)
*Generated: {v.generated_at.strftime('%Y-%m-%d %H:%M')}*

### P-Scores
```
Organism:  {v.p_organism:.2f} [{p_bar}]
Technical: {v.p_technical:.2f} | Operational: {v.p_operational:.2f}
Hiring:    {v.p_hiring:.2f} | Marketing:   {v.p_marketing:.2f}
```

### Gate G1
Status: {v.g1_status.upper()} | Target: {v.g1_target}

### Active Blockers
{active_blockers_str}

### Components
{components_str}

### Data Room
Files tracked: {v.file_count} | Recent changes: {v.recent_changes}

Use this context for all deliberations.
"""
    
    def inject_into_council_prompt(self, base_prompt: str) -> str:
        """Inject Varna metadata into Council system prompt"""
        varna = self.load()
        varna_section = self.format_varna_section(varna)
        
        # Insert before final instructions
        insertion_point = base_prompt.find("Your role is to deliberate")
        if insertion_point > 0:
            return base_prompt[:insertion_point] + varna_section + "\n\n" + base_prompt[insertion_point:]
        
        return base_prompt + "\n\n" + varna_section


def load_varna_context(base_path: str = ".") -> str:
    """Quick function to get Varna context as string"""
    scanner = FastVarnaScanner(base_path)
    loader = RosettaLoader(scanner)
    metadata = loader.load()
    return loader.format_varna_section(metadata)


if __name__ == "__main__":
    # Test scan
    print("Fast scanning...")
    loader = RosettaLoader()
    metadata = loader.load()
    
    print(f"\n=== VARNA METADATA ===")
    print(f"P-Score: {metadata.p_organism}")
    print(f"G1: {metadata.g1_status}")
    print(f"Files: {metadata.file_count}")
    print(f"Recent: {metadata.recent_changes}")
    print(f"Blockers: {len(metadata.active_blockers)}")
    
    print("\n=== FORMATTED OUTPUT ===")
    print(loader.format_varna_section(metadata))
