# Decision pack: Lagos same-day parcel delivery

Agent: Report Writer
Mode: Quick Check
Launch country and city: Nigeria, Lagos (Lagos Island and the Lekki–Ajah axis first)
Date: 2026-10-13
Currency and rate: NGN at 1,331 per USD, as in `00_brief.md` (as of 2026-10-12)
Evidence mix: 7 [S], 38 [E] and 32 [A] figures (counted in the body, excluding the labels legend line)

Labels: [S] sourced, [E] estimated, [A] assumed. Each figure keeps the label and source or method it has in the run file it came from.

This is a fictional example run. The founders and their details are invented.

## Verdict

**Pivot**, copied unchanged from `30_assessment/scorecard_result.json`.

The verdict is about the next test, not the whole company. As planned, the idea does not pass: the Sceptical Investor's re-run of the model has each parcel losing money in the Moderate scenario, and the original flat fee of NGN 2,000 (USD 1.50) [A] would not fix that. The pivot is a change to the offer and the price: replace the flat fee with zone pricing (Island NGN 1,700 (USD 1.28) and Lekki–Ajah NGN 3,000 (USD 2.25) [A], with a 2% fee on cash collected [A] and half the fee charged on refused parcels). It answers the finding that money per transaction is Weak: Moderate contribution is NGN -230 (USD -0.17) [E] per parcel on the Sceptical Investor's inputs (`sceptic.md`, question 2). The 90-day test below checks this changed offer first. It is run as a WhatsApp-booked pilot with no app build.

Why the committee's rules gave this verdict:

- The score alone set the verdict; no rule overrode it.

## Readiness score

**48/100**, confidence **Medium**, copied unchanged from `30_assessment/scorecard_result.json`.

Confidence is Medium because, behind areas 1 to 4, 10 figures are sourced, 11 are estimated and 6 are assumed (counts from `scorecard_inputs.json`), so sourced figures are neither more than half nor fewer than one in five.

