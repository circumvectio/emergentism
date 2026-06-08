import { NextResponse } from 'next/server';
import { auth } from '@clerk/nextjs/server';
import Stripe from 'stripe';
import { prisma } from '@/lib/prisma';

// η=0 / SKYZAI Pay canon (see memory feedback_skyzai_pay_not_stripe): a third-party
// card processor extracts a fee and is not the sovereign rail. Stripe checkout is
// DISABLED by default and only re-enables behind ENABLE_STRIPE_CHECKOUT=true. The
// integration below is preserved, not erased (K3 — tombstone). SKYZAI Pay is canonical.
const STRIPE_CHECKOUT_ENABLED = process.env.ENABLE_STRIPE_CHECKOUT === 'true';

export async function POST(req: Request) {
  try {
    if (!STRIPE_CHECKOUT_ENABLED) {
      return NextResponse.json(
        {
          error: 'Card checkout is disabled under the η=0 constraint. SKYZAI Pay is the canonical rail (integration pending).',
          code: 'eta_zero_skyzai_pay_pending',
        },
        { status: 501 },
      );
    }
    const stripe = new Stripe(process.env.STRIPE_SECRET_KEY ?? '', {
      apiVersion: '2026-05-27.dahlia',
    });

    const { userId } = await auth();
    if (!userId) {
      return new NextResponse('Unauthorized', { status: 401 });
    }

    // Lazy sync user
    let user = await prisma.user.findUnique({ where: { id: userId } });
    if (!user) {
      user = await prisma.user.create({
        data: {
          id: userId,
          email: `${userId}@placeholder.com`,
          plan: 'Free',
          creditsRemaining: 3
        }
      });
    }

    // Create Checkout Session.
    // Server-decided price only — never trust a client-supplied price id (payment-bypass guard).
    const explorerPriceId = process.env.STRIPE_EXPLORER_PRICE_ID;
    const lineItem = explorerPriceId
      ? {
          price: explorerPriceId,
          quantity: 1,
        }
      : {
          price_data: {
            currency: 'usd',
            product_data: {
              name: 'The Infinite Book - Explorer Plan',
              description: '$9/mo for up to 500 AI branches.',
            },
            unit_amount: 900,
            recurring: {
              interval: 'month' as const,
            },
          },
          quantity: 1,
        };

    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      line_items: [lineItem],
      mode: 'subscription',
      success_url: `${req.headers.get('origin')}/book/the-point?success=true`,
      cancel_url: `${req.headers.get('origin')}/pricing?canceled=true`,
      client_reference_id: userId,
      metadata: {
        userId: userId,
      }
    });

    return NextResponse.json({ url: session.url });
  } catch (error) {
    console.error("Stripe Checkout failed", error);
    return NextResponse.json({ error: 'Checkout failed' }, { status: 500 });
  }
}
