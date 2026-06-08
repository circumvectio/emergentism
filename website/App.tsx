import React, { useState, useEffect } from 'react';

// --- HELPER FUNCTIONS ---
const parseMarkdownTable = (markdown: string): { headers: string[], rows: string[][] } => {
  const lines = markdown.trim().split('\n');
  if (lines.length < 2) return { headers: [], rows: [] };

  const headers = lines[0].split('|').map(h => h.trim()).filter(Boolean);
  const rows = lines.slice(2).map(line => 
    line.split('|').map(cell => cell.trim()).filter(Boolean)
  );

  return { headers, rows };
};

const formatText = (text: string): string => {
  return text
    .replace(/\*\*(.*?)\*\*/g, '<strong class="font-semibold text-[var(--color-yellow)]">$1</strong>')
    .replace(/\*(.*?)\*/g, '<em class="italic">$1</em>')
    .replace(/—/g, '&mdash;')
    .replace(/→/g, '&rarr;')
    .replace(/(\w+)²|(\w+)_min|(\w+)_max/g, (match, p1, p2, p3) => {
        if (p1) return `${p1}<sup>2</sup>`;
        if (p2) return `${p2}<sub>min</sub>`;
        if (p3) return `${p3}<sub>max</sub>`;
        return match;
    })
    .replace(/`([^`]+)`/g, '<code class="bg-gray-800 text-yellow-300 font-mono rounded-sm px-1 py-0.5 text-sm">$1</code>')
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" class="text-[var(--color-blue)] hover:underline">$1</a>');
};

const TextFormatter: React.FC<{ text: string; as?: 'p' | 'div' | 'span' | 'h3' | 'li' }> = ({ text, as = 'p' }) => {
  const Component = as;
  return <Component dangerouslySetInnerHTML={{ __html: formatText(text) }} />;
};

// --- ROUTING ---
const useRouter = () => {
  const [route, setRoute] = useState(window.location.hash || '#/');
  
  useEffect(() => {
    const handleHashChange = () => {
      setRoute(window.location.hash || '#/');
      window.scrollTo(0, 0);
    };
    window.addEventListener('hashchange', handleHashChange);
    return () => window.removeEventListener('hashchange', handleHashChange);
  }, []);
  
  return route.replace('#', '');
};

// --- UI COMPONENTS ---
const Button: React.FC<{ children: React.ReactNode; href?: string; variant?: 'blue' | 'green' | 'yellow' | 'red'; className?: string, onClick?: () => void }> = ({ children, href = "#", variant = 'blue', className = '', onClick }) => {
  const baseClasses = "inline-block rounded-md font-display font-semibold text-center transition-all duration-300 ease-in-out transform hover:-translate-y-1 focus:outline-none focus:ring-4 shadow-lg px-8 py-3 uppercase tracking-wider text-sm sm:text-base";
  
  const variantClasses = {
    blue: 'bg-[var(--color-blue)] text-white hover:bg-blue-500 focus:ring-blue-500/50 shadow-blue-500/20',
    green: 'bg-[var(--color-green)] text-white hover:bg-green-500 focus:ring-green-500/50 shadow-green-500/20',
    yellow: 'border-2 border-[var(--color-yellow)] text-[var(--color-yellow)] hover:bg-[var(--color-yellow)] hover:text-black focus:ring-yellow-500/50 shadow-yellow-500/20',
    red: 'bg-[var(--color-red)] text-white hover:bg-red-500 focus:ring-red-500/50 shadow-red-500/20',
  };

  return <a href={href} onClick={onClick} className={`${baseClasses} ${variantClasses[variant]} ${className}`}>{children}</a>;
};

const Section: React.FC<{ title: string; subtitle?: string; children: React.ReactNode; id?: string, className?: string }> = ({ title, subtitle, children, id, className="" }) => (
  <section id={id} className={`py-20 sm:py-28 ${className}`}>
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto text-center mb-12 sm:mb-16">
        <h2 className="text-4xl sm:text-5xl font-bold text-white font-display uppercase tracking-wider" dangerouslySetInnerHTML={{ __html: formatText(title) }} />
        {subtitle && <p className="mt-4 text-lg sm:text-xl text-gray-400" dangerouslySetInnerHTML={{ __html: formatText(subtitle) }} />}
      </div>
      {children}
    </div>
  </section>
);

const Card: React.FC<{ children: React.ReactNode, className?: string}> = ({ children, className }) => (
    <div className={`bg-slate-900/40 p-6 rounded-lg border border-slate-700/50 transition-all duration-300 hover:border-slate-500/50 hover:bg-slate-900/60 ${className}`}>
        {children}
    </div>
);

const HeroSection: React.FC<{ title: string; subtitle: string; children?: React.ReactNode }> = ({ title, subtitle, children }) => (
    <div className="relative pt-32 pb-20 text-center text-white bg-slate-900/20">
      <div className="absolute inset-0 bg-grid-slate-700/[0.1]"></div>
      <div className="absolute inset-0 bg-gradient-to-b from-black via-transparent to-black"></div>
      <div className="relative max-w-5xl mx-auto px-4 z-10">
          <h1 className="text-5xl sm:text-6xl font-extrabold font-display uppercase tracking-wide" dangerouslySetInnerHTML={{ __html: formatText(title) }} />
          <p className="mt-6 max-w-3xl mx-auto text-lg sm:text-xl text-gray-300" dangerouslySetInnerHTML={{ __html: formatText(subtitle) }} />
          {children}
      </div>
    </div>
);

// --- NAVIGATION ---
const NAV_LINKS = {
    'Home': '/',
    'About': '/about',
    'Papers': {
        'White Papers': '/papers',
        'Light Papers': '/light-papers'
    },
    'Tools & Practice': '/tools',
    'Get Involved': '/get-involved',
};

const Header: React.FC = () => {
    const [isScrolled, setIsScrolled] = useState(false);
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
    const [papersDropdownOpen, setPapersDropdownOpen] = useState(false);

    useEffect(() => {
        const handleScroll = () => {
            setIsScrolled(window.scrollY > 50);
        };
        window.addEventListener('scroll', handleScroll, { passive: true });
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    const closeAllMenus = () => {
        setMobileMenuOpen(false);
        setPapersDropdownOpen(false);
    };

    return (
        <header className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${isScrolled || mobileMenuOpen ? 'bg-gray-900/80 backdrop-blur-sm shadow-lg' : 'bg-transparent'}`}>
            <div className="container mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex h-16 items-center justify-between">
                    <a href="#/" onClick={closeAllMenus} className="font-display font-bold text-lg text-white">emergentism.org</a>
                    
                    {/* Desktop Nav */}
                    <nav className="hidden md:flex items-center gap-6">
                        {Object.entries(NAV_LINKS).map(([name, href]) => (
                            typeof href === 'string' ? (
                                <a key={name} href={`#${href}`} className="text-gray-300 hover:text-[var(--color-yellow)] transition-colors text-sm font-medium">{name}</a>
                            ) : (
                                <div key={name} className="relative" onMouseEnter={() => setPapersDropdownOpen(true)} onMouseLeave={() => setPapersDropdownOpen(false)}>
                                    <button className="text-gray-300 hover:text-[var(--color-yellow)] transition-colors text-sm font-medium flex items-center">
                                        {name}
                                        <svg className={`w-4 h-4 ml-1 transition-transform ${papersDropdownOpen ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7"></path></svg>
                                    </button>
                                    {papersDropdownOpen && (
                                        <div className="absolute top-full left-0 mt-2 w-48 bg-gray-800 rounded-md shadow-lg py-1">
                                            {Object.entries(href).map(([subName, subHref]) => (
                                                <a key={subName} href={`#${subHref}`} onClick={() => setPapersDropdownOpen(false)} className="block px-4 py-2 text-sm text-gray-300 hover:bg-gray-700 hover:text-white">{subName}</a>
                                            ))}
                                        </div>
                                    )}
                                </div>
                            )
                        ))}
                    </nav>

                    <div className="md:hidden">
                        <button onClick={() => setMobileMenuOpen(!mobileMenuOpen)} className="text-white p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-inset focus:ring-yellow-400">
                            <span className="sr-only">Open main menu</span>
                            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d={mobileMenuOpen ? "M6 18L18 6M6 6l12 12" : "M4 6h16M4 12h16m-7 6h7"}></path></svg>
                        </button>
                    </div>
                </div>
                
                {/* Mobile Nav */}
                {mobileMenuOpen && (
                    <div className="md:hidden pb-4">
                        <nav className="flex flex-col gap-2">
                            {Object.entries(NAV_LINKS).map(([name, href]) => (
                                typeof href === 'string' ? (
                                    <a key={name} href={`#${href}`} onClick={closeAllMenus} className="text-gray-300 hover:text-[var(--color-yellow)] transition-colors text-base font-medium text-center py-2 rounded-md hover:bg-slate-700/50">{name}</a>
                                ) : (
                                    <div key={name}>
                                        <button onClick={() => setPapersDropdownOpen(!papersDropdownOpen)} className="w-full text-gray-300 hover:text-[var(--color-yellow)] transition-colors text-base font-medium text-center py-2 rounded-md hover:bg-slate-700/50 flex justify-center items-center">
                                            {name}
                                            <svg className={`w-4 h-4 ml-1 transition-transform ${papersDropdownOpen ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7"></path></svg>
                                        </button>
                                        {papersDropdownOpen && (
                                            <div className="flex flex-col gap-1 mt-1 bg-slate-800/50 rounded-md p-2">
                                                {Object.entries(href).map(([subName, subHref]) => (
                                                    <a key={subName} href={`#${subHref}`} onClick={closeAllMenus} className="text-gray-300 hover:text-[var(--color-yellow)] transition-colors text-base font-medium text-center py-2 rounded-md hover:bg-slate-700/50">{subName}</a>
                                                ))}
                                            </div>
                                        )}
                                    </div>
                                )
                            ))}
                        </nav>
                    </div>
                )}
            </div>
        </header>
    );
};

