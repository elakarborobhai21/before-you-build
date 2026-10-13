# Sceptical Investor assessment: Lagos same-day parcel delivery

Agent: Sceptical Investor
Mode: Quick Check
Draft assessed: 20_model/quick_model.md
Launch country and city: Nigeria, Lagos (Lagos Island and the Lekki–Ajah axis first)
Date: 2026-10-13
Search status: Web search partly available: the WebFetch tool failed with a DNS error, so pages were opened through the lead's fetch script; two tax explainer pages (Guardian, Techpoint) were blocked, so the VAT registration threshold is from search snippets only.
Evidence mix: 27 [S], 73 [E], 54 [A] (counted in the rest of the file, excluding this line)

Follow `<PLUGIN_ROOT>/skills/before-you-build/references/conventions.md` for labels, currency and copy style. This file does not state a verdict: the scoring engine writes it to `30_assessment/scorecard_result.json`.

Brief names below: MC = `10_research/market_competition.md`, CD = `10_research/customer_demand.md`, FF = `10_research/founder_fit.md`, QM = `20_model/quick_model.md`. Rate: 1 USD = 1,331 NGN (00_brief.md, 2026-10-12). All recomputes were run in python3 from the QM formulas with the inputs changed as stated; the QM's own Moderate results (contribution NGN 87.5, 90-day cash NGN 9.20 million, 24-month cash floor NGN 75.80 million) reproduce exactly, so the draft's arithmetic is sound. The disagreements below are about inputs, not sums.

## The ten questions

### 1. Who exactly pays, and why would they switch from what they use today?

The small online seller pays, per the brief, sometimes passing the fee to the buyer. They use WhatsApp riders, couriers or friends today. Reasons to switch are reliability, cash remittance and tracking, but CD marks these as the analyst's reading [A] (no direct evidence found). The evidence that sellers pay and switch is about interstate parcels at NGN 5,000 to 7,500 (USD 3.76 to 5.63) [S](https://techcabal.com/2024/03/16/nigerian-businesses-are-forced-to-navigate-high-flying-delivery-prices/) (March 2024, before later naira moves, CD), not same-day intra-Lagos. CD says plainly there is no direct demand signal for this exact offer. The habit to beat is a known rider at roughly NGN 1,000 to 2,000 (USD 0.75 to 1.50) a run [A] (MC, read from a blog grid, not found directly), and trust in that rider is personal.

### 2. What does one transaction really earn after every cost, including discounts, failures, payments and support?

On my recompute, a Moderate parcel loses NGN 230 (USD 0.17) [E] (QM waterfall re-run with a blended fee of NGN 1,900 and rider cost of NGN 1,590, all other Moderate inputs unchanged), against the draft's gain of NGN 87.5 (USD 0.07). Two input changes drive it. First, the draft rounds its own 60/40 fee blend of NGN 1,900 (USD 1.43) [E] up to NGN 2,000 (USD 1.50) [A] with no evidence. Second, the draft's Moderate rider cost of NGN 1,400 (USD 1.05) is not what its stated zone mix gives: Island NGN 1,000 to 1,300 and Ajah NGN 2,000 to 2,500 [S](https://kolonell.com/en/blog/last-mile-delivery-zones-pricing-lagos-2026) (MC) at the 60/40 mix the fee uses, at range midpoints, give NGN 1,590 (USD 1.19) [E] (0.6 x 1,150 + 0.4 x 2,250). The draft's own Defensive figure of NGN 1,600 uses that same method. Once the business crosses the VAT threshold, VAT of 7.5% [S](https://grey.co/blog/facebook-ads-cost-nigeria) inside a fixed price takes the loss to NGN 369 (USD 0.28) [E] (revenue x 7.5 / 107.5 added as a cost). Even the Island alone loses NGN 66 (USD 0.05) [E] at the NGN 1,500 fee and a NGN 1,150 midpoint cost; it earns NGN 113 (USD 0.08) [E] only at the bottom of the cost range.

### 3. What does it cost to win a customer here, and how many times do they come back?

CD's full range is NGN 2,500 to 100,000 (USD 1.88 to 75.13) [E] (cost per lead NGN 500 to 5,000 [S](https://grey.co/blog/facebook-ads-cost-nigeria) divided by a lead-to-seller rate of 5% to 20% [A]). The draft uses NGN 27,500 (USD 20.66) [A] (middle of CD's assumed planning band). At the draft's own contribution, a seller sending 8 parcels a week [A] earns NGN 3,033 (USD 2.28) a month [E] (87.5 x 8 x 52 / 12), so payback takes 9.1 months [E] (27,500 / 3,033). At my recomputed contribution, a seller is never paid back. Repeat: 5% monthly churn [A] (QM, no retention data in CD) implies an average life of 20 months [E] (1 / 0.05). No local seller retention figure exists; CD's only evidence is that sellers drop couriers that fail them.

