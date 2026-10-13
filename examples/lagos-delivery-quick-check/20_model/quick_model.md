# Quick model: Lagos same-day parcel delivery

Agent: Quick Modeller
Mode: Quick Check
Date: 2026-10-13
Currency and rate: NGN; 1 USD = 1,331 NGN, as of 2026-10-12 (from 00_brief.md)
Evidence mix: 9 [S], 88 [E], 103 [A] (counted in the whole file, including this line)

Founder cash is NGN 18,000,000 (USD 13,524) [E] (18,000,000 / 1,331, amount from 00_brief.md); no outside money is promised. Prices are held flat in naira, so costs and fees are assumed to rise together.

## Key numbers

All figures are [E] (formulas in the sections below) unless marked. A parcel is one transaction. Money cells show NGN, then USD in brackets.

| Item | Defensive | Moderate | Optimistic |
|---|---|---|---|
| Contribution per parcel | -937 (USD -0.70) | 88 (USD 0.07) | 1,053 (USD 0.79) |
| Parcels per month, month 6 | 542 | 1,613 | 4,003 |
| Parcels per month, month 12 | 1,098 | 3,896 | 10,844 |
| Parcels per month, month 24 | 2,409 | 12,091 | 42,174 |
| Monthly fixed costs, month 12 | 2,900,000 (USD 2,179) | 2,850,000 (USD 2,141) | 3,320,000 (USD 2,494) |
| Break-even month | never within 24 months | never within 24 months | month 4 |
| Cash to run the 90-day test | 9,817,894 (USD 7,376) | 9,204,917 (USD 6,916) | 6,062,822 (USD 4,555) |
| Cash need (lowest cumulative point, 24 months) | 103,063,886 (USD 77,433) and still falling | 75,794,995 (USD 56,946) and still falling | 6,062,822 (USD 4,555), reached in month 3 |

Moderate earns about NGN 88 (USD 0.07) a parcel after every variable cost, against fixed costs of NGN 2.85 million (USD 2,141) a month at month 12. On these numbers the business does not cover its costs within 24 months in the Defensive or Moderate case. It does in the Optimistic case, which takes the better end of every range at once.

## Assumptions