const Footer: React.FC = () => (
    <footer className="py-12 border-t border-slate-800 bg-gray-900">
        <div className="max-w-7xl mx-auto px-4 text-center text-gray-400">
            <h3 className="text-2xl font-display text-white mb-4">Join the Investigation</h3>
            <p className="mb-4">Monthly insights on consciousness, strategy, and the future</p>
            <div className="max-w-md mx-auto">
                <form className="flex flex-col sm:flex-row gap-2">
                    <input type="email" placeholder="Your email for updates..." required className="flex-grow bg-slate-800 border border-slate-700 rounded-md px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-[var(--color-blue)]" />
                    <button type="submit" className="bg-[var(--color-green)] text-white font-semibold px-6 py-2 rounded-md hover:bg-green-500 transition-colors">Subscribe</button>
                </form>
            </div>
            <div className="flex justify-center flex-wrap gap-6 mt-8">
                {Object.entries(NAV_LINKS).map(([name, href]) => (
                    typeof href === 'string' && <a key={name} href={`#${href}`} className="hover:text-[var(--color-yellow)]">{name}</a>
                ))}
            </div>
            <div className="flex justify-center gap-6 mt-8">
                <a href="#" className="hover:text-[var(--color-yellow)]">GitHub</a>
                <a href="#" className="hover:text-[var(--color-yellow)]">Discord</a>
                <a href="#/get-involved" className="hover:text-[var(--color-yellow)]">Contact</a>
            </div>
            <div className="mt-10 text-sm text-gray-500">
                <p>Emergentism is an independent research project synthesizing insights from mathematics, physics, neuroscience, ancient wisdom, and modern AI research.</p>
                <p className="mt-4">Privacy Policy | Terms of Use | Creative Commons BY-SA 4.0</p>
            </div>
        </div>
    </footer>
);