### 4. How much money is needed to reach proof, and where does it come from?

The draft's 90-day test costs NGN 9.20 million (USD 6,916) [E] (QM); on my inputs it is NGN 9.60 million (USD 7,214) [E] (QM monthly model re-run, months 1 to 3), mostly fixed cost. A leaner WhatsApp-booked test with no hub or clerk costs about NGN 3.12 million (USD 2,344) [E] (question 10 build-up). Both fit inside the founders' NGN 18,000,000 (USD 13,524) [A] (stated by the founder in the brief). After the test there is no break-even in sight: the Moderate cash floor is NGN 112.59 million (USD 84,589) [E] at month 24 and still falling, against the draft's NGN 75.80 million (USD 56,949) [E]. Founder cash runs out in month 7 [E] on both sets of inputs. The draft names no capital ask and no source; funding climate was not researched in this Quick Check, so whether a raise is possible is unknown.

### 5. Who on the team is full-time, and what conflicts does each founder carry?

Founder 1 (operations) is full-time from month 1 [A] (stated at intake, FF). Founder 2 (product) stays part-time for at least six months [A] (FF). No one owns finance or cash reconciliation, which is the core risk in a cash-on-delivery business (FF). Founder 1 left a logistics operations role in 2026, the same sector, so non-compete and non-solicitation terms for riders and sellers are unread; Founder 2's employment contract may claim the app code. Neither is cleared in writing (FF).

### 6. What do the biggest incumbents do the day this launches?

Kwik already runs Lagos same-day with dynamic quotes, estimated at NGN 900 to 2,000 (USD 0.68 to 1.50) [E] (snippet only, page not opened, MC). It can match an Island price within weeks [A] (MC inference). GIG is slow and intercity-focused; Sendbox could add same-day through partners (MC). The real price ceiling is the informal WhatsApp rider, who carries no app, hub or reconciliation overhead and will not change at all. What survives a price match is dense rider supply in a few districts and trusted cash remittance, not the app.

### 7. Which rule, licence or tax could change the model?