Brief names: MC = `10_research/market_competition.md`, CD = `10_research/customer_demand.md`, FF = `10_research/founder_fit.md`. Kolonell = [Last-mile delivery in Lagos](https://kolonell.com/en/blog/last-mile-delivery-zones-pricing-lagos-2026) (MC) and [Same-Day Delivery in Lagos](https://kolonell.com/en/blog/same-day-delivery-zones-and-cost-lagos-2026) (CD), a consultancy blog that calls its figures order of magnitude.

| Assumption | Defensive | Moderate | Optimistic | Source or method |
|---|---|---|---|---|
| Delivery fee per parcel, blended (NGN) | 1,500 [S](https://kolonell.com/en/blog/last-mile-delivery-zones-pricing-lagos-2026) | 2,000 [A] | 2,500 [A] | Defensive is the Island fee in MC. Moderate sits between that and the Lekki NGN 2,000 to 3,000 in CD (60% Island at 1,500, 40% Lekki at 2,500 gives 1,900, rounded up). Optimistic is inside the CD range of 1,500 to 3,500. Reason: no rate card found; founder quotes needed. |
| Blended rider cost per delivery (NGN) | 1,600 [E] | 1,400 [E] | 1,200 [E] | Island NGN 1,000 to 1,300 and Ajah NGN 2,000 to 2,500 [S](https://kolonell.com/en/blog/last-mile-delivery-zones-pricing-lagos-2026) (MC), weighted by a zone mix of 60/40, 50/50 and 80/20 Island to outer [A]. Includes the rider's fuel. Glovo riders report NGN 700 to 2,000 an order [S](https://nairametrics.com/2026/05/30/inside-lagos-delivery-boom-riders-risking-everything-to-survive/) (CD). |
| Parcel contents value (NGN) | 18,000 [A] | 18,000 [A] | 18,000 [A] | Typical basket from a guide example in MC. Used only to size the cash-on-delivery fee and losses; it is never revenue. |
| Share of parcels paid by cash on delivery | 60% [A] | 60% [A] | 60% [A] | Share unknown in MC and CD (one report says cash is 23% of online sales, snippet only). Working figure; ask 15 sellers. |
| Cash-on-delivery fee (% of cash collected) | 1.0% [A] | 1.5% [A] | 2.0% [A] | No local price evidence (CD section 4). Founder's idea is a small fee on cash remitted. |
| First-attempt failure rate | 30% [S](https://kolonell.com/en/blog/same-day-delivery-zones-and-cost-lagos-2026) | 22.5% [E] | 15% [S](https://kolonell.com/en/blog/same-day-delivery-zones-and-cost-lagos-2026) | First-attempt success of 70% to 85% (CD). Moderate is the midpoint, 100% - 77.5%. |
| Final refusal of cash parcels | 14% [A] | 10% [A] | 6.5% [E] | Moderate is the 10% working figure in MC. Defensive is 10% plus 40% [A]. Optimistic is 10% x (1 - 35%), taking the midpoint of the 30 to 40% cut from notifying buyers [S](https://kolonell.com/en/blog/last-mile-delivery-zones-pricing-lagos-2026) (MC). |
| Fee waived on a refused parcel; return trip as share of a normal trip | 50%; 50% [A] | 50%; 50% [A] | 50%; 50% [A] | Structural working figures. Reason: a seller will not pay the full fee for an undelivered parcel; the return leg is shorter. |
| Gateway fee on the delivery fee | 1.5% + NGN 10 a parcel [S](https://support.paystack.com/hc/en-us/articles/360009881920-What-are-Paystack-s-transaction-charges) | same | same | 1.5% from the Paystack schedule (MC). The NGN 100 charge is spread over 10 parcels per wallet top-up [A]. Charged on every parcel, which is the cautious reading. |
| Gateway fee on parcel contents | 0 [A] | 0 [A] | 0 [A] | Buyers pay the seller, not the business, except as cash. The business is not the seller of record. |
| Payout transfer to seller (NGN per cash parcel collected) | 25 [A] | 25 [A] | 25 [A] | Daily batch payout; no tariff found. Working figure. |
| Cash deposit and handling (% of cash collected) | 0.3% [A] | 0.3% [A] | 0.3% [A] | Bank deposit charges; no figure found. |
| Cash loss and shrinkage (% of cash collected) | 1.0% [A] | 0.5% [A] | 0.2% [A] | No local data. MC says discrepancies eat margin if riders do not remit daily. |
| Promotions and discounts (% of fee) | 8% [A] | 5% [A] | 3% [A] | Launch credits and volume deals. No data. |
| Lost or damaged parcels, repaid (% of contents value) | 0.6% [A] | 0.3% [A] | 0.15% [A] | No data; business assumed to repay the seller in full. |
| Support and buyer notifications (NGN per parcel) | 60 [A] | 40 [A] | 30 [A] | Messaging cost plus support time; no figure found. |
| Parcels per seller per week sent through the business | 5 [A] | 8 [A] | 12 [A] | Brief says 5 to 50 a week. Sellers keep using their own riders for part of it, so the low end is used. |
| New paying sellers in month 1; monthly growth | 5; 5% [A] | 8; 8% [A] | 12; 10% [A] | Founder-led selling at first. No pilot data. Month 24 new sellers: 15, 47, 107 [E] (n0 x (1+g)^23). |
| Monthly seller churn | 8% [A] | 5% [A] | 3% [A] | CD: sellers switch when a courier fails them; no retention data. |
| Share of a month a new seller is active in the month joined | 50% [A] | 50% [A] | 50% [A] | Mid-month joining. |
| Cost to win one paying seller (NGN) | 40,000 [A] | 27,500 [A] | 15,000 [A] | CD planning band NGN 15,000 to 40,000 [A]. Full range NGN 2,500 to 100,000 [E] (cost per lead NGN 500 to 5,000 [S](https://grey.co/blog/facebook-ads-cost-nigeria) / 5 to 20% lead-to-seller [A]). |
| Founder 1 salary from month 1 (NGN a month) | 600,000 [A] | 600,000 [A] | 600,000 [A] | FF: full-time from month 1. No Lagos pay data in the research; working figure for an operations lead. |
| Founder 2 salary from month 7 (NGN a month) | 900,000 [A] | 900,000 [A] | 900,000 [A] | FF: not full-time in the first 6 months, so month 7 is the earliest. Working figure for a developer. Shown on its own line. |
| Contract developer, months 1 to 6 (NGN a month) | 250,000 [A] | 250,000 [A] | 250,000 [A] | FF: the builder is part-time while the test runs. |
| Cash reconciliation clerk (NGN a month) | 300,000 [A] | 300,000 [A] | 300,000 [A] | FF: no finance owner; cash handling needs one. |
| Dispatcher and support agents (NGN each a month) | 250,000 [A] | 250,000 [A] | 250,000 [A] | One agent per 150 parcels a day (26 operating days a month) [A], minimum one. |
| Tools, hosting, maps and messaging (NGN a month) | 200,000 [A] | 150,000 [A] | 120,000 [A] | No figure found. |
| Hub and cash desk (NGN a month) | 300,000 [A] | 300,000 [A] | 300,000 [A] | Small Lekki space; no figure found. |
| Rider cover, phones and uniforms (NGN a month) | 150,000 [A] | 150,000 [A] | 150,000 [A] | No figure found. |
| Accounting, legal and licences (NGN a month) | 100,000 [A] | 100,000 [A] | 100,000 [A] | Licensing of a cash-remitting service was not checked in MC. |
| Other and contingency (NGN a month) | 100,000 [A] | 100,000 [A] | 100,000 [A] | CD notes rider paperwork and tout harassment costs. |
| One-time set-up and cash float, month 1 (NGN) | 2,000,000 [A] | 2,000,000 [A] | 2,000,000 [A] | 1,500,000 for registration, rider kit and legal review, 500,000 float for late rider deposits [A]. Float is not recovered in the model. |

## Per-transaction waterfall

NGN per booked parcel, USD in brackets. Each line is [E] with the formula shown, built from the inputs above. COD = cash on delivery; cash collected = 60% x (1 - refusal) x 18,000.

| Line | Defensive | Moderate | Optimistic | Formula |
|---|---|---|---|---|
| Delivery fee billed | 1,500.0 (USD 1.127) [E] | 2,000.0 (USD 1.503) [E] | 2,500.0 (USD 1.878) [E] | fee |
| Fee waived on refused cash parcels | -63.0 (USD 0.047) [E] | -60.0 (USD 0.045) [E] | -48.8 (USD 0.037) [E] | fee x 60% x refusal x 50% |
| Cash-on-delivery fee | 92.9 (USD 0.070) [E] | 145.8 (USD 0.110) [E] | 202.0 (USD 0.152) [E] | cash collected x COD fee % |
| Revenue per parcel | 1,529.9 (USD 1.149) [E] | 2,085.8 (USD 1.567) [E] | 2,653.2 (USD 1.993) [E] | sum of the three lines above |
| Rider pay, first trip | -1,600.0 (USD 1.202) [E] | -1,400.0 (USD 1.052) [E] | -1,200.0 (USD 0.902) [E] | rider cost |
| Re-attempt trips | -345.6 (USD 0.260) [E] | -231.0 (USD 0.174) [E] | -133.2 (USD 0.100) [E] | (first-attempt failure - 60% x refusal) x rider cost |
| Return trips, refused parcels | -67.2 (USD 0.050) [E] | -42.0 (USD 0.032) [E] | -23.4 (USD 0.018) [E] | 60% x refusal x 50% x rider cost |
| Payment gateway fee | -32.5 (USD 0.024) [E] | -40.0 (USD 0.030) [E] | -47.5 (USD 0.036) [E] | 1.5% x fee + 10 |
| Payout transfer to seller | -12.9 (USD 0.010) [E] | -13.5 (USD 0.010) [E] | -14.0 (USD 0.011) [E] | 25 x 60% x (1 - refusal) |
| Cash deposit and handling | -27.9 (USD 0.021) [E] | -29.2 (USD 0.022) [E] | -30.3 (USD 0.023) [E] | 0.3% x cash collected |
| Cash loss | -92.9 (USD 0.070) [E] | -48.6 (USD 0.037) [E] | -20.2 (USD 0.015) [E] | loss % x cash collected |
| Promotions and discounts | -120.0 (USD 0.090) [E] | -100.0 (USD 0.075) [E] | -75.0 (USD 0.056) [E] | promo % x fee |
| Refunds for lost or damaged parcels | -108.0 (USD 0.081) [E] | -54.0 (USD 0.041) [E] | -27.0 (USD 0.020) [E] | claim % x 18,000 |
| Support and notifications | -60.0 (USD 0.045) [E] | -40.0 (USD 0.030) [E] | -30.0 (USD 0.023) [E] | per-parcel figure |
| Total variable cost | -2,466.9 (USD 1.853) [E] | -1,998.3 (USD 1.501) [E] | -1,600.6 (USD 1.203) [E] | sum of the ten cost lines |
| **Contribution per parcel** | **-937.1 (USD 0.704)** [E] | **87.5 (USD 0.066)** [E] | **1,052.6 (USD 0.791)** [E] | revenue - total variable cost |

The parcel contents value (NGN 18,000, USD 13.52) is [A] and is not revenue. Contribution is positive in Moderate and Optimistic and negative in Defensive.

## Monthly view

Moderate scenario. Money columns in NGN millions, with USD thousands in brackets. All cells are [E].

| Month | New sellers | Active sellers | Parcels | Revenue | Variable cost | Acquisition | Fixed (month 1 incl. 2.00 one-time) | Result | Cumulative cash |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 8.0 | 8 | 139 | 0.29 (0.2k) | 0.28 (0.2k) | 0.22 (0.2k) | 4.20 (3.2k) | -4.41 (-3.3k) | -4.41 (-3.3k) |
| 3 | 9.3 | 25 | 697 | 1.45 (1.1k) | 1.39 (1.0k) | 0.26 (0.2k) | 2.20 (1.7k) | -2.40 (-1.8k) | -9.20 (-6.9k) |
| 6 | 11.8 | 52 | 1,613 | 3.37 (2.5k) | 3.22 (2.4k) | 0.32 (0.2k) | 2.20 (1.7k) | -2.38 (-1.8k) | -16.36 (-12.3k) |
| 12 | 18.7 | 122 | 3,896 | 8.13 (6.1k) | 7.79 (5.8k) | 0.51 (0.4k) | 2.85 (2.1k) | -3.02 (-2.3k) | -34.51 (-25.9k) |
| 18 | 29.6 | 221 | 7,164 | 14.94 (11.2k) | 14.32 (10.8k) | 0.81 (0.6k) | 3.10 (2.3k) | -3.29 (-2.5k) | -54.18 (-40.7k) |
| 24 | 47.0 | 372 | 12,091 | 25.22 (18.9k) | 24.16 (18.2k) | 1.29 (1.0k) | 3.60 (2.7k) | -3.83 (-2.9k) | -75.79 (-56.9k) |

Formulas, each month t: new sellers = 8 x 1.08^(t-1); active sellers = last month's active x 0.95 + new; parcels = (last month's active x 0.95 + 0.5 x new) x 8 x 52 / 12; revenue = parcels x 2,085.8; variable cost = parcels x 1,998.3; acquisition = new x 27,500; fixed = the lines in Assumptions (month 12: 600,000 + 900,000 + 300,000 + 250,000 + 150,000 + 300,000 + 150,000 + 100,000 + 100,000 = 2,850,000); result = parcels x 87.5 - acquisition - fixed - one-time; cumulative = running sum from zero. Month 24 fixed costs rise to NGN 3.60 million (USD 2,705) because four dispatchers are needed.

## Break-even and cash

| | Defensive | Moderate | Optimistic |
|---|---|---|---|
| Each parcel makes money after variable costs? | no [E] (-937 (USD -0.70)) | yes [E] (88 (USD 0.07)) | yes [E] (1,053 (USD 0.79)) |
| First month contribution covers fixed costs and acquisition | never within 24 months [E] | never within 24 months [E] | month 4 [E] |
| Month-24 result | -5,771,280 (USD -4,336) [E] | -3,833,296 (USD -2,880) [E] | 37,460,548 (USD 28,145) [E] |
| Cash for the 90-day test (months 1 to 3) | 9,817,894 (USD 7,376) [E] | 9,204,917 (USD 6,916) [E] | 6,062,822 (USD 4,555) [E] |
| Cash need before any raise | 103,063,886 (USD 77,433) [E] | 75,794,995 (USD 56,946) [E] | 6,062,822 (USD 4,555) [E] |
| 90-day test as share of the NGN 18,000,000 founder cash | 55% [E] | 51% [E] | 34% [E] |

Cash need is the lowest cumulative monthly result from zero. In Defensive and Moderate it keeps falling at month 24 (monthly losses of NGN 5.77 million (USD 4,336) and NGN 3.83 million (USD 2,880)), so the figure is a floor, not a peak. Against the brief's NGN 18,000,000 (USD 13,524) and no promised money [E]: the 90-day test fits in all three scenarios, but the cash runs out in month 6 (Defensive), month 7 (Moderate) and not at all in Optimistic [E] (first month cumulative result is below -18,000,000). The 90-day cost is mostly fixed: salaries, hub and staff are about NGN 2.2 million (USD 1,653) a month, while Moderate parcels earn NGN 0.06 million (USD 46) in contribution in month 3.

Share of market at month 24 [E] (parcels per month / 433,333 a month, the 5,000 sellers x 20 parcels x 52 / 12 sizing in MC, whose seller count and parcels are [A]): Defensive 2,409 parcels, 0.6%; Moderate 12,091, 2.8%; Optimistic 42,174, 9.7%. The market figure is a screening estimate, so these shares are indicative only.

## What moves the outcome most

Each item is swung alone from the Moderate value to the Defensive one; all other inputs stay at Moderate. Moderate cash need is NGN 75.80 million (USD 56,948) [E]. Every effect is [E] from re-running the model.

| Assumption | Moderate to Defensive | Contribution per parcel | Cash need at 24 months | Change |
|---|---|---|---|---|
| Delivery fee | 2,000 to 1,500 | -365 (USD -0.27) | 128.23m (USD 96.3k) | +52.43m (USD +39.4k) |
| Rider cost | 1,400 to 1,600 | -152 (USD -0.11) | 103.49m (USD 77.8k) | +27.69m (USD +20.8k) |
| First-attempt failure | 22.5% to 30% | -18 (USD -0.01) | 87.96m (USD 66.1k) | +12.17m (USD +9.1k) |
| Cost to win a seller | 27,500 to 40,000 | 88 (unchanged) | 82.47m (USD 62.0k) | +6.68m (USD +5.0k) |

Fee and rider cost decide the result because contribution per parcel is only about NGN 88 (USD 0.07). Volume barely helps at that margin: 5 parcels per seller a week instead of 8 raises the cash need by only NGN 1.05 million (USD 792), and 12 instead of 8 lowers it by only NGN 1.32 million (USD 993) [E]. Upside runs: a fee of NGN 2,400 with everything else Moderate breaks even in month 22; NGN 2,500 in month 19; NGN 2,500 with rider cost at NGN 1,200 in month 14 [E]. Parcels needed a month at month 24 for contribution to cover fixed costs and acquisition at NGN 87.5: 55,905 [E] ((3,600,000 + 1,291,722) / 87.5), 4.6 times Moderate's 12,091 and 12.9% of the sizing market.

## Gaps and assumptions

Almost every figure above is [A]. These move the answer most; the first four are what to close before a test:

- Delivery fee and rider cost [A]/[E]: the research has only one consultancy blog and its two posts disagree (MC and CD). Close it with five courier quotes and five rider quotes for Lekki to Victoria Island and Ajah to Ikoyi.
- Cash-on-delivery share, fee and refusal rate [A]: no local data. Close it by asking 15 sellers what share of parcels are paid in cash, and test a 1% to 2% fee in the pilot.
- Seller volume and churn [A]: 8 parcels a week through the business and 5% monthly churn are guesses. Close them by tracking the first 20 sellers for 8 weeks.
- Cost to win a seller [A]: the NGN 15,000 to 40,000 band has no pilot data. Close it with the NGN 60,000 two-week test described in CD.
- Founder salaries NGN 600,000 and NGN 900,000 a month [A]: the research has no Lagos pay figure. Close it with two quotes for each role from local job listings. Founder 2's start month is 7 because FF says not before month 7.
- Staff, hub, tools, cover, accounting, contingency and set-up [A]: none has a source. Close them with three quotes each for the hub and tools and one accountant's fee quote.
- Refund, promotion, cash-loss, handling, payout and support rates [A]: small individually, about NGN 285 (USD 0.21) a parcel together in Moderate [E] (sum of those lines).
- Not modelled: interest on cash, tax, VAT on fees, seasonality (Detty December, Black Friday), naira moves, rider recruitment cost, insurance claims beyond parcel repayment, and any okada restriction on bikes in the launch districts (MC says unconfirmed).
- Optimistic combines the best end of every range at once, so treat it as a ceiling, not a plan.

## Sources

- [Last-mile delivery in Lagos: zones, pricing and timing (2026)](https://kolonell.com/en/blog/last-mile-delivery-zones-pricing-lagos-2026) — accessed 2026-10-13 — used in 20_model/quick_model.md
- [Same-Day Delivery in Lagos: Zones, Cost and Feasibility (2026), Kolonell](https://kolonell.com/en/blog/same-day-delivery-zones-and-cost-lagos-2026) — accessed 2026-10-13 — used in 20_model/quick_model.md
- [Paystack transaction charges](https://support.paystack.com/hc/en-us/articles/360009881920-What-are-Paystack-s-transaction-charges) — accessed 2026-10-13 — used in 20_model/quick_model.md
- [Facebook Ads cost in Nigeria (2026), Grey](https://grey.co/blog/facebook-ads-cost-nigeria) — accessed 2026-10-13 — used in 20_model/quick_model.md
- [Inside Lagos' delivery boom: Riders risking everything to survive, Nairametrics](https://nairametrics.com/2026/05/30/inside-lagos-delivery-boom-riders-risking-everything-to-survive/) — accessed 2026-10-13 — used in 20_model/quick_model.md
- [Exchange rate source, open.er-api.com](https://open.er-api.com/v6/latest/USD) — accessed 2026-10-13 — used in 20_model/quick_model.md

---

> This report was produced by AI agents using publicly available information and the details you provided. Figures may be incomplete, out of date or wrong; each is marked sourced, estimated or assumed. It is not financial, legal, tax or investment advice. Check important figures yourself and talk to real customers before acting.