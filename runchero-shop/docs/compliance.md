# Compliance notes

Short version: the shop is built so that it never sells more than a single
household is allowed to buy, never claims a price it cannot back up, and
never hides a fee until checkout.

## Beef for home use

Beef sold for use in the household is exempt from state sales tax in
Kentucky. That exemption, in 9 CFR 303.1(d), comes with two limits:

- **No single sale may be more than half of a carcass.** A household cannot
  buy a whole cow's worth of beef in one order and call it a sale to
  households.
- **At least 75% of the carcass must be sold to households.** The remainder
  can go to restaurants or retailers, but the household share has to be the
  bulk of the animal.

How the shop honors this:

- A whole cow is a **campaign**, not a product. It is split into a
  `household_target` number of shares, so no household ever holds more than
  half a carcass.
- The share size is checked against the carcass weight. The campaign state
  reports `max_share_lbs` (half the carcass) and `min_household_lbs` (75% of
  the carcass), and the campaign page shows the household share against both.
- The campaign page says plainly that one sale may not be more than half a
  carcass and that three quarters has to go to households.
- A household takes one share, with its own order and its own cut sheet.

## Prices and claims

Every price in the shop comes from somewhere and can be traced:

- The base price of each cut is set in the admin console, and each change is
  written to `price_audits` with the before and after numbers.
- A cut can point at a market series. When the series is fresh, the shop
  shows the market price and a savings badge comparing the cut price to
  that benchmark.
- The badge always says the comparison is made **before packing options**.
  Packing is priced per pound or per item and changes the total, so the
  badge must not pretend to cover it.
- When the market series is missing or stale, the shop shows the price
  without a benchmark rather than inventing one.
- The shop does not scrape chain store prices. Where a local price is
  needed, a human enters it in `/admin/market` and it is stored in
  `local_observations` with a date and a source note.

## Payments

The default provider is `mock`. It never contacts a card network and never
charges anybody. Every surface that could be mistaken for a real payment
says so:

- the checkout button says it is a demo and no card is charged,
- the receipt says the order is a mock payment,
- the order list in the admin console labels it `mock`.

With `RBS_PAYMENT_PROVIDER=stripe` and a secret key, the same checkout
talks to Stripe's REST API over `urllib`. The mock labels are not shown when
the provider is real.

## Fees, shown early

- Packing charges appear on the cart page and on the cut page, before
  checkout. The default choices are preselected but the shopper can see
  what they cost and change them.
- Delivery is $15, free over $159, and the threshold is on the cart page.
- The minimum order is $99. The cart says how far away it is rather than
  failing silently at checkout.

## Marketing

The site is a local farm store. There is no email list sold, no data sold,
and no third party tracking. Social links are plain links to the farm's own
pages. The only outbound calls the shop makes are to USDA price feeds, and
they carry no customer data.

## Tax

Prices shown are pre tax. Kentucky beef for home use is tax exempt, so
orders are written with a tax total of zero and the site links the
exemption on the checkout and in the terms rather than leaving it implicit.
The tax total is stored on every order, so a future taxable sale can be
recorded without changing the order table.