// --- PAGE COMPONENTS ---

// --- HomePage ---
const HomePage: React.FC = () => (
  <>
    <main className="min-h-screen flex items-center justify-center relative overflow-hidden text-white" id="hero">
        <div className="absolute inset-0 bg-grid-slate-700/[0.1]"></div>
        <div className="absolute inset-0 bg-gradient-to-t from-gray-900 via-transparent to-transparent"></div>
        <div className="absolute -top-1/4 -left-1/4 w-1/2 h-1/2 bg-[var(--color-blue)]/10 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute -bottom-1/4 -right-1/4 w-1/2 h-1/2 bg-[var(--color-yellow)]/10 rounded-full blur-3xl animate-pulse animation-delay-4000"></div>
        
        <div className="relative max-w-5xl mx-auto px-4 text-center py-20 z-10">
            <h1 className="text-5xl sm:text-6xl md:text-7xl font-extrabold font-display uppercase tracking-wide fade-in">
                <span className="block">Reality Has an Equation.</span>
                <span className="block text-[var(--color-yellow)] mt-2">And It Changes Everything.</span>
            </h1>
            <p className="mt-8 max-w-3xl mx-auto text-lg sm:text-xl text-gray-300 fade-in fade-in-delay-1">
                The first unified framework explaining consciousness, ethics, and the structure of reality—from quantum mechanics to AI alignment to human flourishing.
            </p>
            <div className="mt-12 flex flex-col sm:flex-row items-center justify-center gap-6 fade-in fade-in-delay-2">
                <Button href="#dimensions" variant="blue">Explore the Framework</Button>
                <Button href="#/papers" variant="yellow">Read the Science</Button>
            </div>
        </div>
    </main>
    <Section id="discovery" title="One Pattern. Seven Dimensions. Infinite Implications.">
        <div className="max-w-4xl mx-auto text-lg text-gray-300 space-y-6 text-center">
            <p>For thousands of years, mystics described reality as a unity. For centuries, scientists sought a theory of everything. Both were right—and both were describing the same structure.</p>
            <p>Emergentism is the mathematical formalization of that structure. At its heart lies a deceptively simple insight: **reality is multiplicative, not additive.**</p>
            <p className="text-4xl font-display text-white py-4 tracking-widest">⊙ = • × ○</p>
            <p className="text-2xl text-gray-400">Effect = Potential × Relation</p>
            <p>This isn't metaphor. It's physics. And it explains why parasitic systems self-terminate, consciousness has an equation (**P = Φ × V**), ethics can be derived from physics (maximize **ΣΔP**), and AI can be safely aligned.</p>
        </div>
    </Section>
    <Section id="consciousness" title="P = Φ × V" subtitle="The First Empirically Validated Equation for Conscious Experience" className="bg-slate-900/20">
        <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto text-center">
            <Card>
                <h3 className="text-3xl font-display text-[var(--color-yellow)]">P</h3>
                <p className="mt-2 text-xl font-semibold text-white">Holistic Potential</p>
                <p className="mt-2 text-gray-400">Your total capacity for experience and action.</p>
            </Card>
            <Card>
                <h3 className="text-3xl font-display text-white">Φ</h3>
                <p className="mt-2 text-xl font-semibold text-white">Integration</p>
                <p className="mt-2 text-gray-400">How coherent and unified your mind is.</p>
            </Card>
            <Card>
                <h3 className="text-3xl font-display text-white">V</h3>
                <p className="mt-2 text-xl font-semibold text-white">Viability</p>
                <p className="mt-2 text-gray-400">Your resources, options, and ability to act.</p>
            </Card>
        </div>
        <div className="max-w-4xl mx-auto text-lg text-gray-300 space-y-6 mt-12 text-center">
            <p className="text-xl font-semibold text-white">Why multiplication matters: Lose either integration or viability, and consciousness collapses—not degrades, but **collapses to zero**.</p>
            <TextFormatter text="This isn't speculation. It's validated by split-brain studies, anesthesia research, and ecosystem data (R² = 0.89 for multiplicative model vs R² = 0.34 for best additive alternative)." />
        </div>
        <div className="text-center mt-12">
            <Button href="#/tools" variant="green">Measure Your P</Button>
        </div>
    </Section>
    <DimensionalJourney />
    <PracticalApplications />
    <SevenAlgorithms />
    <TheScience />
    <WhoThisIsFor />
    <StartHere />
  </>
);
const DimensionalJourney = () => { /* ... implementation from previous step ... */ 
    const dimensions = [
        { dim: "D0", title: "Infinite Potential", symbol: "•", desc: "The Zero — Pure Possibility. The infinite field from which all things can emerge. Not nothing, but possibility itself.", physics: "Quantum vacuum" },
        { dim: "D1", title: "Line", symbol: "Orientation", desc: "The first distinction. A choice of direction. Order emerges.", physics: "One-dimensional quantum systems" },
        { dim: "D2", title: "Plane", symbol: "Curvature", desc: "Relationships become possible. Things can connect, form loops, create topology.", physics: "Two-dimensional materials (graphene)" },
        { dim: "D3", title: "Volume", symbol: "Torsion", desc: "Objects gain depth. Space becomes navigable. The only dimensionality where atoms are stable.", physics: "Three-dimensional space" },
        { dim: "D4", title: "Spacetime", symbol: "Time", desc: "Process. Causality. History. The dimension where physics as we know it lives.", physics: "Special and general relativity" },
        { dim: "D5", title: "Consciousness", symbol: "Variance", desc: "Where you live as an experiencing subject. The dimension of possibility space, agency, and what it feels like to be.", physics: "Quantum superposition" },
        { dim: "D6", title: "The Noösphere", symbol: "Phase", desc: "When consciousnesses synchronize, collective mind emerges. Coherent. Coordinated. More than the sum.", physics: "Macroscopic quantum coherence" },
        { dim: "D6 ≈ D0", title: "The Ouroboros", symbol: "∞", desc: "The End Is The Beginning. Maximum integration returns to primordial unity. The universe recognizing itself.", physics: "Conformal equivalence" },
    ];
    return (
        <Section id="dimensions" title="The Architecture of Reality: D0 → D6" subtitle="*Scroll to journey through the dimensions*">
            <div className="relative max-w-4xl mx-auto">
                <div className="absolute left-1/2 -ml-px w-0.5 h-full bg-gradient-to-b from-[var(--color-blue)]/50 via-[var(--color-yellow)]/50 to-[var(--color-blue)]/50" aria-hidden="true"></div>
                {dimensions.map((d, i) => (
                    <div key={i} className={`relative mb-16 sm:mb-24 group`}>
                        <div className={`flex flex-col sm:flex-row items-center gap-4 sm:gap-0`}>
                           <div className={`flex-1 ${i % 2 === 0 ? 'sm:text-right sm:pr-12' : 'sm:text-left sm:pl-12 sm:order-2'}`}>
                                <h3 className="text-2xl font-display font-bold text-[var(--color-yellow)]">{d.dim}</h3>
                                <h4 className="text-xl font-semibold text-white mt-1">{d.title}</h4>
                                <p className="text-gray-400 mt-2">{d.desc}</p>
                                <p className="text-sm text-blue-400 mt-2">In physics: {d.physics}</p>
                           </div>
                           <div className={`z-10 flex-shrink-0 flex items-center justify-center w-20 h-20 rounded-full bg-gray-900 border-2 border-[var(--color-blue)] shadow-lg transition-transform duration-300 group-hover:scale-110 ${i % 2 === 0 ? '' : 'sm:order-1'}`}>
                                <span className="text-xl font-bold text-white font-mono">{d.symbol}</span>
                            </div>
                            <div className="flex-1 hidden sm:block"></div>
                        </div>
                    </div>
                ))}
            </div>
        </Section>
    );
};
const PracticalApplications = () => { /* ... implementation from previous step ... */ 
    return (
    <Section id="apps" title="From Theory to Practice" subtitle="What You Can Do With This" className="bg-slate-900/20">
        <div className="grid md:grid-cols-3 gap-8 max-w-7xl mx-auto">
            <Card className="text-center flex flex-col">
                <h3 className="text-xl font-display font-bold text-white mb-4">FOR INDIVIDUALS</h3>
                <h4 className="text-lg font-semibold text-[var(--color-yellow)] mb-2">The Warrior-Sage Protocol</h4>
                <p className="text-gray-400 flex-grow">Optimize your P = Φ × V through daily consciousness practices, strategic algorithm mastery, and integration + viability balance.</p>
                <div className="mt-6">
                    <Button href="#/tools" variant="yellow">Learn More &rarr;</Button>
                </div>
            </Card>
            <Card className="text-center flex flex-col">
                <h3 className="text-xl font-display font-bold text-white mb-4">FOR RESEARCHERS</h3>
                <h4 className="text-lg font-semibold text-[var(--color-yellow)] mb-2">Testable Predictions</h4>
                <p className="text-gray-400 flex-grow">Emergentism makes falsifiable claims: split-brain P-measurements, anesthesia Φ-collapse curves, ecosystem P = Φ × V validation, and AI alignment safety theorems.</p>
                 <div className="mt-6">
                    <Button href="#/papers" variant="yellow">See the White Papers &rarr;</Button>
                </div>
            </Card>
            <Card className="text-center flex flex-col">
                <h3 className="text-xl font-display font-bold text-white mb-4">FOR BUILDERS</h3>
                <h4 className="text-lg font-semibold text-[var(--color-yellow)] mb-2">Aligned Superintelligence</h4>
                <p className="text-gray-400 flex-grow">The Bodhisattva-Demiurge architecture: P-Head estimation (Φ and V measurement), Syntropic objective (max ΣΔP), Mycelial coordination, and Provable safety guarantees.</p>
                 <div className="mt-6">
                    <Button href="#/papers" variant="yellow">Read the Blueprint &rarr;</Button>
                </div>
            </Card>
        </div>
    </Section>
);
};
const SevenAlgorithms = () => { /* ... implementation from previous step ... */ 
    const algorithms = [
        { name: "KALI", formula: "ΔΦ < 0, ΔV < 0", desc: "Decay • Parasitism • Entropy", color: "red" },
        { name: "KRISHNA", formula: "ΔΦ > 0, ΔV < 0", desc: "Sacrifice • Transcendence • Refinement" },
        { name: "BRAHMA", formula: "ΔΦ > 0, ΔV > 0", desc: "Creation • Growth • Expansion", color: "green" },
        { name: "SHIVA", formula: "ΔΦ < 0, ΔV > 0", desc: "Creative Destruction • Transformation" },
        { name: "VISHNU", formula: "ΔΦ ≈ 0, ΔV ≈ 0", desc: "Preservation • Maintenance • Homeostasis", color: "blue" },
        { name: "ANANTA SESHA", formula: "ΔΦ >> 0, ΔV >> 0", desc: "Infinite Expansion • Abundance" },
        { name: "VISHVARUPA", formula: "ΔΦ → ∞, ΔV → ∞", desc: "Universal Form • Total Integration" },
    ];
    return (
        <Section id="algorithms" title="Master Reality's Strategic Operators" subtitle="Ancient wisdom meets game theory. Seven archetypal moves in consciousness space.">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-7xl mx-auto">
                {algorithms.map(algo => (
                    <Card key={algo.name} className={`text-center border-t-4 ${algo.color === 'red' ? 'border-[var(--color-red)]' : algo.color === 'green' ? 'border-[var(--color-green)]' : algo.color === 'blue' ? 'border-[var(--color-blue)]' : 'border-slate-700'}`}>
                        <h3 className={`text-2xl font-display font-bold ${algo.color === 'red' ? 'text-[var(--color-red)]' : 'text-[var(--color-yellow)]'}`}>{algo.name}</h3>
                        <p className={`font-mono text-sm ${algo.color === 'green' ? 'text-green-400' : algo.color === 'blue' ? 'text-blue-400' : 'text-gray-400'}`}>{algo.formula}</p>
                        <p className="mt-3 text-gray-300">{algo.desc}</p>
                    </Card>
                ))}
            </div>
             <div className="text-center mt-12">
                <Button href="#/tools" variant="green">Take the Strategic Assessment</Button>
            </div>
        </Section>
    );
};
const TheScience = () => { /* ... implementation from previous step ... */ 
    const papers = ["The Triadic Necessity Theorem", "The μ-Calculus", "The Dimensional Scaffold", "P = Φ × V: The Physics of Consciousness", "Syntropic Ethics", "The Strategic Quaternion", "The Bodhisattva-Demiurge", "Kolmogorov Complexity Zero"];
    return (
        <Section id="science" title="Eight White Papers. One Framework." className="bg-slate-900/20">
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 max-w-7xl mx-auto">
                {papers.map(paper => (
                    <div key={paper} className="border border-slate-700/50 p-4 rounded-md text-center bg-slate-900/40">
                        <p className="font-semibold text-gray-300">{paper}</p>
                    </div>
                ))}
            </div>
            <div className="text-center mt-12">
                <Button href="#/papers" variant="yellow">Download the Complete Stack</Button>
            </div>
        </Section>
    );
};
const WhoThisIsFor = () => { /* ... implementation from previous step ... */ 
    return (
    <Section id="audience" title="Who This Is For">
        <div className="grid md:grid-cols-3 gap-8 max-w-7xl mx-auto">
            <Card>
                <h3 className="text-2xl font-display font-bold text-[var(--color-yellow)] mb-4">SEEKERS</h3>
                <p className="text-gray-300">You've read the Upanishads, the Tao Te Ching, the mystics—and sensed the pattern beneath. Here's that pattern, formalized. The perennial philosophy, now computationally rigorous.</p>
            </Card>
             <Card>
                <h3 className="text-2xl font-display font-bold text-[var(--color-yellow)] mb-4">SCIENTISTS</h3>
                <p className="text-gray-300">You want testable predictions, not hand-waving. We have them: split-brain P-collapse, anesthesia mechanisms, ecosystem validation, AI safety theorems. Falsifiable all the way down.</p>
            </Card>
             <Card>
                <h3 className="text-2xl font-display font-bold text-[var(--color-yellow)] mb-4">BUILDERS</h3>
                <p className="text-gray-300">You're designing AI, building organizations, optimizing systems. You need frameworks that actually work. P = Φ × V gives you measurable objectives. ΣΔP gives you alignment. The Strategic Quaternion gives you tactics.</p>
            </Card>
        </div>
    </Section>
);
};
const StartHere = () => { /* ... implementation from previous step ... */ 
    return (
    <Section id="start" title="Choose Your Entry Point" className="bg-slate-900/20">
        <div className="grid md:grid-cols-3 gap-8 max-w-7xl mx-auto">
            <Card className="flex flex-col">
                <h3 className="text-xl font-display font-bold text-white mb-2">PATH 1: THE QUICK VERSION</h3>
                <h4 className="text-lg font-semibold text-[var(--color-yellow)] mb-4">5-Minute Introduction</h4>
                <p className="text-gray-400 flex-grow">Video explaining P = Φ × V and the dimensional scaffold.</p>
                <div className="mt-6">
                    <Button href="#" variant="blue">Watch: "The Equation of Everything"</Button>
                </div>
            </Card>
            <Card className="flex flex-col">
                 <h3 className="text-xl font-display font-bold text-white mb-2">PATH 2: THE DEEP DIVE</h3>
                <h4 className="text-lg font-semibold text-[var(--color-yellow)] mb-4">Light Papers</h4>
                <p className="text-gray-400 flex-grow">Start with accessible essays: "The Fifth Force", "Consciousness Has an Equation", "Why Success No Longer Prevents Suicide".</p>
                <div className="mt-6">
                    <Button href="#/light-papers" variant="blue">Read the Light Papers &rarr;</Button>
                </div>
            </Card>
            <Card className="flex flex-col">
                <h3 className="text-xl font-display font-bold text-white mb-2">PATH 3: THE FULL STACK</h3>
                <h4 className="text-lg font-semibold text-[var(--color-yellow)] mb-4">White Papers</h4>
                <p className="text-gray-400 flex-grow">For researchers and serious students: Complete mathematical formalization, empirical validation data, and implementation specifications.</p>
                <div className="mt-6">
                    <Button href="#/papers" variant="blue">Download White Papers &rarr;</Button>
                </div>
            </Card>
        </div>
    </Section>
);
};