| # | Area | Rating | The evidence in one line |
|---|---|---|---|
| 1 | Customer pull | Weak | Sellers pay NGN 5,000 to 7,500 (USD 3.76 to 5.63) for interstate parcels [S](https://techcabal.com/2024/03/16/nigerian-businesses-are-forced-to-navigate-high-flying-delivery-prices/), a different product. No waiting list, search trend or stated intent for this offer was found (`customer_demand.md`). |
| 2 | Route to customers | Adequate | Cost per lead NGN 500 to 5,000 (USD 0.38 to 3.76) [S](https://grey.co/blog/facebook-ads-cost-nigeria); lead-to-seller rate 5% to 20% [A] (no local figure); cost to win a seller NGN 2,500 to 100,000 (USD 1.88 to 75.13) [E] (cost per lead divided by lead-to-seller rate). Nothing proven. |
| 3 | Money per transaction | Weak | Moderate contribution NGN -230 (USD -0.17) [E] (NGN -369 (USD -0.28) [E] with VAT), against the draft model's NGN 88 (USD 0.07) [E]. Island fee NGN 1,500 (USD 1.13) [S](https://kolonell.com/en/blog/last-mile-delivery-zones-pricing-lagos-2026). |
| 4 | Cash to proof | Adequate | Founder cash NGN 18,000,000 (USD 13,524) [A] (stated by the founder in the brief) covers a lean test of NGN 3,120,000 (USD 2,344) [E]. Cash runs out in month 7 [E] if the business runs on at Moderate; no source of later money is named. |
| 5 | Competitive response | Weak | Kwik already runs Lagos same-day and can match Island prices within weeks [A] (inference in `market_competition.md`). Informal riders set the price ceiling and carry no overhead. |
| 6 | Team and commitment | Adequate | Founder 1 full-time from month 1 [A] (stated at intake). Founder 2 part-time for six months [A]. No finance or cash-control owner; employer terms unread. |
| 7 | Rules and operations | Weak | The 2022 okada exemption for delivery riders is unconfirmed today [S](https://www.icirnigeria.org/delivery-riders-power-bikes-exempted-from-lagos-okada-ban-police/) (headline only). Courier licence and cash remittance rules not researched; VAT threshold unresolved. |

## What the numbers say

From `20_model/quick_model.md`, with the Sceptical Investor's recomputed figure beside it where the two differ. The recompute in `sceptic.md` covers the Moderate scenario only; it changes inputs (blended fee NGN 1,900 (USD 1.43) [E] and rider cost NGN 1,590 (USD 1.19) [E] instead of NGN 2,000 [A] and NGN 1,400 [E]), not arithmetic. The Defensive and Optimistic cells were not recomputed.

| Measure | Defensive | Moderate | Optimistic | Recomputed by the Sceptical Investor (Moderate) |
|---|---|---|---|---|
| Contribution per transaction (what each parcel leaves after its own costs) | NGN -937 (USD -0.70) [E] | NGN 88 (USD 0.07) [E] | NGN 1,053 (USD 0.79) [E] | NGN -230 (USD -0.17) [E]; NGN -369 (USD -0.28) [E] with VAT |
| Break-even month | never within 24 months [E] | never within 24 months [E] | month 4 [E] | same |
| Cash to run the 90-day test | NGN 9,817,894 (USD 7,376) [E] | NGN 9,204,917 (USD 6,916) [E] | NGN 6,062,822 (USD 4,555) [E] | NGN 9,600,000 (USD 7,213) [E] |
| Cash to reach break-even | NGN 103,063,886 (USD 77,433) [E], still falling at month 24 | NGN 75,794,995 (USD 56,946) [E], still falling at month 24 | NGN 6,062,822 (USD 4,555) [E] | NGN 112,590,000 (USD 84,590) [E], still falling at month 24 |

Founder cash in the brief: NGN 18,000,000 (USD 13,524) [A]. Outside money promised: none.

The two versions of Moderate differ because the draft rounded its own 60/40 fee blend of NGN 1,900 up to NGN 2,000 [A] and used a rider cost of NGN 1,400 [E] that its stated zone mix does not give (`sceptic.md`, question 2). Almost every input in the quick model is assumed: the model's evidence mix is 9 [S], 88 [E] and 103 [A].

## Top 3 risks

Most serious first, from the Sceptical Investor's risk register and pre-mortem.

1. **Sellers will not pay what a paid rider costs.** Moderate needs a blended fee of at least NGN 2,110 (USD 1.59) [E] (the fee at which contribution reaches zero), and NGN 2,290 (USD 1.72) [E] once VAT applies. The only sourced Island price is NGN 1,500 (USD 1.13) [S](https://kolonell.com/en/blog/last-mile-delivery-zones-pricing-lagos-2026), and informal WhatsApp riders charge roughly NGN 1,000 to 2,000 (USD 0.75 to 1.50) a run [A]. Likelihood and impact are both High. Early warning sign: more than half of the first 20 sellers [A] refuse the zone price.
2. **The cash runs out with no source of more.** Fixed costs of about NGN 2.2 million (USD 1,653) a month [E] run ahead of contribution; founder cash is gone in month 7 [E], and no raise or amount is named. Funding climate was not researched in this Quick Check. Likelihood and impact are both High. Early warning sign: cumulative spend above NGN 4,000,000 (USD 3,005) [A] before the decision.
3. **Cash loss or late remittance.** A rider keeping one day's cash costs about NGN 360,000 (USD 270) [E] (20 cash parcels x NGN 18,000 [A]), which wipes out a month or more of Moderate contribution. No one on the team owns cash reconciliation (`founder_fit.md`), and sellers drop couriers that fail them (`customer_demand.md`). Likelihood Medium, impact High. Early warning sign: any unreconciled day, or any seller complaint about payout timing.

## The test

The cheapest test in the next 90 days: a concierge pilot booked by WhatsApp and a form, with no app.

- Version tested: the changed offer (zone pricing), not the original flat NGN 2,000 fee. The Sceptical Investor's recompute puts the original fee below zero contribution, so testing it would only confirm a loss. This is the same change as the pivot above.
- What it tests: whether Lagos sellers will pay a blended fee near NGN 2,220 (USD 1.67) [E] (Island NGN 1,700 and Lekki–Ajah NGN 3,000 [A] at a 60/40 mix) while riders accept about NGN 1,590 (USD 1.19) [E] a drop (`sceptic.md`, question 9).
- What you do: Founder 1 recruits 20 sellers [A] in Lekki, Victoria Island and Ajah and contracts 3 to 5 riders [A] at a per-drop rate. You run real paid parcels at the zone prices and log every cost per parcel. Before the pilot starts, get five courier quotes and five rider quotes, and pay for one legal check of the okada exemption, courier licence and cash remittance.
- Budget: NGN 3,120,000 (USD 2,344) [E] (Founder 1 pay, a part-time dispatcher, tools and messaging, a recoverable cash float of NGN 500,000, Meta ads, seller sign-up credits, a parcel-loss allowance and the legal check; build-up in `sceptic.md`, question 10; each input [A] except the ad floor [S](https://grey.co/blog/facebook-ads-cost-nigeria)).
- Duration: 2 weeks set-up plus 6 weeks live (56 days). Start 2026-10-20, live from 2026-11-03, end 2026-12-15. Black Friday and the December peak fall inside the window, so record cost per drop by week.
- What you measure: contribution per booked parcel, C = (delivery fees collected + cash fees − rider pay for all trips − gateway and transfer fees − cash shortfalls − refunds and claims − discounts − messaging) / parcels booked, which is the money per transaction measure. Also revenue per booked parcel, R = (fees collected + cash fees) / parcels booked, and how many paying sellers are still booking in the last two live weeks.
- Pass line: C − R x 7.5 / 107.5 ≥ 0 (positive after VAT), and at least 12 of the first 20 paying sellers [A] (60% retention, a working bar) still booking in the last two live weeks. Minimum sample: 300 booked parcels from at least 15 paying sellers [A].
- Fail line: C ≤ 0 over the minimum sample, or fewer than 10 of 20 sellers [A] (half, a working bar) accept the zone prices. The Sceptical Investor reads that as: the price sellers will pay does not cover a paid rider, so Stop. Between the lines, change the price once and decide.
- Decide by: 2026-12-22, before the decision deadline of 2027-01-31 in the brief.

Even a pass shows only that a parcel is positive after VAT on thin numbers: the Sceptical Investor's re-run of the zone-priced offer earns NGN 108 (USD 0.08) [E] a parcel before VAT and loses NGN 56 (USD 0.04) [E] after it at Moderate inputs, so the pilot has to beat that.

## What would change this verdict

- Money per transaction (Weak): measured contribution per parcel above zero after VAT over 300 parcels, from the pilot's own logs.
- Customer pull (Weak): at least 12 of 20 pilot sellers [A] still booking after six weeks at paid prices, which shows they pay and stay.
- Competitive response (Weak): evidence that district density and trusted cash remittance hold when Kwik or an informal rider cuts price. The pilot's retention in the last two weeks is the first read.
- Rules and operations (Weak): written confirmation of the okada exemption, courier licence and cash remittance rules, and the VAT registration threshold, from the legal check and an accountant.
- Team and commitment (Adequate): a named owner for cash reconciliation, and written clearance of both founders' employer terms.

## Sources and limits

- Search status: market and customer research: web search and fetch worked, but several pages (Kwik pricing, Glovo and Faramove status, the seller count, the DHL Nigeria page) could not be found or opened. Founder fit: web search was not used. Sceptical Investor: web search partly available; two tax pages were blocked, so the VAT registration threshold (NGN 25 million, 50 million or 100 million) rests on search snippets only.
- The assumptions that matter most and are not yet checked:
  - Zone prices NGN 1,700 and NGN 3,000 and a 2% cash fee [A] (set to clear the zero line, not from evidence).
  - Cash-on-delivery share 60% [A] and refusal rate 10% [A] (no local data).
  - Lead-to-seller rate 5% to 20% [A] (no local figure).
  - Rider day rate NGN 8,000 [A] and tout levy NGN 1,000 a day [A] (no figure found).
  - Founder cash NGN 18,000,000 [A] (stated by the founder, not checked).
  - Monthly seller churn 5% [A] (no retention data).
  - Fee and rider cost rest on one consultancy blog whose two posts disagree; the quick model used the low ends and the Sceptical Investor used the midpoints. Both are shown above.
- Unknown: courier licence and cash remittance rules, goods-in-transit insurance, and whether a raise is possible after month 7.
- What this Quick Check did not cover: no strategy draft, no investment banker review, no revision round. A Full Review covers these and reuses this run's research.
- Every link used in this run is in `sources.md` in the run folder.

---

> This report was produced by AI agents using publicly available information and the details you provided. Figures may be incomplete, out of date or wrong; each is marked sourced, estimated or assumed. It is not financial, legal, tax or investment advice. Check important figures yourself and talk to real customers before acting.
