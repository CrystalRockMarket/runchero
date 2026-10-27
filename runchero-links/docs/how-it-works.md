# How Runchero Links works

Runchero Links is a small, stateless tool that adds the community's Amazon
Associate tag to links. It does not redirect, shorten, hide, or track anything.

## The conversion

1. **Check the address.** Only Amazon US addresses are accepted: `amazon.com`
   and its `www`, `m`, and `smile` subdomains. Short hosts `a.co` and `amzn.to`
   are resolved first.
2. **Find the useful part.** Product links are reduced to the 10-character
   product ID (ASIN). Search links keep the search words and department.
3. **Remove clutter.** Referral, campaign, session, and tracking parameters are
   stripped.
4. **Add the tag.** The link is rebuilt with `tag=runchero-20` and nothing else.
5. **Hand it back.** The page shows the clean link, a copy button, and an open
   button.

| Before | After |
| --- | --- |
| `amazon.com/Some-Name/dp/B08N5WRWNW/ref=sr_1_1?qid=123&th=1` | `amazon.com/dp/B08N5WRWNW?tag=runchero-20` |
| `amazon.com/s?k=canning+jars&ref=nb_sb_noss` | `amazon.com/s?k=canning%20jars&tag=runchero-20` |

## Short links

`a.co` and `amzn.to` addresses do not contain the product ID. The server follows
the shortcut, checking that every redirect stays inside an Amazon-owned host,
then converts the final page. It gives up after five redirects or five seconds.
If the shortcut service cannot be reached, paste the full product link instead.

## Earnings

Amazon pays a percentage of the price of qualifying purchases made after someone
follows a tagged link. The rate depends on the category and changes over time.
The estimator lets a visitor try different assumptions:

- $60 order at 3% = $1.80
- ten qualifying orders a month = $18.00
- twelve months at that pace = $216.00

These are illustrations. Not every click leads to a purchase, not every purchase
qualifies, returns can reverse a commission, and Amazon can change the rate card
or the programme rules at any time.

## Privacy

- No accounts, cookies, analytics, or history.
- Pasted links are converted in memory, not written to a database.
- Server logs record the page and status, not the links or search terms.
- Short-link lookups are rate limited per device.

## Rules we follow

- **Disclosure.** The affiliate relationship is stated in the footer and next to
  the tool.
- **No cloaking.** Links point straight at Amazon with the tag visible, not
  through a redirect.
- **No shortening.** Amazon's Operating Agreement does not allow masking or
  shortening affiliate links.
- **Honest estimates.** Earnings figures are labelled as estimates and the rate
  is adjustable.

## Limits

- Amazon US (`amazon.com`) only for now.
- Up to 50 links per conversion.
- Short-link resolution needs an internet connection.
- The tag is a demo value until `RLK_AFFILIATE_TAG` is set to the real Associate
  tag.