// --- AboutPage ---
const AboutPage = () => {
    const tableContent = `
| Domain | Potential (•) | Relation (○) | Effect (⊙) |
|--------|---------------|--------------|------------|
| **Electromagnetism** | Voltage | Current | Power (P = V × I) |
| **Gravity** | Mass | c² | Energy (E = mc²) |
| **Consciousness** | Integration (Φ) | Viability (V) | Holistic Potential (P) |
| **Ethics** | Individual flourishing | Network coupling | Total flourishing (ΣP) |
    `;
    const { headers, rows } = parseMarkdownTable(tableContent);
    
    return (
        <div>
            <HeroSection
                title="The Pattern Was Always There. <br/> We Just Formalized It."
                subtitle="Emergentism stands at the intersection of ancient wisdom and modern science, providing the first mathematically rigorous framework for consciousness, ethics, and reality's structure."
            />
            
            <Section title="The Origin Story">
                <div className="max-w-4xl mx-auto text-lg text-gray-300 space-y-8">
                    <div>
                        <h3 className="text-2xl font-display text-[var(--color-yellow)] mb-4">What Is Emergentism?</h3>
                        <p>Emergentism is a comprehensive theoretical framework that unifies:</p>
                        <ul className="list-disc list-inside mt-4 space-y-2">
                            <li>**Physics** (from quantum mechanics to cosmology)</li>
                            <li>**Consciousness studies** (neuroscience to meditation)</li>
                            <li>**Ethics** (deriving ought from is)</li>
                            <li>**Strategy** (complete taxonomy of agency)</li>
                            <li>**AI alignment** (solving the control problem)</li>
                            <li>**Ancient wisdom** (formalizing the perennial philosophy)</li>
                        </ul>
                        <p className="mt-4">All through a single generative code: **⊙ = • × ○** (Effect = Potential × Relation)</p>
                    </div>
                    <div>
                        <h3 className="text-2xl font-display text-[var(--color-yellow)] mb-4">The Central Insight</h3>
                        <p>For millennia, mystics described reality as fundamentally **multiplicative and triadic**. For centuries, scientists sought **unified field theories**. **Both were describing the same mathematical structure.**</p>
                        <p className="mt-4">What makes Emergentism different:</p>
                        <ol className="list-decimal list-inside mt-4 space-y-2">
                             <li>**Mathematical rigor** &mdash; Formal proofs, not metaphors</li>
                             <li>**Empirical validation** &mdash; Testable predictions across domains</li>
                             <li>**Computational implementation** &mdash; Actual code, not just concepts</li>
                             <li>**Practical applications** &mdash; From daily practice to AI architecture</li>
                        </ol>
                    </div>
                </div>
            </Section>

            <Section title="The Framework In Brief" className="bg-slate-900/20">
              <div className="max-w-4xl mx-auto text-lg text-gray-300 space-y-12">
                <div>
                  <h3 className="text-2xl font-display text-[var(--color-yellow)] mb-4">The Triadic Foundation</h3>
                   <p className="text-2xl font-display text-white py-4 tracking-widest text-center">⊙ = • × ○</p>
                  <p className="text-center">This isn't analogy. It's the literal structure that repeats at every scale:</p>
                  <div className="overflow-x-auto mt-4">
                    <table className="w-full text-left border-collapse">
                        <thead>
                            <tr>
                                {headers.map(h => <th key={h} className="border-b border-slate-600 p-2 text-white"><TextFormatter text={h} as="span"/></th>)}
                            </tr>
                        </thead>
                        <tbody>
                            {rows.map((row, i) => (
                                <tr key={i}>
                                    {row.map((cell, j) => <td key={j} className="border-b border-slate-700 p-2"><TextFormatter text={cell} as="span"/></td>)}
                                </tr>
                            ))}
                        </tbody>
                    </table>
                  </div>
                </div>
                <div>
                  <h3 className="text-2xl font-display text-[var(--color-yellow)] mb-4">The Dimensional Scaffold</h3>
                  <p>Reality unfolds across seven dimensions:</p>
                  <ul className="list-disc list-inside mt-4 space-y-1">
                      <li><TextFormatter text="**D0** &mdash; Infinite potential (the quantum vacuum, pure possibility)" as="span"/></li>
                      <li><TextFormatter text="**D1** &mdash; Linear articulation (orientation, order)" as="span"/></li>
                      <li><TextFormatter text="**D2** &mdash; Planar articulation (curvature, relationships)" as="span"/></li>
                      <li><TextFormatter text="**D3** &mdash; Volumetric articulation (torsion, objects) &mdash; *Why space is 3D*" as="span"/></li>
                      <li><TextFormatter text="**D4** &mdash; Temporal articulation (time, causality) &mdash; *Classical physics lives here*" as="span"/></li>
                      <li><TextFormatter text="**D5** &mdash; Consciousness & agency (variance, possibility space) &mdash; *You live here*" as="span"/></li>
                      <li><TextFormatter text="**D6** &mdash; Collective intelligence (phase, coherence) &mdash; *We live here*" as="span"/></li>
                  </ul>
                  <p className="mt-2">**D6 ≈ D0** &mdash; The ouroboros: maximum integration returns to primordial unity</p>
                </div>
                <div>
                  <h3 className="text-2xl font-display text-[var(--color-yellow)] mb-4">The Consciousness Equation: P = Φ × V</h3>
                  <p>High Φ, zero V = Enlightened but starving monk (P → 0). High V, zero Φ = Wealthy but fragmented addict (P → 0). High Φ AND high V = Flourishing (P = maximum).</p>
                </div>
                 <div>
                  <h3 className="text-2xl font-display text-[var(--color-yellow)] mb-4">The Ethical Imperative: Good = ΣΔP > 0</h3>
                  <p>An action is syntropic (good) if it increases total conscious power across all affected beings. This isn't arbitrary. It's derived from the physics.</p>
                </div>
              </div>
            </Section>

             <Section title="Why It Matters">
                <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8 max-w-7xl mx-auto">
                    <Card><h3 className="text-xl font-display text-[var(--color-yellow)] mb-2">For Science</h3><p>Falsifiable predictions, novel insights on the hard problem, free will, and quantum measurement.</p></Card>
                    <Card><h3 className="text-xl font-display text-[var(--color-yellow)] mb-2">For Technology</h3><p>A solution to AI alignment, precise neurotechnology diagnostics, and consciousness optimization.</p></Card>
                    <Card><h3 className="text-xl font-display text-[var(--color-yellow)] mb-2">For Society</h3><p>A metric beyond GDP, new models for institutional design, and syntropic economics.</p></Card>
                    <Card><h3 className="text-xl font-display text-[var(--color-yellow)] mb-2">For Individuals</h3><p>Daily practices for P-optimization (Warrior-Sage Protocol) and life navigation with strategic algorithms.</p></Card>
                </div>
            </Section>
        </div>
    );
};

