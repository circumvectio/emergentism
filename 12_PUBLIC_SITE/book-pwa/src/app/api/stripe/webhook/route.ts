import { NextResponse } from 'next/server';
import Stripe from 'stripe';
import { prisma } from '@/lib/prisma';
import { headers } from 'next/headers';

// η=0: Stripe is disabled by default (see the checkout route + feedback_skyzai_pay_not_stripe).
// With checkout off, no sessions exist, so no webhook events arrive; this handler is preserved
// (K3) and no-ops unless ENABLE_STRIPE_CHECKOUT=true. SKYZAI Pay is the canonical rail.
const STRIPE_ENABLED = process.env.ENABLE_STRIPE_CHECKOUT === 'true';

export async function POST(req: Request) {
  if (!STRIPE_ENABLED) {
    return new NextResponse('Stripe disabled under η=0 — SKYZAI Pay is the canonical rail.', { status: 200 });
  }
  const stripe = new Stripe(process.env.STRIPE_SECRET_KEY ?? '', {
    apiVersion: '2026-05-27.dahlia',
  });

  const body = await req.text();
  const h = await headers();
  const signature = h.get('stripe-signature') as string;

  let event: Stripe.Event;

  try {
    event = stripe.webhooks.constructEvent(
      body,
      signature,
      process.env.STRIPE_WEBHOOK_SECRET!
    );
  } catch (error) {
    const message = error instanceof Error ? error.message : 'Invalid webhook signature';
    return new NextResponse(`Webhook Error: ${message}`, { status: 400 });
  }

  const session = event.data.object as Stripe.Checkout.Session;

  if (event.type === 'checkout.session.completed') {
    const userId = session.metadata?.userId;
    if (userId) {
      // Payment-bypass guard: validate what was actually purchased before granting the plan.
      // Never grant on a bare "session completed" — a user could complete a $0/wrong-price session.
      const expectedPriceId = process.env.STRIPE_EXPLORER_PRICE_ID;
      const expectedAmount = 900; // Explorer = $9/mo
      let entitled = false;
      try {
        const lineItems = await stripe.checkout.sessions.listLineItems(session.id, { limit: 1 });
        const purchasedPriceId = lineItems.data[0]?.price?.id;
        entitled = expectedPriceId
          ? purchasedPriceId === expectedPriceId
          : (session.amount_total ?? 0) >= expectedAmount && session.payment_status === 'paid';
      } catch (err) {
        console.error('Stripe line-item validation failed', err);
        entitled = false;
      }

      if (entitled) {
        await prisma.user.update({
          where: { id: userId },
          data: {
            plan: 'Explorer',
            creditsRemaining: 500,
          },
        });

        await prisma.payment.create({
          data: {
            userId: userId,
            provider: 'stripe',
            amount: session.amount_total || expectedAmount,
            plan: 'Explorer',
            status: 'completed',
          }
        });
      }
    }
  }

  return new NextResponse('OK', { status: 200 });
}
