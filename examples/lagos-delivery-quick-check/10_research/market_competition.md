# Market and competition: Lagos same-day parcel delivery

Agent: byb-market-competition-scout
Mode: Quick Check
Launch country and city: Nigeria, Lagos (Lagos Island and the Lekki–Ajah axis first)
Comparison countries: none
Date: 2026-10-13
Search status: Web search and fetch worked. Several pages (Kwik pricing, Glovo and Faramove status, a seller count) could not be found or opened; those items are marked below.
Evidence mix: 9 [S], 9 [E], 8 [A]

## Key findings

- Market size cannot be sourced bottom-up. No count of small online sellers on Lagos Island and Lekki exists in public sources, so the market is an `[A]`-driven estimate of about NGN 7.8 billion (USD 5.9 million) a year in delivery fees [E] (5,000 sellers x 20 parcels a week x 52 weeks x NGN 1,500; seller count and parcels per week are [A]).
- Per-parcel margin looks thin. One seller-facing guide puts the Island customer fee at NGN 1,500 (USD 1.13) against a real cost per drop of NGN 1,000 to 1,300 (USD 0.75 to 0.98) [S](https://kolonell.com/en/blog/last-mile-delivery-zones-pricing-lagos-2026), leaving roughly NGN 200 to 500 (USD 0.15 to 0.38) per parcel before app, support, cash losses and overhead [E] (fee minus cost range).
- Kwik is the main same-day rival and has no public rate card; its quotes are dynamic and reviewers cite surge pricing and rider availability as weak spots [S](https://brands.ng/blog/kwik-delivery-vs-gigl-which-is-cheaper-faster-in-lagos/).
- Published price points disagree by about 2x (NGN 900 to 5,000 per Lagos parcel depending on source), so the founder's pricing cannot be set from desk research.
- Delivery riders were said to be exempt from the Lagos okada ban in 2022, but no current text confirms it; check before building the rider model.
- Cash remittance is a known pain point at existing couriers, which is the opening for the cash-on-delivery fee, but it is also the main fraud and cash-handling risk [S](https://brands.ng/blog/best-logistics-company-in-nigeria-for-ecommerce-in-2026-a-sellers-honest-guide/).

## Evidence

### Market size, bottom-up

Formula, Lagos Island and Lekki axis: sellers x parcels per week x 52 x fee per parcel.

- Sellers: unknown. Working figure 5,000 [A] (no public count of Instagram and WhatsApp sellers by district found; chosen as a round number for a screening test).
- Parcels per seller: 20 a week [A] (the brief gives 5 to 50; midpoint-ish).
- Fee: NGN 1,500 (USD 1.13) for an Island same-day drop [S](https://kolonell.com/en/blog/last-mile-delivery-zones-pricing-lagos-2026). This is a sizing input only.
- Result: 5.2 million parcels a year and NGN 7.8 billion (USD 5.9 million) a year in fees [E] (5,000 x 20 x 52 x 1,500). Halve or double the seller count and the answer moves in step.
- Lagos city and Nigeria: not built. Unknown without a seller count; do not scale from the Island figure.
- Weak context for the seller base: over half of surveyed Nigerian MSMEs sold online only through social media (GSMA webinar summary, sample size and date not seen) [E] (snippet only, page not opened). Online shoppers: about 76.7 million in 2024 [E] (snippet only, PayU page not opened). These are national figures, not Lagos.
- Top-down cross-check: Nigeria e-commerce was USD 9.35 billion in 2025 [S](https://www.mordorintelligence.com/industry-reports/nigeria-ecommerce-market/market-size); another vendor says USD 15 billion [E] (snippet only, Ken Research page not opened). That is a goods value, not delivery fees. If delivery were 3% of goods value [A] (no source; typical-looking share), national fees would be about USD 280 million, about 47x the Island bottom-up figure. The two answers are not comparable, because the Island is one slice of one city; the gap says only that the bottom-up number is not a ceiling.

### Payment and logistics basics

- Card and bank-transfer gateway fee, local: 1.5% + NGN 100 (USD 0.08), capped at NGN 2,000 (USD 1.50); the NGN 100 is waived under NGN 2,500 (USD 1.88) [S](https://support.paystack.com/hc/en-us/articles/360009881920-What-are-Paystack-s-transaction-charges). On a typical NGN 18,000 basket this is about NGN 370 (USD 0.28) [E] (1.5% x 18,000 + 100; basket from a guide example, [A] as typical).
- Cash on delivery share: unknown. One report puts cash at 23% of online sales [E] (snippet only, page not opened); it may not equal pay-on-delivery.
- Delivery cost: NGN 1,000 to 1,300 (USD 0.75 to 0.98) real cost per Island drop; NGN 2,000 to 2,500 (USD 1.50 to 1.88) for Ajah/Sangotedo [S](https://kolonell.com/en/blog/last-mile-delivery-zones-pricing-lagos-2026). That guide is a consultancy blog with no stated method; treat as order of magnitude.
- Failed delivery rate: no figure found. The same guide says notifying the buyer cuts failed drops 30 to 40% [S](https://kolonell.com/en/blog/last-mile-delivery-zones-pricing-lagos-2026). Working figure 10% failed or refused for cash orders [A] (no local data; to be tested).
- Cash reconciliation: the guide says each rider must remit cash with a slip daily or discrepancies eat margin [S](https://kolonell.com/en/blog/last-mile-delivery-zones-pricing-lagos-2026).

### Seasonality and local norms

- Traffic: Lagos traffic, more than company promises, drives delivery time [S](https://brands.ng/blog/kwik-delivery-vs-gigl-which-is-cheaper-faster-in-lagos/). A noon pickup cut-off for same-day delivery is exposed to this.
- Peak demand (Detty December, Black Friday): expected to lift volume and rider cost, but no source opened [A] (general knowledge, not checked).
- Trust: sellers need cash-on-delivery because many buyers will not prepay a social-media seller [A] (general knowledge, not checked live).
- Okada rules: the 2022 ban covered Eti-Osa, Lagos Island, Lagos Mainland and others [E] (snippet only, Radio Nigeria Lagos page not opened). A police statement reported delivery riders as exempt [S](https://www.icirnigeria.org/delivery-riders-power-bikes-exempted-from-lagos-okada-ban-police/) (headline only; conditions not read, 2022). This bears directly on a bike-based model in the launch districts.

### Competitors

| Name | Type | Pricing and fees | Weak spots from reviews | Likely response |
|---|---|---|---|---|
| Kwik Delivery | local | No public rate card; dynamic app quotes; surge possible. One blog estimate NGN 900 to 2,000 (USD 0.68 to 1.50) [E] (snippet only) | Price fluctuations, rider inconsistency, occasional cancellations [S](https://brands.ng/blog/kwik-delivery-vs-gigl-which-is-cheaper-faster-in-lagos/) | Match price on Island routes; has riders and brand. Its Dutch parent was reported bankrupt in May 2025, with Nigerian operations said to be unaffected [E] (snippet only) |
| GIG Logistics | local, national | NGN 1,500 to 2,500 (USD 1.13 to 1.88) Lagos same-day to 48h in one blog; NGN 3,000 to 5,000 (USD 2.25 to 3.76) for 0 to 2 kg in another [E] (snippet only) | Delays, slow support, inconsistent COD remittance [S](https://brands.ng/blog/best-logistics-company-in-nigeria-for-ecommerce-in-2026-a-sellers-honest-guide/) | Slow; built for intercity, not same-day |
| Sendbox | local | Not found | Dashboard praised; COD remittance timelines a friction [S](https://brands.ng/blog/best-logistics-company-in-nigeria-for-ecommerce-in-2026-a-sellers-honest-guide/) | Could add same-day through partners |
| Gokada and similar rider apps | local | Not found | Riders report low fees pushing them to private jobs outside the app [E] (2021 article, general sector, not Gokada alone) [S](https://www.restofworld.org/2021/when-lagos-banned-ride-hailing-desperate-startups-pivoted-to-deliveries-and-its-paying-off-big-time/) | Already offers on-demand delivery; current status unverified |
| Independent WhatsApp riders, friends and family | informal | Roughly NGN 1,000 to 2,000 (USD 0.75 to 1.50) per run [A] (not found; read from the Kolonell grid) | No tracking, no cash safety, uneven availability [A] (inference, no review pages opened) | None; this is the habit to displace |

Glovo, Bolt and Faramove: current Nigerian delivery status not found.

### Incumbent response

Kwik is the likeliest to respond: it already does Lagos same-day and could cut the Island price or add cash-remittance features within weeks [A] (inference, no evidence of past response behaviour). What would survive a copy: dense rider supply in a few Island and Lekki districts, trusted cash remittance, and seller relationships. A better app alone would not survive.

### One global analogy

Gojek-style on-demand courier apps in Indonesia started as bike-hailing and moved to deliveries for small sellers, as Lagos apps did after the 2020 ban [S](https://www.restofworld.org/2021/when-lagos-banned-ride-hailing-desperate-startups-pivoted-to-deliveries-and-its-paying-off-big-time/) (Lagos side only; the Indonesian side is from general knowledge, not checked [A]). What differs: Lagos has no public address system, heavy traffic, and rider-fee pressure; those apps were funded far more heavily than NGN 18 million (USD 13,524) [E] (18,000,000 / 1,331).

## Gaps and assumptions

- Seller count, parcels per week: [A] (no public data) — how to close it: count active sellers in 10 Lekki and Island Instagram groups and ask 15 sellers their weekly parcels.
- Failed-delivery rate 10% [A] (no local data) — ask three riders or a courier.
- Kwik's actual rates: not found — book five test deliveries on Island routes at different times and record quotes.
- COD share: not found — ask the same 15 sellers.
- Okada exemption for couriers today: unconfirmed — call Lagos State Ministry of Transportation or read the current notice.
- Seasonality and trust claims are [A] (general knowledge, not checked).
- For the lead: rider pay and retention, and seller willingness to pay NGN 1,500 or more per parcel, belong to other agents. Tax and licensing of a cash-remitting service were not checked.

## Sources

- [Last-mile delivery in Lagos: zones, pricing and timing (2026)](https://kolonell.com/en/blog/last-mile-delivery-zones-pricing-lagos-2026) — accessed 2026-10-13 — used in 10_research/market_competition.md
- [Kwik Delivery vs GIGL: Which Is Cheaper and Faster in Lagos](https://brands.ng/blog/kwik-delivery-vs-gigl-which-is-cheaper-faster-in-lagos/) — accessed 2026-10-13 — used in 10_research/market_competition.md
- [Best Logistics Company in Nigeria for Ecommerce in 2026](https://brands.ng/blog/best-logistics-company-in-nigeria-for-ecommerce-in-2026-a-sellers-honest-guide/) — accessed 2026-10-13 — used in 10_research/market_competition.md
- [Paystack transaction charges](https://support.paystack.com/hc/en-us/articles/360009881920-What-are-Paystack-s-transaction-charges) — accessed 2026-10-13 — used in 10_research/market_competition.md
- [Nigeria E-commerce Market Size, Mordor Intelligence](https://www.mordorintelligence.com/industry-reports/nigeria-ecommerce-market/market-size) — accessed 2026-10-13 — used in 10_research/market_competition.md
- [When Lagos banned ride-hailing, startups pivoted to deliveries, Rest of World](https://www.restofworld.org/2021/when-lagos-banned-ride-hailing-desperate-startups-pivoted-to-deliveries-and-its-paying-off-big-time/) — accessed 2026-10-13 — used in 10_research/market_competition.md
- [Delivery riders, power bikes exempted from Lagos okada ban, ICIR](https://www.icirnigeria.org/delivery-riders-power-bikes-exempted-from-lagos-okada-ban-police/) — accessed 2026-10-13 — used in 10_research/market_competition.md

---

> This report was produced by AI agents using publicly available information and the details you provided. Figures may be incomplete, out of date or wrong; each is marked sourced, estimated or assumed. It is not financial, legal, tax or investment advice. Check important figures yourself and talk to real customers before acting.