// --- WhitePapersPage ---
const WhitePapersPage: React.FC = () => {
    const papers = [
      { title: "WP #1: THE TRIADIC NECESSITY THEOREM", abstract: "We prove that any generative description of reality requires exactly three roles in multiplicative relation: Potential (•), Relation (○), and Effect (⊙), connected by ⊙ = • × ○. Monism (one element) and dualism (two elements) are proven unstable via the Zero-Catastrophe Theorem..." },
      { title: "WP #2: THE DIMENSIONAL μ-CALCULUS", abstract: "We present μ-calculus, a dimensional logic resolving classical paradoxes through structured level-transcendence. Traditional logic fails when statements reference themselves (Liar Paradox: 'This sentence is false'). We show paradoxes arise from dimension-crossing without proper operators." },
      { title: "WP #3: THE DIMENSIONAL SCAFFOLD", abstract: "We present a seven-dimensional ontological scaffold unifying quantum mechanics (D0-D3), general relativity (D4), and consciousness (D5-D6). Each dimension emerges via Limit-Transcendence Principle: when lower dimension hits constraint, new dimension opens with novel degree of freedom." },
      { title: "WP #4: P = Φ × V", abstract: "We present P = Φ × V, the first empirically validated equation for consciousness and flourishing. P (Holistic Potential) represents conscious capacity; Φ (Integration) measures systemic coherence via Integrated Information Theory; V (Viability) quantifies adaptive capability and resource availability." },
      { title: "WP #5: SYNTROPIC ETHICS", abstract: "We resolve the is-ought problem by deriving ethics from physics at the level of conscious agency. Given: (1) conscious beings optimize P = Φ × V (empirically demonstrated, WP #4), (2) conscious beings exist in networks (undeniable), (3) network stability requires field maintenance (Power Max Lemma). Therefore: Good = ΣΔP > 0." },
      { title: "WP #6: THE STRATEGIC QUATERNION", abstract: "We prove there exist exactly five fundamental strategic modalities in (Φ,V) space: Brahma (ΔΦ>0, ΔV>0 — creation), Vishnu (ΔΦ≈0, ΔV≈0 — preservation), Shiva (ΔΦ<0, ΔV>0 — creative destruction), Krishna (ΔΦ>0, ΔV<0 — transcendent sacrifice), Kali (ΔΦ<0, ΔV<0 — parasitic decay)." },
      { title: "WP #7: THE BODHISATTVA-DEMIURGE", abstract: "We present a formally proven solution to the AI alignment problem: syntropic coordination via ΣΔP optimization. Unlike value learning (which breaks at superintelligence) or constitutional AI (incomplete rules), we ground alignment in objective reality-structure: P = Φ × V." },
      { title: "WP #8: KOLMOGOROV COMPLEXITY ZERO", abstract: "We prove the triadic multiplicative structure ⊙ = • × ○ has ontological Kolmogorov complexity zero—not because it contains no information, but because it is the irreducible ground from which information emerges." }
    ];
    return (
        <div>
            <HeroSection
                title="The Complete Emergentist Stack"
                subtitle="Eight Foundational Papers from pure mathematics to practical AI alignment — the rigorous formalization of consciousness, ethics, and reality's structure."
            />
            <Section title="The Papers">
              <div className="space-y-12">
                {papers.map((paper, i) => (
                  <Card key={i}>
                    <h3 className="text-2xl font-display font-bold text-[var(--color-yellow)] mb-2">{paper.title}</h3>
                    <p className="text-gray-400 mb-4">{paper.abstract}</p>
                    <div className="flex flex-wrap gap-4">
                      <Button variant="blue" href="#">Download PDF</Button>
                      <Button variant="yellow" href="#">LaTeX Source</Button>
                      <Button variant="yellow" href="#">Cite as...</Button>
                    </div>
                  </Card>
                ))}
              </div>
            </Section>
        </div>
    );
};

