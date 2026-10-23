# Conversion plan

The shop sells real food to real neighbors. The goal is that a shopper who
knows what they want can get it in a minute, and a shopper who does not know
what they want can figure it out. Everything here has to stay true to the
promise: **under the local shelf, cut for the table.**

## What is already in place

| Idea | Where |
| --- | --- |
| Market benchmark on every cut, with the source and date shown | `/cut/<slug>` |
| Honest savings badge, "before packing options" | `/cut/<slug>`, cart |
| Packing choices visible and priced before checkout | cut page, cart, checkout |
| Free delivery threshold shown as progress, not a surprise | cart |
| Minimum order gap shown with the amount still needed | cart |
| Pinned call to action on a phone | cut page |
| Four reassurance points next to the decision | cut, cart, checkout |
| Related cuts from the same primal | cut page |
| Whole cow drop pages with live availability | `/campaigns` |
| Standing orders and self service pause, skip, cancel | `/manage/<token>` |
| Account with saved defaults, order history, and guest-order matching | `/account` |
| Market price table with source and observation date | `/market-prices` |
| Data provenance explainer, linked from the footer | `/data-sources` |
| Landing funnel: fill-the-freezer first, then deals and favorites | `/` |
| Sort control on the shop, including biggest savings | `/shop` |

## The next three moves, in order

**1. Cut page to cart rate.** Most of the traffic will land on a cut page
and leave for the cart. The measure is add to cart presses per cut page
view. The lever, if the rate is low, is the pack size choice: it is the one
decision on the page that can go wrong, because a shopper does not know what
"5 lb vacuum pack" means for their freezer. The fix is wording, not a
default change. Keep the default preselected.

**2. Cart abandonment at the minimum order.** The $99 minimum is real, so
the cart says exactly how much more is needed. If shoppers leave there, the
lever is offering a small top up item near the gap, like a pound of ground
beef or a pack of stew meat, rather than lowering the minimum.

**3. Repeat rate on standing orders.** A third of the revenue should be
subscriptions. The lever is the cutoff: the weekly cut day needs to land
before the household plans its meals. If skips are high, move the cutoff
earlier in the day rather than adding a reminder email, because a reminder
for a cutoff the shopper missed is just noise.

## What we will not do

These are not oversights. They are the lines.

- **No fake reviews or testimonials.** We have no customers yet, and
  invented quotes are the fastest way to lose a farmer's customers.
- **No fake scarcity.** A countdown timer on stock that is not limited is a
  lie, and this shop sells food to people who can call the farm.
- **No hidden fees.** Packing, delivery, and the tax note are all on the
  screen before the shopper commits.
- **No prechecked subscription.** Standing orders have to be a deliberate
  choice, in a form that says what it will cost.
- **No email list sold or data shared.** The shop sends nothing but order
  and cut sheet mail.
- **No dark patterns.** No countdown, no "only 2 left" without a real
  count, no preselected add on, no trick wording on the cancel button.

## Measuring it

The shop records orders, not people. There is no tracking pixel and no
third party analytics. The numbers that matter come out of the database:

```sql
-- orders per day
SELECT date(created_at) AS day, count(*) AS orders
FROM orders GROUP BY day ORDER BY day DESC;

-- the cut people buy most often
SELECT c.name, count(oi.id) AS lines, sum(oi.qty) AS qty
FROM order_items oi JOIN cuts c ON c.id = oi.ref_id
WHERE oi.item_type = 'cut'
GROUP BY c.name ORDER BY qty DESC LIMIT 10;

-- packing choices that get picked, per order
SELECT json_extract(value, '$.code') AS choice, count(*) AS orders
FROM orders, json_each(orders.packing_json)
WHERE json_extract(value, '$.group') = 'wrap'
GROUP BY choice ORDER BY orders DESC;

-- standing orders that are still active
SELECT count(*) FROM subscriptions WHERE status = 'active';
```

Volume is small enough that these are read by eye, weekly. The shop's own
`price_audits` and `audit_log` tables already keep a record of every change
made in the admin console, so the answer to "when did that price change" is
always a query away.
