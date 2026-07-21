"use client";

import { useState } from "react";
import { Sparkles, Check } from "lucide-react";

export default function PricingPage() {
  const [isLoading, setIsLoading] = useState(false);
  const [note, setNote] = useState<string | null>(null);
  const clerkPublishableKey = process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY ?? "";
  const isAuthConfigured = /^pk_(test|live)_[A-Za-z0-9_-]{20,}/.test(clerkPublishableKey);

  const handleSubscribe = async () => {
    if (!isAuthConfigured) {
      return;
    }

    setIsLoading(true);
    try {
      const res = await fetch('/api/stripe/checkout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ priceId: 'default' })
      });

      if (res.status === 401) {
        window.location.href = '/sign-in?redirectUrl=/pricing';
        return;
      }

      const data = await res.json().catch(() => ({}));
      if (data.url) {
        window.location.href = data.url;
      } else {
        setNote(data.error || 'SKYZAI Pay integration pending (η=0).');
        setIsLoading(false);
      }
    } catch (e) {
      console.error(e);
      setIsLoading(false);
    }
  };

  const handleSignIn = () => {
    if (isAuthConfigured) {
      window.location.href = '/sign-in?redirectUrl=/pricing';
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-6 py-24">
      <div className="text-center mb-16">
        <h1 className="font-serif text-4xl md:text-6xl text-[#c7a474] mb-6">The Infinite Play</h1>
        <p className="text-xl text-white/70 max-w-2xl mx-auto">
          The canonical book is free forever. To unlock the recursive AI expansion engine, upgrade to the Explorer tier.
        </p>
      </div>

      <div className="grid md:grid-cols-2 gap-8 max-w-3xl mx-auto">
        {/* Free Tier */}
        <div className="p-8 rounded-lg border border-white/10 bg-white/5 flex flex-col">
          <h2 className="text-2xl font-serif mb-2">Canonical Reader</h2>
          <div className="text-3xl font-bold mb-6">Free</div>
          <ul className="space-y-4 mb-8 flex-1">
            <li className="flex items-center gap-3 text-white/80">
              <Check className="w-5 h-5 text-[#c7a474]" /> Read the full 31k-word canon
            </li>
            <li className="flex items-center gap-3 text-white/80">
              <Check className="w-5 h-5 text-[#c7a474]" /> Access all public L1-L7 mappings
            </li>
            <li className="flex items-center gap-3 text-white/80">
              <Check className="w-5 h-5 text-[#c7a474]" /> 3 Free AI Expansions
            </li>
          </ul>
          <button
            disabled
            onClick={handleSignIn}
            className="w-full py-3 px-4 rounded bg-white/10 text-white/50 cursor-not-allowed font-medium"
          >
            Current Plan
          </button>
        </div>

        {/* Explorer Tier */}
        <div className="p-8 rounded-lg border border-[#c7a474]/50 bg-[#c7a474]/5 flex flex-col relative overflow-hidden">
          <div className="absolute top-0 right-0 bg-[#c7a474] text-[#0a0a0a] text-xs font-bold px-3 py-1 uppercase tracking-wider rounded-bl">
            Premium
          </div>
          <h2 className="text-2xl font-serif mb-2 text-[#c7a474]">Explorer</h2>
          <div className="text-3xl font-bold mb-6">$9<span className="text-lg text-white/50 font-normal">/mo</span></div>
          <ul className="space-y-4 mb-8 flex-1">
            <li className="flex items-center gap-3 text-white/90">
              <Check className="w-5 h-5 text-[#c7a474]" /> Everything in Free
            </li>
            <li className="flex items-center gap-3 text-white/90">
              <Check className="w-5 h-5 text-[#c7a474]" /> 500 AI Expansions per month
            </li>
            <li className="flex items-center gap-3 text-white/90">
              <Check className="w-5 h-5 text-[#c7a474]" /> Private branch history
            </li>
            <li className="flex items-center gap-3 text-white/90">
              <Check className="w-5 h-5 text-[#c7a474]" /> Powered by Claude Sonnet 4.6
            </li>
          </ul>
          <button
            onClick={handleSubscribe}
            disabled={isLoading || !isAuthConfigured}
            className="w-full py-3 px-4 rounded bg-[#c7a474] hover:bg-[#d4b589] text-[#0a0a0a] font-bold transition-colors flex items-center justify-center gap-2 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {!isAuthConfigured ? 'Provider Not Configured' : isLoading ? 'Redirecting...' : (
              <>
                <Sparkles className="w-5 h-5" />
                Subscribe Now
              </>
            )}
          </button>
          {note && <p className="mt-3 text-center text-sm text-white/60">{note}</p>}
        </div>
      </div>
    </div>
  );
}