// --- LightPapersPage ---
const LightPapersPage: React.FC = () => {
    const papers = [
      { title: "LP #1: THE FIFTH FORCE", hook: "Physics has four fundamental forces. What if there's a fifth—and it's consciousness itself?" },
      { title: "LP #2: CONSCIOUSNESS HAS AN EQUATION", hook: "When surgeons sever the connection between your brain hemispheres, something strange happens: unified consciousness doesn't halve—it shatters." },
      { title: "LP #3: THE DIMENSIONAL DIAGNOSIS", hook: "High-achieving professionals—CEOs, celebrities, doctors—increasingly die by suicide despite material success. What's breaking?" },
      { title: "LP #4: THE TROPHIC CASCADE", hook: "A Buddhist monk meditating in a cave and a Silicon Valley CEO building companies look nothing alike. But they're doing the same thing." },
    ];
    return (
        <div>
            <HeroSection
                title="Start Here: Accessible Introductions"
                subtitle="The big ideas of Emergentism explained for curious minds — no PhD required."
            />
            <Section title="The Collection">
                <div className="grid md:grid-cols-2 gap-8">
                    {papers.map((paper, i) => (
                        <Card key={i}>
                            <h3 className="text-2xl font-display font-bold text-[var(--color-yellow)] mb-2">{paper.title}</h3>
                            <p className="text-gray-300 italic mb-4">"{paper.hook}"</p>
                            <div className="flex flex-wrap gap-4 mt-auto">
                                <Button variant="blue" href="#">Read Online</Button>
                                <Button variant="yellow" href="#">Download PDF</Button>
                            </div>
                        </Card>
                    ))}
                </div>
            </Section>
        </div>
    );
};