- VAT at 7.5% [S](https://grey.co/blog/facebook-ads-cost-nigeria). The registration threshold is unresolved: snippets give NGN 25 million, NGN 50 million from January 2026, or NGN 100 million [E] (snippet only, pages not opened). Draft Moderate revenue is NGN 46.85 million (USD 35,199) in year 1 and NGN 194.83 million (USD 146,380) in year 2 [E] (QM monthly model summed), so VAT applies by year 2 under any of these thresholds. Informal riders charge none.
- Company income tax: small companies with turnover up to NGN 100 million are exempt from company income tax; above it, about 34% of profit [S](https://www.zikoko.com/money/nigerian-tax-laws-2026-what-it-means-for-your-wallet/). This only bites once profitable.
- The 2022 Lagos okada ban covered Eti-Osa and Lagos Island; delivery riders were reported exempt [S](https://www.icirnigeria.org/delivery-riders-power-bikes-exempted-from-lagos-okada-ban-police/) (2022, headline only, more than two years old). Current status is unconfirmed.
- Collecting buyers' cash and remitting it to sellers may count as payment collection or need a courier licence; not checked by any brief [A] (not researched).

### 8. What did the draft leave out?

The draft is honest about most of its gaps and lists VAT, okada rules, rider recruitment and naira moves as "not modelled". What it leaves out that changes the answer: VAT inside a fixed price (NGN 139 (USD 0.10) a parcel [E]); a rider cost inconsistent with its own zone mix; the rounding up of the fee; gateway fees if buyers pay on delivery by transfer instead of cash; a float that stays at NGN 500,000 (USD 376) [A] (QM) while daily cash collected reaches about NGN 1.46 million (USD 1,097) by month 12 [E]; and any capital ask or source of money after month 7. See Missing costs.

### 9. What is the single assumption that, if wrong, kills the business?

That Lagos sellers will pay a blended same-day fee of at least NGN 2,110 (USD 1.59) [E] (fee at which Moderate contribution reaches zero with a 2% cash fee, rider cost NGN 1,590), and at least NGN 2,290 (USD 1.72) [E] once VAT applies, while riders accept about NGN 1,590 (USD 1.19) [E] a drop. The only sourced Island price is NGN 1,500 (USD 1.13) [S](https://kolonell.com/en/blog/last-mile-delivery-zones-pricing-lagos-2026), and Kwik's estimated top is NGN 2,000 [E] (snippet only). If sellers will not pay above what they pay a WhatsApp rider, every parcel loses money and volume makes it worse.

### 10. What is the cheapest way to find out within 90 days?

My recompute puts Moderate contribution below zero, so the test must test a changed offer, not the original NGN 2,000 flat fee. The changed offer is zone pricing: Island NGN 1,700 (USD 1.28) and Lekki–Ajah NGN 3,000 (USD 2.25) [A] (set so a 60/40 mix clears the zero line), a blended NGN 2,220 (USD 1.67) [E], plus a 2% fee on cash collected [A] (up from 1.5%) and half the fee charged on refused parcels. At Moderate inputs this earns NGN 108 (USD 0.08) a parcel before VAT and loses NGN 56 (USD 0.04) after it [E] (QM waterfall re-run), so it is positive but thin; the test finds out whether sellers accept it and what riders really cost.

- Test: a concierge pilot booked by WhatsApp and a form, no app. Founder 1 recruits 20 sellers [A] (enough to reach the sample in six weeks at 8 parcels a week [A]) in Lekki, Victoria Island and Ajah, contracts 3 to 5 riders [A] (per-drop rate), and runs real paid parcels at the zone prices, logging every cost per parcel.
- Cost: NGN 3.12 million (USD 2,344) [E] (Founder 1 pay 2 x 600,000, part-time dispatcher 2 x 250,000, tools and messaging 2 x 150,000, cash float 500,000 (recoverable), Meta ads 120,000 at Grey's NGN 60,000-a-month floor, seller sign-up credits 15 x 10,000, parcel-loss allowance 300 x 500, legal check of the okada exemption, courier licence and cash remittance 200,000; each input [A] except the ad floor [S](https://grey.co/blog/facebook-ads-cost-nigeria)).
- What it measures: contribution per booked parcel C = (delivery fees collected + cash fees − rider pay for all trips − gateway and transfer fees − cash shortfalls − refunds and claims − discounts − messaging) / parcels booked; and R = revenue per booked parcel = (fees collected + cash fees) / parcels booked. It directly measures money per transaction.
- Pass line: C − R x 7.5 / 107.5 ≥ 0 (positive after VAT), and at least 12 of the first 20 paying sellers [A] (60% retention, a working bar) still booking in the last two live weeks.
- Fail line: C ≤ 0 over the minimum sample, or fewer than 10 of 20 sellers [A] (half, a working bar) accept the zone prices. That means the price sellers will pay does not cover a paid rider: Stop. Between the lines, change the price once and decide.
- Minimum sample: 300 booked parcels from at least 15 paying sellers [A] (enough parcels to read failure and refusal rates near 10% to 20%, spread over enough sellers that one seller cannot decide the result).
- Duration: 2 weeks set-up plus 6 weeks live. Start 2026-10-20 (brief date plus 7 days), live from 2026-11-03, end 2026-12-15, decision by 2026-12-22, before the 2027-01-31 deadline. Black Friday and the December peak fall inside the window; record cost per drop by week so the peak does not flatter or hide the result.

## Recomputed numbers

| Figure | Draft value | Recomputed value | Label and method or source | Difference and why |
|---|---|---|---|---|
| Market size, Island and Lekki | NGN 7.8 billion (USD 5.9 million) a year | NGN 9.88 billion (USD 7.4 million) [E] | 5.2 million parcels [E] (MC: 5,000 sellers [A] x 20 a week [A] x 52) x NGN 1,900 | Same order. Both rest on an assumed seller count; the figure is a screening number only |
| Blended delivery fee, Moderate | NGN 2,000 (USD 1.50) [A] | NGN 1,900 (USD 1.43) [E] | QM's own blend: 60% x 1,500 + 40% x 2,500 | Draft rounded up with no evidence. Within the competitor range of NGN 1,500 to 2,500 Island [S](https://kolonell.com/en/blog/same-day-delivery-zones-and-cost-lagos-2026), at the top of Kwik's estimated NGN 900 to 2,000 [E] (snippet only). Not above the range |
| Cash fee (take on cash collected) | 1.5% [A] | 1.5% [A] (kept) | No competitor cash fee found in MC or CD | No range to compare against; untested |
| Revenue base | Fee plus cash fee; contents not revenue | Same | QM | Correct: the business is not the seller of record, so the NGN 18,000 contents are not counted as revenue |
| Payment fee base | 1.5% x fee + NGN 10 [S](https://support.paystack.com/hc/en-us/articles/360009881920-What-are-Paystack-s-transaction-charges) | Same, plus a risk on cash paid by transfer | Paystack local rate (MC) | Correct base for the fee. Not charged on contents, which holds only if buyers pay riders in cash (see Missing costs) |
| Revenue per parcel, Moderate | NGN 2,085.8 (USD 1.57) | NGN 1,988.8 (USD 1.49) [E] | 1,900 − 57 waived + 145.8 cash fee | −NGN 97 |
| Rider cost per drop, Moderate | NGN 1,400 (USD 1.05) [E] | NGN 1,590 (USD 1.19) [E] | 0.6 x 1,150 + 0.4 x 2,250, midpoints of [S](https://kolonell.com/en/blog/last-mile-delivery-zones-pricing-lagos-2026) | QM says 50/50 mix for Moderate, which gives NGN 1,700; 1,400 matches only 60/40 at the bottom of both ranges. Same mix and method as the draft's Defensive |
| Variable cost per parcel, Moderate | NGN 1,998.3 (USD 1.50) | NGN 2,218.8 (USD 1.67) [E] | QM ten cost lines at the new fee and rider cost | +NGN 221, mostly rider pay and re-attempts |
| Contribution per parcel, Moderate | NGN 87.5 (USD 0.07) | −NGN 230 (USD −0.17) [E]; −NGN 369 (USD −0.28) [E] with VAT | Revenue − variable cost; VAT = revenue x 7.5 / 107.5 | Sign flips |
| Cost to win a seller | NGN 27,500 (USD 20.66) [A] | NGN 2,500 to 100,000 (USD 1.88 to 75.13) [E] | CD method | Draft value is a guess inside a 40-fold range |
| Repeat (monthly churn) | 5% [A] | 5% [A] (kept); 20-month average life [E] | 1 / churn | No evidence either way |
| Break-even month, Moderate | Never within 24 months | Never within 24 months [E] | QM monthly model re-run | Same. Break-even inside 24 months needs a blended fee of about NGN 2,650 (USD 1.99) [E] (month 22) |
| 90-day test cash, Moderate | NGN 9.20 million (USD 6,916) | NGN 9.60 million (USD 7,214) [E] | Months 1 to 3 re-run | +NGN 0.40 million |
| Cash need, Moderate, 24 months | NGN 75.80 million (USD 56,949), still falling | NGN 112.59 million (USD 84,589) [E], still falling | Lowest cumulative point re-run | +NGN 36.79 million; month-24 loss NGN 7.67 million (USD 5,765) [E] a month |
| Capital ask | None stated | None that the plan can support [E] | No break-even, so no amount ends the losses | The draft gives no raise, amount or source |

## Missing costs

| Cost | Amount | Label and method or source | Effect on the Moderate scenario |
|---|---|---|---|
| VAT on fees once registered | NGN 139 (USD 0.10) a parcel | [E] (1,988.8 x 7.5 / 107.5; rate [S](https://grey.co/blog/facebook-ads-cost-nigeria)) | Contribution from −230 to −369; from year 2 at the latest |
| Gateway fee on cash paid by transfer | NGN 123 (USD 0.09) a parcel | [E] (50% of cash buyers paying by transfer [A] x (1.5% x 9,720 + 100) [S](https://support.paystack.com/hc/en-us/articles/360009881920-What-are-Paystack-s-transaction-charges)) | A further −123 if collections go through a gateway; zero if cash in hand |
| Fuel and rider pay rise | NGN 159 (USD 0.12) a parcel per 10% rise | [E] (10% x 1,590); fuel costs rose in 2026 [S](https://nairametrics.com/2026/05/30/inside-lagos-delivery-boom-riders-risking-everything-to-survive/) | Fees are held flat in naira, so any rise comes straight off contribution |
| Rider idle time at low density | Unknown; up to NGN 1,600 (USD 1.20) a parcel at 5 parcels a day | [E] (day rate NGN 8,000 [A] / 5 parcels; month 1 is 139 parcels [E] (QM) over 26 days) | Holds only if riders refuse per-drop pay at low volume; the test shows it |
| Tout and union levies | About NGN 50 (USD 0.04) a parcel | [E] (NGN 1,000 a rider a day [A] / 20 parcels a day [A]); harassment reported in CD (snippets only) | −50 |
| Rider recruitment and checks | NGN 20,000 (USD 15.03) a rider | [A] (no figure found; guarantor and document checks) | Small per parcel; recurs with rider churn |
| Cash float as volume grows | About NGN 2.9 million (USD 2,179) at month 12, against NGN 500,000 in the draft | [E] (2 days x 3,896 / 26 parcels x 9,720 cash per booked parcel) | About NGN 2.4 million more cash tied up by month 12 |
| One rider absconding with a day's cash | About NGN 360,000 (USD 270) an event | [E] (20 cash parcels x NGN 18,000 [A]) | One event wipes out the Moderate contribution of a month or more |
| Courier licence and legal review of cash remittance | Unknown | [A] (not researched in any brief) | Could add a fixed cost or a structure change |
| Goods-in-transit insurance | Unknown | [A] (not found) | The draft's 0.3% claims line assumes the business self-insures |
| Funding after month 7 | Not stated | [E] (cash runs out month 7) | The plan has no source of money after the test |

Costs the draft does cover, with working figures: payment fees on the fee, cash handling and loss, failed deliveries and returns, discounts, refunds, support, founder salaries, hiring, hosting, accounting. Chargebacks are minor for cash and transfer payments.

## Pre-mortem

It is twelve months from launch and the business has failed. It failed because:

1. Every parcel lost money. Sellers would not pay more than their WhatsApp rider, about NGN 1,500 on the Island [S](https://kolonell.com/en/blog/last-mile-delivery-zones-pricing-lagos-2026), while a paid rider cost about NGN 1,590 [E] blended. Growth made the monthly loss bigger.
2. The cash ran out in month 7 [E]. Fixed costs of about NGN 2.2 million (USD 1,653) a month [E] (QM) ran ahead of contribution, and no raise was arranged.
3. A rider kept a day's cash, or remittance ran late, and sellers left. Cash handling had no owner (FF), and sellers drop couriers that fail them (CD).
4. Kwik matched the Island price and informal riders cut theirs, so the only advantage left was service in a few districts.
5. Riders were stopped or harassed under okada rules whose 2022 exemption [S](https://www.icirnigeria.org/delivery-riders-power-bikes-exempted-from-lagos-okada-ban-police/) no longer held, or a VAT bill arrived at 7.5% of fees.

## Risk register

| Risk | Likelihood (Low, Medium, High) | Impact (Low, Medium, High) | Mitigation | Early warning sign |
|---|---|---|---|---|
| Sellers will not pay above NGN 2,110 (USD 1.59) [E] blended | High | High | Zone pricing, test before any build | More than half of the first 20 [A] (pilot target) sellers refuse the zone price |
| Rider cost above NGN 1,590 (USD 1.19) [E] a drop | Medium | High | Per-drop contracts, batched routes, Island-first density | Riders ask for a day rate or reject Lekki–Ajah runs |
| Cash loss or late remittance | Medium | High | Daily deposit slips, rider guarantors, one owner for reconciliation | Any unreconciled day, any seller complaint about payout timing |
| Funding gap after month 7 | High | High | Keep the test lean; decide on the test result before hiring | Cumulative spend above NGN 4 million (USD 3,005) [A] (test budget plus a margin) before the decision |
| Incumbent price match | Medium | Medium | Win on remittance speed and reliability in a few districts | Sellers quote Kwik prices back to you |
| VAT and courier licensing | Medium | Medium | Price VAT in from the start; one paid legal review | Revenue nearing NGN 25 million (USD 18,783) [E] (lowest threshold in snippets) a year |
| Okada restrictions on bikes | Low | High | Confirm the exemption in writing before the pilot | Riders stopped or bikes impounded in Eti-Osa |
| Founder employer conflicts | Low | Medium | Read exit papers; get Founder 2's employer clearance in writing | Any clause naming riders, sellers or code |

## Scorecard

Ratings follow `references/scorecard.md`: Strong (3), Adequate (2), Weak (1), Fatal (0).

| # | Area (key) | Rating | Evidence, with labels |
|---|---|---|---|
| 1 | Customer pull (`customer_pull`) | 1 | Sellers pay NGN 5,000 to 7,500 for interstate parcels [S](https://techcabal.com/2024/03/16/nigerian-businesses-are-forced-to-navigate-high-flying-delivery-prices/), but that is a different product. The delivery market is active: Glovo Nigeria delivered about 38 million items in 2025 [S](https://nairametrics.com/2026/05/30/inside-lagos-delivery-boom-riders-risking-everything-to-survive/). Instagram reaches about 3.7% of Nigerians [S](https://stats.napoleoncat.com/instagram-users-in-nigeria/2026/06/). Seller volume of 5 to 50 parcels a week is [A] (brief definition, not validated). No waiting list, search trend or stated intent for this offer was found. Weak: demand for this exact offer is unproven. |
| 2 | Route to customers (`route_to_customers`) | 2 | Cost per lead NGN 500 to 5,000 [S](https://grey.co/blog/facebook-ads-cost-nigeria); below NGN 60,000 a month the ad algorithm is said not to learn [S](https://grey.co/blog/facebook-ads-cost-nigeria). Lead-to-seller rate 5% to 20% [A] (no local figure). Cost to win a seller NGN 2,500 to 100,000 [E] (CD method); planning band NGN 15,000 to 40,000 [A] (CD). Payback 9.1 months [E] at the draft's contribution. Adequate: channels exist and a full-time operator can sell in person, but nothing is proven. |
| 3 | Money per transaction (`money_per_transaction`) | 1 | Island fee NGN 1,500 [S](https://kolonell.com/en/blog/last-mile-delivery-zones-pricing-lagos-2026); Island rider cost NGN 1,000 to 1,300 [S](https://kolonell.com/en/blog/last-mile-delivery-zones-pricing-lagos-2026); Ajah rider cost NGN 2,000 to 2,500 [S](https://kolonell.com/en/blog/last-mile-delivery-zones-pricing-lagos-2026); first-attempt success 70% to 85% [S](https://kolonell.com/en/blog/same-day-delivery-zones-and-cost-lagos-2026); VAT 7.5% [S](https://grey.co/blog/facebook-ads-cost-nigeria). Blended fee NGN 1,900 [E]; blended rider cost NGN 1,590 [E]; Moderate contribution −NGN 230 [E], −NGN 369 [E] with VAT; zero-contribution fee NGN 2,110 [E]. Cash-on-delivery share 60% [A] and refusal 10% [A] untested. Weak, not Fatal: a zone price can turn it positive on paper, and the test measures it. |
| 4 | Cash to proof (`cash_to_proof`) | 2 | Founder cash NGN 18,000,000 [A] (stated by the founder in the brief). Lean test NGN 3.12 million [E]; draft-shaped 90-day test NGN 9.60 million [E]. Cash need at 24 months NGN 112.59 million [E] and still falling; cash runs out in month 7 [E]. Funding climate not researched. Adequate: the founders can fund the test; the later raise is unproven. |
| 5 | Competitive response (`competitive_response`) | 1 | Kwik runs Lagos same-day and can match Island prices within weeks (MC). Informal riders set the price ceiling and carry no overhead. What survives is district density and trusted remittance, neither built yet. |
| 6 | Team and commitment (`team_commitment`) | 2 | Founder 1 full-time from month 1 (FF). Founder 2 part-time for six months; no finance or cash-control owner; both employer positions unread (FF). |
| 7 | Rules and operations (`rules_operations`) | 1 | The okada exemption for delivery riders dates from 2022 and is unconfirmed today (MC). Courier licensing and cash remittance rules not researched. VAT threshold unresolved. Cash reconciliation has no owner. Several unchecked rules sit directly under the model. |

- Test measures unit economics: true, because the test in question 10 runs real paid parcels at the changed zone prices and logs every cost per parcel, giving contribution per booked parcel directly.
- At least one founder full-time within 6 months of a pass: true, per `10_research/founder_fit.md` (Founder 1 full-time from month 1).
- Labelled figures behind areas 1 to 4: S 10, E 11, A 6
- Inputs: `30_assessment/scorecard_inputs.json`. Score, verdict and confidence: `30_assessment/scorecard_result.json`, written by the scoring engine.

## Gaps and assumptions

- Lead-to-seller rate 5% to 20% [A] (no local figure) — how to close it: the test's NGN 120,000 ad spend and the count of sellers who book a paid parcel.
- Cash-on-delivery share 60% and refusal 10% [A] (no local data) — how to close it: record both on every pilot parcel.
- Share of cash buyers paying by transfer, 50% [A] (no data) — how to close it: record payment method on every pilot parcel.
- Zone prices NGN 1,700 and NGN 3,000 and a 2% cash fee [A] (set to clear the zero line, not from evidence) — how to close it: the pilot itself.
- Rider day rate NGN 8,000 and tout levy NGN 1,000 a day [A] (no figure found) — how to close it: ask five riders what they would accept and what they pay on the road.
- Rider recruitment NGN 20,000 a rider [A] (no figure found) — how to close it: price the first three hires.
- Test cost inputs (pay, tools, credits, legal) [A] (working figures) — how to close it: quotes before 2026-10-20.
- Founder cash NGN 18,000,000 [A] (stated by the founder, not checked).
- VAT registration threshold: NGN 25 million, 50 million or 100 million [E] (snippet only, pages not opened) — how to close it: read the Nigeria Tax Act 2025 text or FIRS guidance, or ask an accountant.
- Okada exemption, courier licence and cash remittance rules: unknown — how to close it: the NGN 200,000 legal check in the test budget.
- Funding climate and a realistic raise: not researched in a Quick Check.
- The rider cost and fee figures rest on one consultancy blog whose posts disagree (MC, CD); my recompute uses its midpoints, the draft used the low ends. Five rider quotes and five courier quotes would settle it before the pilot starts.

## Sources

- [Last-mile delivery in Lagos: zones, pricing and timing (2026)](https://kolonell.com/en/blog/last-mile-delivery-zones-pricing-lagos-2026) — accessed 2026-10-13 — used in 30_assessment/sceptic.md
- [Same-Day Delivery in Lagos: Zones, Cost and Feasibility (2026), Kolonell](https://kolonell.com/en/blog/same-day-delivery-zones-and-cost-lagos-2026) — accessed 2026-10-13 — used in 30_assessment/sceptic.md
- [Paystack transaction charges](https://support.paystack.com/hc/en-us/articles/360009881920-What-are-Paystack-s-transaction-charges) — accessed 2026-10-13 — used in 30_assessment/sceptic.md
- [Facebook Ads cost in Nigeria (2026), Grey](https://grey.co/blog/facebook-ads-cost-nigeria) — accessed 2026-10-13 — used in 30_assessment/sceptic.md
- [Nigerian businesses are forced to navigate high-flying delivery prices, TechCabal](https://techcabal.com/2024/03/16/nigerian-businesses-are-forced-to-navigate-high-flying-delivery-prices/) — accessed 2026-10-13 — used in 30_assessment/sceptic.md
- [Inside Lagos' delivery boom: Riders risking everything to survive, Nairametrics](https://nairametrics.com/2026/05/30/inside-lagos-delivery-boom-riders-risking-everything-to-survive/) — accessed 2026-10-13 — used in 30_assessment/sceptic.md
- [Instagram users in Nigeria, NapoleonCat](https://stats.napoleoncat.com/instagram-users-in-nigeria/2026/06/) — accessed 2026-10-13 — used in 30_assessment/sceptic.md
- [Delivery riders, power bikes exempted from Lagos okada ban, ICIR](https://www.icirnigeria.org/delivery-riders-power-bikes-exempted-from-lagos-okada-ban-police/) — accessed 2026-10-13 — used in 30_assessment/sceptic.md
- [New Nigerian Tax Laws 2026: What They Really Mean for Your Wallet, Zikoko](https://www.zikoko.com/money/nigerian-tax-laws-2026-what-it-means-for-your-wallet/) — accessed 2026-10-13 — used in 30_assessment/sceptic.md

---

> This report was produced by AI agents using publicly available information and the details you provided. Figures may be incomplete, out of date or wrong; each is marked sourced, estimated or assumed. It is not financial, legal, tax or investment advice. Check important figures yourself and talk to real customers before acting.