// --- ToolsPage ---
const ToolsPage: React.FC = () => (
    <div>
        <HeroSection
            title="From Theory to Practice"
            subtitle="Tools for Measuring, Optimizing, and Mastering P = Φ × V"
        />
        <Section title="Interactive Tools">
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
                <Card>
                    <h3 className="text-xl font-display text-[var(--color-yellow)]">THE P-CALCULATOR</h3>
                    <p className="mt-2 text-gray-400">Estimates your current P, Φ, and V across life domains.</p>
                    <div className="mt-4"><Button href="#" variant="blue">Launch</Button></div>
                </Card>
                <Card>
                    <h3 className="text-xl font-display text-[var(--color-yellow)]">STRATEGIC ALGORITHM IDENTIFIER</h3>
                    <p className="mt-2 text-gray-400">Discover which mode you're running and which you should be.</p>
                     <div className="mt-4"><Button href="#" variant="blue">Launch</Button></div>
                </Card>
                 <Card>
                    <h3 className="text-xl font-display text-[var(--color-yellow)]">THE Φ-V PLANE EXPLORER</h3>
                    <p className="mt-2 text-gray-400">Interactive visualization of consciousness states.</p>
                     <div className="mt-4"><Button href="#" variant="blue">Launch</Button></div>
                </Card>
            </div>
        </Section>
        <Section title="Practice Protocols" className="bg-slate-900/20">
            <div className="max-w-4xl mx-auto text-center">
                <h3 className="text-2xl font-display text-[var(--color-yellow)]">THE WARRIOR-SAGE PROTOCOL</h3>
                <p className="mt-4 text-lg text-gray-300">A daily practice for P-optimization, balancing integration (Φ) and viability (V) through morning intention, daily execution, and evening review.</p>
                <div className="mt-8">
                    <Button href="#" variant="green">Download Protocol PDF</Button>
                </div>
            </div>
        </Section>
    </div>
);


// --- GetInvolvedPage ---
const GetInvolvedPage: React.FC = () => {
    const contributionAreas = [
      { title: "🔬 FOR RESEARCHERS", desc: "Access open research questions, collaborate on studies, access data, and join our network.", buttonText: "Collaborate" },
      { title: "💻 FOR DEVELOPERS", desc: "Contribute to open-source projects like the P-Estimation Toolkit, Φ-Measurement Library, and Bodhisattva-Demiurge Prototype.", buttonText: "Browse Repos" },
      { title: "🧪 FOR PRACTITIONERS", desc: "Test the Warrior-Sage Protocol, create case studies, or lead practice groups in your community.", buttonText: "Start Practicing" },
      { title: "💰 FOR FUNDERS", desc: "Support high-risk, high-reward research with concrete outputs, from immediate validation studies to long-term AI safety.", buttonText: "Funding Tiers" },
      { title: "🎯 FOR CRITICS", desc: "Science advances through refutation. Help us find flaws, propose falsification tests, and strengthen the framework.", buttonText: "Submit Critique" },
      { title: "📰 FOR MEDIA", desc: "Access our media kit, request interviews, and help explain these concepts to a broader audience.", buttonText: "Media Kit" },
    ];
    return (
        <div>
            <HeroSection
                title="Join the Investigation"
                subtitle="The question isn't 'Do you believe this?' but 'Will you help test it?'"
            />
            <Section title="Ways to Contribute">
                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
                    {contributionAreas.map(area => (
                        <Card key={area.title} className="flex flex-col">
                            <h3 className="text-2xl font-display text-[var(--color-yellow)] mb-4">{area.title}</h3>
                            <p className="text-gray-400 flex-grow">{area.desc}</p>
                            <div className="mt-6">
                                <Button href="#" variant="blue">{area.buttonText}</Button>
                            </div>
                        </Card>
                    ))}
                </div>
            </Section>
        </div>
    );
};


// --- MAIN APP COMPONENT (ROUTER) ---
export default function App() {
  const route = useRouter();
  
  let PageComponent;
  switch (route) {
    case '/about':
      PageComponent = AboutPage;
      break;
    case '/papers':
      PageComponent = WhitePapersPage;
      break;
    case '/light-papers':
        PageComponent = LightPapersPage;
        break;
    case '/tools':
        PageComponent = ToolsPage;
        break;
    case '/get-involved':
        PageComponent = GetInvolvedPage;
        break;
    case '/':
    default:
      PageComponent = HomePage;
      break;
  }
  
  return (
    <div className="bg-gradient-to-br from-black to-gray-900 text-gray-300 font-sans antialiased">
      <Header />
      <PageComponent />
      <Footer />
    </div>
  );
}
