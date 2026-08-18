# La Casarana — Historical Pattern & Analytics MVP

## Executive scope

- **As-of date:** 2026-07-31
- **Completed confirmed bookings:** 3,124
- **Future confirmed bookings currently on books:** 307
- **Sellable physical rooms in current catalogue:** 80
- **Excluded non-sellable/deleted/pseudo room types:** 9

> **Design principle:** show the full population first, then reliable rankings, contextual benchmarks, conversion behaviour, distributions and interpretation.
>
> **Occupancy note:** the source does not include the hotel's historical opening calendar. The report therefore uses a clearly labelled **inferred operating-period occupancy** and does not present it as an official opening calendar.

## Executive summary

- **Revenue:** Appartamento Area Giardino is the largest room revenue driver at €1,005,415, while Camera Deluxe leads reliable operating RevPAR at €165.
- **Demand quality:** Appartamento Area Giardino books furthest in advance at 83 days; Appartamento Area Giardino has the lowest reliable cancellation rate at 13.0%.
- **Conversion:** 29,195 requests generated 83.8% quotation coverage and 3.1% matched request-to-booking conversion.
- **What converts:** Appartamento Area Giardino has the highest reliable same-room conversion at 3.3% across 5,086 quoted requests.
- **Treatment conversion:** Bed & Breakfast leads reliable same-treatment conversion at 3.7%.
- **Booking-window conversion:** the 0-7-day band converts best at 8.0% in the reconstructed request funnel.
- **Treatments:** Mezza Pensione is the largest comparable treatment revenue driver at €1,675,352.
- **Pricing implication:** pricing decisions should combine conversion, booking window, retained demand and occupancy; no single KPI is sufficient on its own.

## Decision-relevant patterns

### P01 — Demand is strongly seasonal during inferred operating periods

**Metric:** operating-period occupancy  
**Confidence:** HIGH  
**Evidence:** The strongest operating months are 2025-08, 2024-08, 2024-07 (93.4%, 93.3%, 92.9%); the weakest active months are 2025-05, 2026-05, 2025-09.  
**Why it matters:** Use separate high-season yield and shoulder-season volume strategies; do not treat closed months as zero-demand inventory.

### P02 — Revenue scale and pricing power sit in different rooms

**Metric:** room commercial profile  
**Confidence:** HIGH  
**Evidence:** Appartamento Area Giardino leads reliable room revenue at €1,005,415, while Camera Deluxe leads operating RevPAR at €165. The highest observed ADR is Suite Familiare Vista Piscina at €296 (29 bookings); the highest reliable ADR is Villino Double at €248.  
**Why it matters:** Use total revenue to understand scale, and ADR/RevPAR to understand pricing power and inventory productivity.

### P03 — Early-booking demand is concentrated and more predictable in the strongest lead-time room

**Metric:** booking window + cancellation  
**Confidence:** HIGH  
**Evidence:** Appartamento Area Giardino books 83 days ahead versus a reliable-room weighted average of 60 days, with cancellation 13.0% versus 20.3%.  
**Why it matters:** Review pricing earlier for rooms that combine long lead time with lower cancellation risk.

### P04 — Cancellation changes the quality of apparent demand

**Metric:** cancellation risk  
**Confidence:** HIGH  
**Evidence:** Appartamento Area Giardino has the lowest reliable cancellation rate at 13.0%, 7.2 percentage points below the reliable-room average.  
**Why it matters:** Use retained demand, not gross bookings alone, when interpreting saturation and pickup.

### P05 — Commercial treatment economics are concentrated

**Metric:** treatment concentration  
**Confidence:** HIGH  
**Evidence:** Mezza Pensione and Pensione Completa generate 92.3% of comparable treatment revenue. Mezza Pensione ADR is €209 versus €189, with cancellation 18.9% versus 22.9%.  
**Why it matters:** Prioritize pricing and conversion tests on treatments that combine meaningful volume with strong economics.

### P06 — Room conversion varies materially across quoted solutions

**Metric:** same-room conversion  
**Confidence:** MEDIUM  
**Evidence:** Among rooms with 30+ quoted requests, Appartamento Area Giardino converts 3.3% of quoted requests to the same room, versus Suite Familiare Vista Piscina at 0.9%.  
**Why it matters:** Treat room-level conversion as a demand-quality signal: high conversion can support firmer pricing, while low conversion needs diagnosis before price increases.

### P07 — Some rooms combine conversion with premium economics

**Metric:** conversion + ADR  
**Confidence:** MEDIUM  
**Evidence:** Appartamento Area Giardino combines same-room conversion of 3.3% with ADR €158 and operating RevPAR €103.  
**Why it matters:** Rooms that sustain both conversion and premium economics are the strongest candidates for protecting or cautiously increasing price.

### P08 — Treatment demand differs in actual conversion, not only revenue

**Metric:** same-treatment conversion  
**Confidence:** MEDIUM  
**Evidence:** Bed & Breakfast has the highest reliable same-treatment conversion at 3.7% across 1149 quoted requests.  
**Why it matters:** Use treatment conversion together with ADR and revenue per booking to distinguish popular offers from merely high-volume offers.

### P09 — Conversion changes with booking window

**Metric:** lead-time conversion  
**Confidence:** MEDIUM  
**Evidence:** The highest-converting lead-time band is 0-7 days at 8.0%, versus 61-90 days at 2.2%.  
**Why it matters:** Use lead-time conversion with occupancy and booking pace when deciding whether to push price or protect volume.

### P10 — The funnel loses most demand after quotation

**Metric:** request conversion  
**Confidence:** MEDIUM  
**Evidence:** Of 29,195 requests, 83.8% receive a quote but only 3.1% are matched to confirmed bookings.  
**Why it matters:** Conversion deserves the same monitoring priority as occupancy and booking window; however, the request-to-booking link remains a proxy.

### P11 — Cancellation risk peaks in a core arrival month

**Metric:** monthly cancellation  
**Confidence:** HIGH  
**Evidence:** The highest cancellation rate among months with 30+ bookings is 2025-08 at 28.1%.  
**Why it matters:** Discount gross demand by month-specific cancellation risk before using it as a pricing trigger.

### P12 — Historical booking pace is a baseline, not yet a live signal

**Metric:** booking pace  
**Confidence:** MEDIUM  
**Evidence:** Average completed-stay booking shares range from 3.6% to 72.9% across lead-time checkpoints.  
**Why it matters:** Store recurring snapshots before interpreting deviations as acceleration or slowdown.

### P13 — Room-category occupancy contains capacity conflicts

**Metric:** data quality  
**Confidence:** HIGH  
**Evidence:** The historical reconstruction contains 423 room-type/date rows above current catalogue capacity.  
**Why it matters:** Treat property-level occupancy as more reliable than room-category occupancy until historical capacity and reassignment logic are confirmed.

### X01 — Aggregate room booking windows hide large seasonal shifts

**Metric:** room × year × season × booking window  
**Confidence:** HIGH  
**Evidence:** Appartamento Area Giardino has a 139-day spread between its shortest and longest reliable monthly booking-window averages.  
**Why it matters:** Use room-and-period-specific lead-time curves instead of one all-season room average when deciding how early pricing should react.

### X02 — Room RevPAR leadership changes by stay period

**Metric:** room × year × season × RevPAR  
**Confidence:** HIGH  
**Evidence:** The strongest reliable room-month RevPAR is Appartamento Area Piscina in 2024-08 at €294.  
**Why it matters:** Monitor room productivity by stay period; an all-season RevPAR average can hide where pricing power is strongest.

### X03 — Room conversion depends on both stay period and booking window

**Metric:** conversion × room × year × season × booking window  
**Confidence:** MEDIUM  
**Evidence:** The strongest sufficiently observed same-room conversion is Appartamento Area Giardino, 2025-09, 0-7: 24.2% across 33 quoted requests.  
**Why it matters:** Read conversion in its room, stay-period and lead-time context before treating it as upward or downward pricing pressure.

### X04 — Treatment booking behaviour changes through the season

**Metric:** treatment × year × season × booking window  
**Confidence:** MEDIUM  
**Evidence:** Mezza Pensione has a 59-day spread between its shortest and longest reliable monthly booking-window averages.  
**Why it matters:** Evaluate treatment pricing and demand by stay period rather than relying on one all-season treatment average.

### X05 — Treatment acceptance changes by season and booking window

**Metric:** conversion × treatment × year × season × booking window  
**Confidence:** MEDIUM  
**Evidence:** The strongest sufficiently observed same-treatment conversion is Mezza Pensione, 2025-09, 0-7: 29.2% across 65 quoted requests.  
**Why it matters:** Validate treatment price and packaging in the specific stay-period and booking-window context where customers actually accept it.

## Conversion performance — what actually converts

> Conversion is a reconstructed **proxy** because the source does not provide a direct request-to-booking identifier. Use it directionally and comparatively, not as an audited CRM conversion rate.

### Overall funnel

|   requests |   requests_with_quote | quote_rate_pct   |   converted_requests | request_to_booking_conversion_pct   | quoted_request_conversion_pct   |
|-----------:|----------------------:|:-----------------|---------------------:|:------------------------------------|:--------------------------------|
|      29195 |                 24456 | 83.75%           |                  829 | 3.07%                               | 3.30%                           |

### Conversion by quoted room

| room_name                     |   quoted_requests |   overall_converted_requests |   same_room_converted_requests | overall_conversion_pct   | same_room_conversion_pct   |   conversion_vs_quoted_room_avg_pp | avg_quote_amount   | avg_adr   | revenue       | cancellation_rate_pct   | operating_occupancy_pct   | operating_revpar   | conversion_reliability   |
|:------------------------------|------------------:|-----------------------------:|-------------------------------:|:-------------------------|:---------------------------|-----------------------------------:|:-------------------|:----------|:--------------|:------------------------|:--------------------------|:-------------------|:-------------------------|
| Appartamento Area Giardino    |              5086 |                          213 |                            166 | 4.19%                    | 3.26%                      |                               1.09 | €2,597.16          | €157.81   | €1,005,415.19 | 13.03%                  | 65.46%                    | €103.30            | HIGH                     |
| Camera  Standard              |              5384 |                          207 |                            169 | 3.84%                    | 3.14%                      |                               0.97 | €1,768.87          | €143.68   | €552,328.88   | 25.03%                  | 69.79%                    | €100.27            | HIGH                     |
| Villino 2Ten                  |               248 |                           12 |                              7 | 4.84%                    | 2.82%                      |                               0.65 | €1,926.22          | €159.21   | €31,581.00    | 22.22%                  | 45.36%                    | €72.21             | HIGH                     |
| Appartamento Area Piscina     |              7456 |                          215 |                            160 | 2.88%                    | 2.15%                      |                              -0.02 | €2,801.80          | €219.96   | €918,835.16   | 19.15%                  | 61.28%                    | €134.79            | HIGH                     |
| Camera Superior               |              5464 |                          171 |                            110 | 3.13%                    | 2.01%                      |                              -0.16 | €2,337.36          | €191.97   | €443,188.77   | 26.54%                  | 72.88%                    | €139.91            | HIGH                     |
| Villino Double                |               368 |                           10 |                              7 | 2.72%                    | 1.90%                      |                              -0.27 | €3,477.66          | €248.13   | €57,374.50    | 23.81%                  | 53.83%                    | €133.56            | HIGH                     |
| Suite Familiare               |               593 |                           21 |                              7 | 3.54%                    | 1.18%                      |                              -0.99 | €3,169.11          | €223.65   | €39,546.15    | 24.32%                  | 39.34%                    | €87.99             | HIGH                     |
| Camera Deluxe                 |              6580 |                          136 |                             62 | 2.07%                    | 0.94%                      |                              -1.23 | €3,102.99          | €238.70   | €327,285.35   | 22.49%                  | 69.29%                    | €165.39            | HIGH                     |
| Suite Familiare Vista Piscina |               996 |                           18 |                              9 | 1.81%                    | 0.90%                      |                              -1.27 | €3,932.70          | €296.27   | €55,337.00    | 21.62%                  | 43.44%                    | €128.71            | HIGH                     |

**How to read this:** `overall_conversion_pct` asks whether a request containing that quoted room converted to any booking; `same_room_conversion_pct` asks whether it converted to that same room. The second is the cleaner signal of what room solution actually converts.

#### Room conversion insight

- **Best reliable same-room conversion:** Appartamento Area Giardino at 3.3% (5,086 quoted requests).
- **Lowest reliable same-room conversion:** Suite Familiare Vista Piscina at 0.9% (996 quoted requests).
- Read this together with ADR and operating RevPAR: high conversion + strong economics can support firmer pricing; low conversion should be diagnosed before increasing price.

### Conversion by quoted treatment

| arrangement_name   | comparability_group   |   quoted_requests |   overall_converted_requests |   same_treatment_converted_requests | overall_conversion_pct   | same_treatment_conversion_pct   |   conversion_vs_comparable_avg_pp | avg_quote_amount   | avg_adr   | revenue_per_booking   | cancellation_rate_pct   | conversion_reliability   |
|:-------------------|:----------------------|------------------:|-----------------------------:|------------------------------------:|:-------------------------|:--------------------------------|----------------------------------:|:-------------------|:----------|:----------------------|:------------------------|:-------------------------|
| Bed & Breakfast    | COMPARABLE_COMMERCIAL |              1149 |                           79 |                                  43 | 6.88%                    | 3.74%                           |                              1.17 | €1,392.76          | €134.96   | €606.24               | 25.38%                  | HIGH                     |
| Mezza Pensione     | COMPARABLE_COMMERCIAL |             11952 |                          488 |                                 410 | 4.08%                    | 3.43%                           |                              0.86 | €2,302.84          | €209.40   | €1,266.33             | 18.85%                  | HIGH                     |
| Pensione Completa  | COMPARABLE_COMMERCIAL |             14790 |                          353 |                                 273 | 2.39%                    | 1.85%                           |                             -0.72 | €2,734.49          | €188.65   | €1,193.38             | 22.92%                  | HIGH                     |
| Only Bed           | COMPARABLE_COMMERCIAL |               451 |                            6 |                                   3 | 1.33%                    | 0.67%                           |                             -1.9  | €1,928.15          | €97.26    | €751.92               | 15.38%                  | HIGH                     |

Special/residence/multiproprietà treatments remain visible, but commercial treatment comparisons should focus on `COMPARABLE_COMMERCIAL` rows.

### Conversion by requested booking window

| booking_window_band   |   requests |   quoted_requests |   converted_requests | quote_rate_pct   | conversion_pct   |
|:----------------------|-----------:|------------------:|---------------------:|:-----------------|:-----------------|
| 0-7                   |       1939 |              1238 |                  155 | 63.52%           | 7.95%            |
| 8-14                  |       2227 |              1677 |                  129 | 75.10%           | 5.78%            |
| 15-30                 |       4660 |              3656 |                  139 | 78.30%           | 2.98%            |
| 31-60                 |       5984 |              5114 |                  151 | 85.20%           | 2.52%            |
| 61-90                 |       4271 |              3925 |                   93 | 91.86%           | 2.18%            |
| 91-180                |       8379 |              7534 |                  193 | 89.67%           | 2.30%            |
| 181+                  |       1735 |              1366 |                   38 | 78.69%           | 2.19%            |

This table shows **when requests convert**, not only when confirmed bookings are eventually observed. It is the most useful conversion view to combine with booking pace and occupancy.

### Conversion by arrival month

| arrival_month   |   requests |   quoted_requests |   converted_requests | quote_rate_pct   | conversion_pct   |   avg_requested_lead_time |
|:----------------|-----------:|------------------:|---------------------:|:-----------------|:-----------------|--------------------------:|
| 2023-12         |          2 |                 0 |                    0 | 0.00%            | 0.00%            |                    124    |
| 2024-01         |          1 |                 0 |                    0 | 0.00%            | 0.00%            |                     32    |
| 2024-02         |          8 |                 1 |                    0 | 12.50%           | 0.00%            |                     39.75 |
| 2024-03         |          1 |                 0 |                    0 | 0.00%            | 0.00%            |                     77    |
| 2024-05         |         47 |                40 |                    2 | 85.11%           | 4.26%            |                     44.3  |
| 2024-06         |       1260 |              1140 |                   70 | 90.26%           | 5.54%            |                     63.46 |
| 2024-07         |       1761 |              1667 |                   91 | 94.23%           | 5.14%            |                     69.66 |
| 2024-08         |       2581 |              2432 |                   82 | 94.12%           | 3.17%            |                     78.23 |
| 2024-09         |       1123 |              1072 |                   36 | 95.46%           | 3.21%            |                     66.87 |
| 2025-03         |          2 |                 0 |                    0 | 0.00%            | 0.00%            |                      6.5  |
| 2025-04         |         23 |                 0 |                    0 | 0.00%            | 0.00%            |                     13.48 |
| 2025-05         |        167 |               125 |                   16 | 73.96%           | 9.47%            |                     25.97 |
| 2025-06         |       1720 |              1633 |                  105 | 94.50%           | 6.08%            |                     46.22 |
| 2025-07         |       2679 |              2523 |                   97 | 93.97%           | 3.61%            |                     61.74 |
| 2025-08         |       4487 |              3447 |                  113 | 76.69%           | 2.51%            |                     67.99 |
| 2025-09         |        787 |               651 |                   72 | 81.89%           | 9.06%            |                     40.81 |
| 2025-10         |         12 |                 0 |                    0 | 0.00%            | 0.00%            |                     38.25 |
| 2025-11         |          8 |                 0 |                    0 | 0.00%            | 0.00%            |                      9.88 |
| 2025-12         |         19 |                 0 |                    0 | 0.00%            | 0.00%            |                     32.32 |
| 2026-01         |         13 |                 0 |                    0 | 0.00%            | 0.00%            |                     30.77 |
| 2026-02         |         12 |                 0 |                    0 | 0.00%            | 0.00%            |                     12.58 |
| 2026-03         |          8 |                 0 |                    0 | 0.00%            | 0.00%            |                     12.38 |
| 2026-04         |         45 |                 0 |                    0 | 0.00%            | 0.00%            |                     28.84 |
| 2026-05         |        264 |               137 |                   11 | 51.50%           | 4.14%            |                     44.61 |
| 2026-06         |       1979 |              1390 |                   68 | 69.92%           | 3.42%            |                     76.54 |
| 2026-07         |       4030 |              3118 |                   69 | 77.29%           | 1.71%            |                     78.99 |
| 2026-08         |       5676 |              4715 |                   55 | 82.97%           | 0.97%            |                    101.08 |
| 2026-09         |        475 |               419 |                   11 | 88.03%           | 2.31%            |                     97.49 |
| 2026-10         |          5 |                 0 |                    0 | 0.00%            | 0.00%            |                    158    |

## Room performance

### Full room population

| room_name                     |   confirmed_bookings | revenue       | avg_adr   |   avg_los |   avg_booking_window | cancellation_rate_pct   | operating_occupancy_pct   | operating_revpar   | revenue_share_pct   | reliability   |
|:------------------------------|---------------------:|:--------------|:----------|----------:|---------------------:|:------------------------|:--------------------------|:-------------------|:--------------------|:--------------|
| Appartamento Area Giardino    |                  983 | €1,005,415.19 | €157.81   |      6.66 |                82.91 | 13.03%                  | 65.46%                    | €103.30            | 29.29%              | HIGH          |
| Appartamento Area Piscina     |                  644 | €918,835.16   | €219.96   |      6.14 |                49.5  | 19.15%                  | 61.28%                    | €134.79            | 26.77%              | HIGH          |
| Camera  Standard              |                  746 | €552,328.88   | €143.68   |      4.74 |                48.88 | 25.03%                  | 69.79%                    | €100.27            | 16.09%              | HIGH          |
| Camera Superior               |                  413 | €443,188.77   | €191.97   |      5.11 |                44.7  | 26.54%                  | 72.88%                    | €139.91            | 12.91%              | HIGH          |
| Camera Deluxe                 |                  220 | €327,285.35   | €238.70   |      5.75 |                56.27 | 22.49%                  | 69.29%                    | €165.39            | 9.54%               | HIGH          |
| Villino Double                |                   31 | €57,374.50    | €248.13   |      6.16 |                52.68 | 23.81%                  | 53.83%                    | €133.56            | 1.67%               | MEDIUM        |
| Suite Familiare Vista Piscina |                   29 | €55,337.00    | €296.27   |      5.55 |                54.66 | 21.62%                  | 43.44%                    | €128.71            | 1.61%               | LOW           |
| Suite Familiare               |                   27 | €39,546.15    | €223.65   |      5.33 |                46.81 | 24.32%                  | 39.34%                    | €87.99             | 1.15%               | LOW           |
| Villino 2Ten                  |                   27 | €31,581.00    | €159.21   |      6.15 |                60.41 | 22.22%                  | 45.36%                    | €72.21             | 0.92%               | LOW           |
| OTA Camera Standard           |                    4 | €1,516.71     | €155.64   |      2.5  |                20    | 55.56%                  | 0.91%                     | €1.42              | 0.04%               | INSUFFICIENT  |

Reliability: HIGH ≥100 completed confirmed bookings; MEDIUM 30–99; LOW 10–29; INSUFFICIENT <10. Rankings below require at least 30 observations.

## Reliable room rankings

### Ranking by ADR

|   rank | room_name                  | value   |   observations | reliability   |
|-------:|:---------------------------|:--------|---------------:|:--------------|
|      1 | Villino Double             | €248.13 |             31 | MEDIUM        |
|      2 | Camera Deluxe              | €238.70 |            220 | HIGH          |
|      3 | Appartamento Area Piscina  | €219.96 |            644 | HIGH          |
|      4 | Camera Superior            | €191.97 |            413 | HIGH          |
|      5 | Appartamento Area Giardino | €157.81 |            983 | HIGH          |
|      6 | Camera  Standard           | €143.68 |            746 | HIGH          |

### Ranking by Revenue

|   rank | room_name                  | value         |   observations | reliability   |
|-------:|:---------------------------|:--------------|---------------:|:--------------|
|      1 | Appartamento Area Giardino | €1,005,415.19 |            983 | HIGH          |
|      2 | Appartamento Area Piscina  | €918,835.16   |            644 | HIGH          |
|      3 | Camera  Standard           | €552,328.88   |            746 | HIGH          |
|      4 | Camera Superior            | €443,188.77   |            413 | HIGH          |
|      5 | Camera Deluxe              | €327,285.35   |            220 | HIGH          |
|      6 | Villino Double             | €57,374.50    |             31 | MEDIUM        |

### Ranking by Booking window

|   rank | room_name                  | value   |   observations | reliability   |
|-------:|:---------------------------|:--------|---------------:|:--------------|
|      1 | Appartamento Area Giardino | 82.91d  |            983 | HIGH          |
|      2 | Camera Deluxe              | 56.27d  |            220 | HIGH          |
|      3 | Villino Double             | 52.68d  |             31 | MEDIUM        |
|      4 | Appartamento Area Piscina  | 49.50d  |            644 | HIGH          |
|      5 | Camera  Standard           | 48.88d  |            746 | HIGH          |
|      6 | Camera Superior            | 44.70d  |            413 | HIGH          |

### Ranking by Lowest cancellation

|   rank | room_name                  | value   |   observations | reliability   |
|-------:|:---------------------------|:--------|---------------:|:--------------|
|      1 | Appartamento Area Giardino | 13.03%  |            983 | HIGH          |
|      2 | Appartamento Area Piscina  | 19.15%  |            644 | HIGH          |
|      3 | Camera Deluxe              | 22.49%  |            220 | HIGH          |
|      4 | Villino Double             | 23.81%  |             31 | MEDIUM        |
|      5 | Camera  Standard           | 25.03%  |            746 | HIGH          |
|      6 | Camera Superior            | 26.54%  |            413 | HIGH          |

### Ranking by Inferred operating-period occupancy

|   rank | room_name                  | value   |   observations | reliability   |
|-------:|:---------------------------|:--------|---------------:|:--------------|
|      1 | Camera Superior            | 72.88%  |            413 | HIGH          |
|      2 | Camera  Standard           | 69.79%  |            746 | HIGH          |
|      3 | Camera Deluxe              | 69.29%  |            220 | HIGH          |
|      4 | Appartamento Area Giardino | 65.46%  |            983 | HIGH          |
|      5 | Appartamento Area Piscina  | 61.28%  |            644 | HIGH          |
|      6 | Villino Double             | 53.83%  |             31 | MEDIUM        |

### Ranking by Inferred operating-period RevPAR

|   rank | room_name                  | value   |   observations | reliability   |
|-------:|:---------------------------|:--------|---------------:|:--------------|
|      1 | Camera Deluxe              | €165.39 |            220 | HIGH          |
|      2 | Camera Superior            | €139.91 |            413 | HIGH          |
|      3 | Appartamento Area Piscina  | €134.79 |            644 | HIGH          |
|      4 | Villino Double             | €133.56 |             31 | MEDIUM        |
|      5 | Appartamento Area Giardino | €103.30 |            983 | HIGH          |
|      6 | Camera  Standard           | €100.27 |            746 | HIGH          |

### Ranking by Average length of stay

|   rank | room_name                  | value   |   observations | reliability   |
|-------:|:---------------------------|:--------|---------------:|:--------------|
|      1 | Appartamento Area Giardino | 6.66d   |            983 | HIGH          |
|      2 | Villino Double             | 6.16d   |             31 | MEDIUM        |
|      3 | Appartamento Area Piscina  | 6.14d   |            644 | HIGH          |
|      4 | Camera Deluxe              | 5.75d   |            220 | HIGH          |
|      5 | Camera Superior            | 5.11d   |            413 | HIGH          |
|      6 | Camera  Standard           | 4.74d   |            746 | HIGH          |

## Room comparison against meaningful benchmarks

### Commercial performance

| room_name                     |   confirmed_bookings | revenue       |   revenue_share_pct | avg_adr   | operating_revpar   | reliability   |   bookings_vs_peer_median_pct |   revenue_vs_peer_median_pct |   adr_vs_property_pct |   revpar_vs_property_pct |
|:------------------------------|---------------------:|:--------------|--------------------:|:----------|:-------------------|:--------------|------------------------------:|-----------------------------:|----------------------:|-------------------------:|
| Appartamento Area Giardino    |                  983 | €1,005,415.19 |               29.29 | €157.81   | €103.30            | HIGH          |                        683.27 |                       422.76 |                -16.85 |                   -13.38 |
| Appartamento Area Piscina     |                  644 | €918,835.16   |               26.77 | €219.96   | €134.79            | HIGH          |                        413.15 |                       377.74 |                 15.89 |                    13.02 |
| Camera  Standard              |                  746 | €552,328.88   |               16.09 | €143.68   | €100.27            | HIGH          |                        494.42 |                       187.18 |                -24.3  |                   -15.92 |
| Camera Superior               |                  413 | €443,188.77   |               12.91 | €191.97   | €139.91            | HIGH          |                        229.08 |                       130.43 |                  1.15 |                    17.31 |
| Camera Deluxe                 |                  220 | €327,285.35   |                9.54 | €238.70   | €165.39            | HIGH          |                         75.3  |                        70.17 |                 25.77 |                    38.68 |
| Villino Double                |                   31 | €57,374.50    |                1.67 | €248.13   | €133.56            | MEDIUM        |                        -75.3  |                       -70.17 |                 30.74 |                    11.99 |
| Suite Familiare Vista Piscina |                   29 | €55,337.00    |                1.61 | €296.27   | €128.71            | LOW           |                        -76.89 |                       -71.23 |                 56.1  |                     7.92 |
| Suite Familiare               |                   27 | €39,546.15    |                1.15 | €223.65   | €87.99             | LOW           |                        -78.49 |                       -79.44 |                 17.84 |                   -26.22 |
| Villino 2Ten                  |                   27 | €31,581.00    |                0.92 | €159.21   | €72.21             | LOW           |                        -78.49 |                       -83.58 |                -16.11 |                   -39.45 |
| OTA Camera Standard           |                    4 | €1,516.71     |                0.04 | €155.64   | €1.42              | INSUFFICIENT  |                        -96.81 |                       -99.21 |                -17.99 |                   -98.81 |

Bookings and revenue are compared with the **median room category**; ADR and RevPAR are compared with weighted property benchmarks.

### Demand behaviour

| room_name                     |   confirmed_bookings |   avg_los |   avg_booking_window |   operating_occupancy_pct | reliability   |   los_vs_property_pct |   booking_window_vs_property_pct |   occupancy_vs_property_pp |
|:------------------------------|---------------------:|----------:|---------------------:|--------------------------:|:--------------|----------------------:|---------------------------------:|---------------------------:|
| Appartamento Area Giardino    |                  983 |      6.66 |                82.91 |                     65.46 | HIGH          |                 15.04 |                            38.6  |                       2.62 |
| Appartamento Area Piscina     |                  644 |      6.14 |                49.5  |                     61.28 | HIGH          |                  6.06 |                           -17.25 |                      -1.56 |
| Camera  Standard              |                  746 |      4.74 |                48.88 |                     69.79 | HIGH          |                -18.12 |                           -18.29 |                       6.95 |
| Camera Superior               |                  413 |      5.11 |                44.7  |                     72.88 | HIGH          |                -11.73 |                           -25.28 |                      10.04 |
| Camera Deluxe                 |                  220 |      5.75 |                56.27 |                     69.29 | HIGH          |                 -0.67 |                            -5.93 |                       6.45 |
| Villino Double                |                   31 |      6.16 |                52.68 |                     53.83 | MEDIUM        |                  6.41 |                           -11.94 |                      -9.01 |
| Suite Familiare Vista Piscina |                   29 |      5.55 |                54.66 |                     43.44 | LOW           |                 -4.13 |                            -8.63 |                     -19.4  |
| Suite Familiare               |                   27 |      5.33 |                46.81 |                     39.34 | LOW           |                 -7.93 |                           -21.75 |                     -23.5  |
| Villino 2Ten                  |                   27 |      6.15 |                60.41 |                     45.36 | LOW           |                  6.24 |                             0.99 |                     -17.48 |
| OTA Camera Standard           |                    4 |      2.5  |                20    |                      0.91 | INSUFFICIENT  |                -56.82 |                           -66.57 |                     -61.93 |

### Cancellation risk

| room_name                     |   total_bookings |   canceled_bookings |   cancellation_rate_pct | reliability   |   cancellation_vs_property_pp |
|:------------------------------|-----------------:|--------------------:|------------------------:|:--------------|------------------------------:|
| Appartamento Area Giardino    |             1136 |                 148 |                   13.03 | HIGH          |                         -7.38 |
| Appartamento Area Piscina     |              799 |                 153 |                   19.15 | HIGH          |                         -1.26 |
| Camera  Standard              |              999 |                 250 |                   25.03 | HIGH          |                          4.62 |
| Camera Superior               |              569 |                 151 |                   26.54 | HIGH          |                          6.13 |
| Camera Deluxe                 |              289 |                  65 |                   22.49 | HIGH          |                          2.08 |
| Villino Double                |               42 |                  10 |                   23.81 | MEDIUM        |                          3.4  |
| Suite Familiare Vista Piscina |               37 |                   8 |                   21.62 | LOW           |                          1.21 |
| Suite Familiare               |               37 |                   9 |                   24.32 | LOW           |                          3.91 |
| Villino 2Ten                  |               36 |                   8 |                   22.22 | LOW           |                          1.81 |
| OTA Camera Standard           |                9 |                   5 |                   55.56 | INSUFFICIENT  |                         35.15 |

## Booking-window distribution by room

| booking_window_band   |   Appartamento Area Giardino |   Appartamento Area Piscina |   Camera  Standard |   Camera Deluxe |   Camera Superior |   OTA Camera Standard |   Suite Familiare |   Suite Familiare Vista Piscina |   Villino 2Ten |   Villino Double |
|:----------------------|-----------------------------:|----------------------------:|-------------------:|----------------:|------------------:|----------------------:|------------------:|--------------------------------:|---------------:|-----------------:|
| 0-7                   |                        20.45 |                       18.48 |              24.6  |           21.1  |             26.88 |                     0 |             25.93 |                           24.14 |          25.93 |            25.81 |
| 8-14                  |                         8.04 |                       11.34 |              11.42 |           11.47 |             13.56 |                    25 |             18.52 |                           24.14 |           3.7  |             9.68 |
| 15-30                 |                         8.65 |                       17.55 |              14.38 |           18.35 |             14.53 |                    75 |             25.93 |                           10.34 |          22.22 |            22.58 |
| 31-60                 |                         6.21 |                       20.34 |              14.78 |           12.39 |             18.4  |                     0 |              7.41 |                            0    |          11.11 |             6.45 |
| 61-90                 |                        10.17 |                       15.06 |              13.98 |           11.47 |              7.99 |                     0 |              0    |                           20.69 |          11.11 |            12.9  |
| 91-180                |                        37.33 |                       15.22 |              19.09 |           21.1  |             16.95 |                     0 |             14.81 |                           13.79 |          22.22 |            19.35 |
| 181+                  |                         9.16 |                        2.02 |               1.75 |            4.13 |              1.69 |                     0 |              7.41 |                            6.9  |           3.7  |             3.23 |

## Treatment performance

### Full treatment population

| arrangement_name      | comparability_group       |   confirmed_bookings | revenue       | avg_adr   |   avg_los | cancellation_rate_pct   |   avg_booking_window | revenue_per_booking   | revenue_share_pct   | reliability   |
|:----------------------|:--------------------------|---------------------:|:--------------|:----------|----------:|:------------------------|---------------------:|:----------------------|:--------------------|:--------------|
| Mezza Pensione        | COMPARABLE_COMMERCIAL     |                 1323 | €1,675,352.13 | €209.40   |      5.75 | 18.85%                  |                51.14 | €1,266.33             | 48.81%              | HIGH          |
| Pensione Completa     | COMPARABLE_COMMERCIAL     |                 1216 | €1,451,150.56 | €188.65   |      5.68 | 22.92%                  |                56.85 | €1,193.38             | 42.28%              | HIGH          |
| Bed & Breakfast       | COMPARABLE_COMMERCIAL     |                  294 | €178,233.50   | €134.96   |      4.38 | 25.38%                  |                41.76 | €606.24               | 5.19%               | HIGH          |
| Only Bed              | COMPARABLE_COMMERCIAL     |                  110 | €82,711.12    | €97.26    |      8.56 | 15.38%                  |               116.78 | €751.92               | 2.41%               | HIGH          |
| Multipropriet         | SPECIAL_OR_NON_COMPARABLE |                   64 | €35,702.99    | €77.04    |      7.42 | 0.00%                   |               230.86 | €557.86               | 1.04%               | MEDIUM        |
| Mezza Pensione Pranzo | COMPARABLE_COMMERCIAL     |                    8 | €5,591.50     | €99.85    |     10.5  | 0.00%                   |                72    | €698.94               | 0.16%               | INSUFFICIENT  |
| Formula Residence     | SPECIAL_OR_NON_COMPARABLE |                   40 | €2,592.00     | €5.32     |      9.07 | 6.98%                   |               109.18 | €64.80                | 0.08%               | MEDIUM        |
| Solo Pernottamento    | SPECIAL_OR_NON_COMPARABLE |                   48 | €904.00       | €2.69     |      8.23 | 0.00%                   |               106.85 | €18.83                | 0.03%               | MEDIUM        |
| No Board              | SPECIAL_OR_NON_COMPARABLE |                   21 | €170.91       | €5.82     |      1.05 | 30.00%                  |                 5.52 | €8.14                 | 0.00%               | LOW           |

Only `COMPARABLE_COMMERCIAL` treatments are included in reliable treatment rankings.

### Ranking by ADR

|   rank | arrangement_name   | value   |   observations | reliability   |
|-------:|:-------------------|:--------|---------------:|:--------------|
|      1 | Mezza Pensione     | €209.40 |           1323 | HIGH          |
|      2 | Pensione Completa  | €188.65 |           1216 | HIGH          |
|      3 | Bed & Breakfast    | €134.96 |            294 | HIGH          |
|      4 | Only Bed           | €97.26  |            110 | HIGH          |

### Ranking by Revenue

|   rank | arrangement_name   | value         |   observations | reliability   |
|-------:|:-------------------|:--------------|---------------:|:--------------|
|      1 | Mezza Pensione     | €1,675,352.13 |           1323 | HIGH          |
|      2 | Pensione Completa  | €1,451,150.56 |           1216 | HIGH          |
|      3 | Bed & Breakfast    | €178,233.50   |            294 | HIGH          |
|      4 | Only Bed           | €82,711.12    |            110 | HIGH          |

### Ranking by Booking window

|   rank | arrangement_name   | value   |   observations | reliability   |
|-------:|:-------------------|:--------|---------------:|:--------------|
|      1 | Only Bed           | 116.78d |            110 | HIGH          |
|      2 | Pensione Completa  | 56.85d  |           1216 | HIGH          |
|      3 | Mezza Pensione     | 51.14d  |           1323 | HIGH          |
|      4 | Bed & Breakfast    | 41.76d  |            294 | HIGH          |

### Ranking by Lowest cancellation

|   rank | arrangement_name   | value   |   observations | reliability   |
|-------:|:-------------------|:--------|---------------:|:--------------|
|      1 | Only Bed           | 15.38%  |            110 | HIGH          |
|      2 | Mezza Pensione     | 18.85%  |           1323 | HIGH          |
|      3 | Pensione Completa  | 22.92%  |           1216 | HIGH          |
|      4 | Bed & Breakfast    | 25.38%  |            294 | HIGH          |

### Ranking by Average length of stay

|   rank | arrangement_name   | value   |   observations | reliability   |
|-------:|:-------------------|:--------|---------------:|:--------------|
|      1 | Only Bed           | 8.56d   |            110 | HIGH          |
|      2 | Mezza Pensione     | 5.75d   |           1323 | HIGH          |
|      3 | Pensione Completa  | 5.68d   |           1216 | HIGH          |
|      4 | Bed & Breakfast    | 4.38d   |            294 | HIGH          |

### Ranking by Revenue per booking

|   rank | arrangement_name   | value     |   observations | reliability   |
|-------:|:-------------------|:----------|---------------:|:--------------|
|      1 | Mezza Pensione     | €1,266.33 |           1323 | HIGH          |
|      2 | Pensione Completa  | €1,193.38 |           1216 | HIGH          |
|      3 | Only Bed           | €751.92   |            110 | HIGH          |
|      4 | Bed & Breakfast    | €606.24   |            294 | HIGH          |

## Treatment comparison

| arrangement_name      | comparability_group       |   confirmed_bookings | revenue       |   revenue_share_pct | avg_adr   |   avg_los |   avg_booking_window |   cancellation_rate_pct | revenue_per_booking   | reliability   |   adr_vs_comparable_property_pct |   los_vs_comparable_property_pct |   booking_window_vs_comparable_property_pct |   cancellation_vs_comparable_property_pp |   revenue_per_booking_vs_comparable_property_pct |
|:----------------------|:--------------------------|---------------------:|:--------------|--------------------:|:----------|----------:|---------------------:|------------------------:|:----------------------|:--------------|---------------------------------:|---------------------------------:|--------------------------------------------:|-----------------------------------------:|-------------------------------------------------:|
| Mezza Pensione        | COMPARABLE_COMMERCIAL     |                 1323 | €1,675,352.13 |               48.81 | €209.40   |      5.75 |                51.14 |                   18.85 | €1,266.33             | HIGH          |                             3.87 |                             0.82 |                                       -7.12 |                                    -2.25 |                                            10.14 |
| Pensione Completa     | COMPARABLE_COMMERCIAL     |                 1216 | €1,451,150.56 |               42.28 | €188.65   |      5.68 |                56.85 |                   22.92 | €1,193.38             | HIGH          |                            -6.43 |                            -0.41 |                                        3.25 |                                     1.82 |                                             3.79 |
| Bed & Breakfast       | COMPARABLE_COMMERCIAL     |                  294 | €178,233.50   |                5.19 | €134.96   |      4.38 |                41.76 |                   25.38 | €606.24               | HIGH          |                           -33.06 |                           -23.2  |                                      -24.16 |                                     4.28 |                                           -47.27 |
| Only Bed              | COMPARABLE_COMMERCIAL     |                  110 | €82,711.12    |                2.41 | €97.26    |      8.56 |               116.78 |                   15.38 | €751.92               | HIGH          |                           -51.76 |                            50.09 |                                      112.09 |                                    -5.72 |                                           -34.6  |
| Multipropriet         | SPECIAL_OR_NON_COMPARABLE |                   64 | €35,702.99    |                1.04 | €77.04    |      7.42 |               230.86 |                    0    | €557.86               | MEDIUM        |                           -61.79 |                            30.1  |                                      319.28 |                                   -21.1  |                                           -51.48 |
| Mezza Pensione Pranzo | COMPARABLE_COMMERCIAL     |                    8 | €5,591.50     |                0.16 | €99.85    |     10.5  |                72    |                    0    | €698.94               | INSUFFICIENT  |                           -50.47 |                            84.11 |                                       30.76 |                                   -21.1  |                                           -39.21 |
| Formula Residence     | SPECIAL_OR_NON_COMPARABLE |                   40 | €2,592.00     |                0.08 | €5.32     |      9.07 |               109.18 |                    6.98 | €64.80                | MEDIUM        |                           -97.36 |                            59.03 |                                       98.29 |                                   -14.12 |                                           -94.36 |
| Solo Pernottamento    | SPECIAL_OR_NON_COMPARABLE |                   48 | €904.00       |                0.03 | €2.69     |      8.23 |               106.85 |                    0    | €18.83                | MEDIUM        |                           -98.67 |                            44.31 |                                       94.06 |                                   -21.1  |                                           -98.36 |
| No Board              | SPECIAL_OR_NON_COMPARABLE |                   21 | €170.91       |                0    | €5.82     |      1.05 |                 5.52 |                   30    | €8.14                 | LOW           |                           -97.11 |                           -81.59 |                                      -89.97 |                                     8.9  |                                           -99.29 |

## Booking-window distribution by treatment

| booking_window_band   |   Bed & Breakfast |   Formula Residence |   Mezza Pensione |   Mezza Pensione Pranzo |   Multipropriet |   No Board |   Only Bed |   Pensione Completa |   Solo Pernottamento |
|:----------------------|------------------:|--------------------:|-----------------:|------------------------:|----------------:|-----------:|-----------:|--------------------:|---------------------:|
| 0-7                   |             29.25 |                 0   |            24.41 |                     0   |               0 |      95.24 |       8.18 |               20.46 |                 6.25 |
| 8-14                  |             10.54 |                 0   |            12.32 |                     0   |               0 |       0    |       4.55 |               11.22 |                 0    |
| 15-30                 |             18.37 |                 0   |            13.68 |                    25   |               0 |       0    |       0.91 |               15.84 |                 2.08 |
| 31-60                 |             16.67 |                 0   |            13.45 |                    12.5 |               0 |       4.76 |       0.91 |               14.93 |                 2.08 |
| 61-90                 |              6.12 |                22.5 |            14.74 |                    25   |               0 |       0    |       4.55 |               11.3  |                12.5  |
| 91-180                |             19.05 |                77.5 |            19.35 |                    37.5 |               0 |       0    |      80.91 |               22.36 |                77.08 |
| 181+                  |              0    |                 0   |             2.04 |                     0   |             100 |       0    |       0    |                3.88 |                 0    |

## Occupancy by completed stay month

| stay_month   |   occupied_room_nights |   calendar_available_room_nights |   calendar_occupancy_pct | inferred_operating_month   |   operating_occupancy_pct |   peak_daily_room_type_occupancy_pct |   over_capacity_rows |
|:-------------|-----------------------:|---------------------------------:|-------------------------:|:---------------------------|--------------------------:|-------------------------------------:|---------------------:|
| 2024-05      |                      6 |                               80 |                     7.5  | False                      |                    nan    |                               100    |                    0 |
| 2024-06      |                   1893 |                             2400 |                    78.88 | True                       |                     78.88 |                               200    |                   55 |
| 2024-07      |                   2303 |                             2480 |                    92.86 | True                       |                     92.86 |                               180    |                   70 |
| 2024-08      |                   2315 |                             2480 |                    93.35 | True                       |                     93.35 |                               200    |                   77 |
| 2024-09      |                   1107 |                             2400 |                    46.12 | True                       |                     46.12 |                               140    |                   22 |
| 2024-10      |                      0 |                             2480 |                     0    | False                      |                    nan    |                                 0    |                    0 |
| 2024-11      |                      0 |                             2400 |                     0    | False                      |                    nan    |                                 0    |                    0 |
| 2024-12      |                      0 |                             2480 |                     0    | False                      |                    nan    |                                 0    |                    0 |
| 2025-01      |                      0 |                             2480 |                     0    | False                      |                    nan    |                                 0    |                    0 |
| 2025-02      |                      0 |                             2240 |                     0    | False                      |                    nan    |                                 0    |                    0 |
| 2025-03      |                      0 |                             2480 |                     0    | False                      |                    nan    |                                 0    |                    0 |
| 2025-04      |                      0 |                             2400 |                     0    | False                      |                    nan    |                                 0    |                    0 |
| 2025-05      |                     70 |                             2480 |                     2.82 | True                       |                      2.82 |                               114.29 |                    2 |
| 2025-06      |                   1339 |                             2400 |                    55.79 | True                       |                     55.79 |                               140    |                   15 |
| 2025-07      |                   2282 |                             2480 |                    92.02 | True                       |                     92.02 |                               150    |                   43 |
| 2025-08      |                   2316 |                             2480 |                    93.39 | True                       |                     93.39 |                               200    |                   50 |
| 2025-09      |                    885 |                             2400 |                    36.88 | True                       |                     36.88 |                               137.5  |                   20 |
| 2025-10      |                      0 |                             2480 |                     0    | False                      |                    nan    |                                 0    |                    0 |
| 2025-11      |                     18 |                             2400 |                     0.75 | False                      |                    nan    |                               100    |                    0 |
| 2025-12      |                      0 |                             2480 |                     0    | False                      |                    nan    |                                 0    |                    0 |
| 2026-01      |                      0 |                             2480 |                     0    | False                      |                    nan    |                                 0    |                    0 |
| 2026-02      |                      0 |                             2240 |                     0    | False                      |                    nan    |                                 0    |                    0 |
| 2026-03      |                      0 |                             2480 |                     0    | False                      |                    nan    |                                 0    |                    0 |
| 2026-04      |                      0 |                             2400 |                     0    | False                      |                    nan    |                                 0    |                    0 |
| 2026-05      |                    310 |                             2480 |                    12.5  | True                       |                     12.5  |                               125    |                    4 |
| 2026-06      |                   1351 |                             2400 |                    56.29 | True                       |                     56.29 |                               300    |                   21 |
| 2026-07      |                   2228 |                             2400 |                    92.83 | True                       |                     92.83 |                               150    |                   44 |

## Property booking-window distribution

| booking_window_band   |   bookings |   room_nights |   revenue |    adr |   booking_share_pct |
|:----------------------|-----------:|--------------:|----------:|-------:|--------------------:|
| 0-7                   |        689 |          2465 |    469240 | 164.71 |               22.08 |
| 8-14                  |        335 |          1526 |    349263 | 200.02 |               10.74 |
| 15-30                 |        431 |          1947 |    438554 | 202.77 |               13.81 |
| 31-60                 |        412 |          2417 |    542874 | 207.88 |               13.21 |
| 61-90                 |        372 |          2678 |    492041 | 183.21 |               11.92 |
| 91-180                |        743 |          5946 |    948442 | 158.98 |               23.81 |
| 181+                  |        138 |          1095 |    191995 | 168.08 |                4.42 |

## Cross-dimensional discovery — how behaviour changes

> This layer merges the dimensions Luca highlighted: **year, stay period, room, treatment, booking window, conversion, ADR/RevPAR and cancellation**. The detailed CSVs contain the full crossover population; the report shows reliable/decision-relevant slices.

### Room × year × season / month

|   stay_year | stay_month   | season_band   | room_name                  |   confirmed_bookings |   avg_booking_window | avg_adr   | occupancy_pct   | revpar   | cancellation_rate_pct   | reliability   |
|------------:|:-------------|:--------------|:---------------------------|---------------------:|---------------------:|:----------|:----------------|:---------|:------------------------|:--------------|
|        2024 | 2024-06      | SHOULDER      | Appartamento Area Giardino |                  120 |                79.08 | €140.12   | 78.57%          | €110.09  | 12.14%                  | HIGH          |
|        2024 | 2024-07      | PEAK          | Appartamento Area Giardino |                  112 |                98.22 | €133.44   | 117.17%         | €156.35  | 14.39%                  | HIGH          |
|        2024 | 2024-08      | PEAK          | Appartamento Area Giardino |                  123 |               113.21 | €117.61   | 109.56%         | €128.86  | 6.77%                   | HIGH          |
|        2024 | 2024-09      | SHOULDER      | Appartamento Area Giardino |                   43 |                45.95 | €157.26   | 45.12%          | €70.96   | 21.82%                  | MEDIUM        |
|        2025 | 2025-06      | SHOULDER      | Appartamento Area Giardino |                   97 |                34.91 | €171.92   | 45.36%          | €77.98   | 13.39%                  | MEDIUM        |
|        2025 | 2025-07      | PEAK          | Appartamento Area Giardino |                  101 |                91.97 | €168.87   | 93.20%          | €157.39  | 16.53%                  | HIGH          |
|        2025 | 2025-08      | PEAK          | Appartamento Area Giardino |                  117 |               103.94 | €170.07   | 96.54%          | €164.19  | 16.43%                  | HIGH          |
|        2025 | 2025-09      | SHOULDER      | Appartamento Area Giardino |                   43 |                 9.53 | €204.68   | 31.07%          | €63.60   | 15.69%                  | MEDIUM        |
|        2026 | 2026-05      | LOW           | Appartamento Area Giardino |                   54 |                16.09 | €168.49   | 13.13%          | €22.13   | 10.00%                  | MEDIUM        |
|        2026 | 2026-06      | SHOULDER      | Appartamento Area Giardino |                   73 |                82.21 | €174.13   | 48.10%          | €83.75   | 13.10%                  | MEDIUM        |
|        2026 | 2026-07      | PEAK          | Appartamento Area Giardino |                   86 |               148.22 | €186.12   | 104.64%         | €194.77  | 7.53%                   | MEDIUM        |
|        2024 | 2024-06      | SHOULDER      | Appartamento Area Piscina  |                   81 |                63.43 | €158.08   | 77.41%          | €122.37  | 17.35%                  | MEDIUM        |
|        2024 | 2024-07      | PEAK          | Appartamento Area Piscina  |                   54 |                62.37 | €279.00   | 69.71%          | €194.50  | 17.91%                  | MEDIUM        |
|        2024 | 2024-08      | PEAK          | Appartamento Area Piscina  |                   61 |                60.98 | €338.41   | 86.92%          | €294.14  | 20.51%                  | MEDIUM        |
|        2024 | 2024-09      | SHOULDER      | Appartamento Area Piscina  |                   30 |                49.37 | €175.43   | 39.81%          | €69.85   | 11.76%                  | MEDIUM        |
|        2025 | 2025-06      | SHOULDER      | Appartamento Area Piscina  |                   75 |                33.24 | €164.30   | 61.85%          | €101.62  | 26.47%                  | MEDIUM        |
|        2025 | 2025-07      | PEAK          | Appartamento Area Piscina  |                   71 |                43.25 | €231.26   | 94.27%          | €217.99  | 24.47%                  | MEDIUM        |
|        2025 | 2025-08      | PEAK          | Appartamento Area Piscina  |                   74 |                65.77 | €234.71   | 101.25%         | €237.65  | 18.68%                  | MEDIUM        |
|        2025 | 2025-09      | SHOULDER      | Appartamento Area Piscina  |                   30 |                16.63 | €178.09   | 40.56%          | €72.23   | 23.08%                  | MEDIUM        |
|        2026 | 2026-05      | LOW           | Appartamento Area Piscina  |                   34 |                29.91 | €174.44   | 12.01%          | €20.94   | 8.11%                   | MEDIUM        |
|        2026 | 2026-06      | SHOULDER      | Appartamento Area Piscina  |                   59 |                40.66 | €183.62   | 56.67%          | €104.05  | 11.94%                  | MEDIUM        |
|        2026 | 2026-07      | PEAK          | Appartamento Area Piscina  |                   58 |                59.4  | €274.09   | 91.30%          | €250.23  | 19.44%                  | MEDIUM        |
|        2024 | 2024-06      | SHOULDER      | Camera  Standard           |                   80 |                73.91 | €100.38   | 106.90%         | €107.31  | 13.04%                  | MEDIUM        |
|        2024 | 2024-07      | PEAK          | Camera  Standard           |                   53 |                68.45 | €132.96   | 81.57%          | €108.45  | 23.19%                  | MEDIUM        |
|        2024 | 2024-08      | PEAK          | Camera  Standard           |                   47 |                62.74 | €152.16   | 73.50%          | €111.84  | 29.41%                  | MEDIUM        |
|        2024 | 2024-09      | SHOULDER      | Camera  Standard           |                   33 |                96.88 | €124.16   | 57.62%          | €71.54   | 14.63%                  | MEDIUM        |
|        2025 | 2025-06      | SHOULDER      | Camera  Standard           |                   83 |                36.65 | €129.66   | 70.71%          | €91.69   | 23.15%                  | MEDIUM        |
|        2025 | 2025-07      | PEAK          | Camera  Standard           |                  107 |                40.03 | €151.45   | 107.37%         | €162.62  | 33.12%                  | HIGH          |
|        2025 | 2025-08      | PEAK          | Camera  Standard           |                   87 |                59.86 | €186.46   | 98.39%          | €183.45  | 38.73%                  | MEDIUM        |
|        2025 | 2025-09      | SHOULDER      | Camera  Standard           |                   61 |                13.23 | €123.33   | 51.19%          | €63.13   | 21.79%                  | MEDIUM        |
|        2026 | 2026-06      | SHOULDER      | Camera  Standard           |                   74 |                33.36 | €135.00   | 74.05%          | €99.96   | 18.68%                  | MEDIUM        |
|        2026 | 2026-07      | PEAK          | Camera  Standard           |                   57 |                58.47 | €206.42   | 98.10%          | €202.49  | 18.06%                  | MEDIUM        |
|        2024 | 2024-06      | SHOULDER      | Camera Superior            |                   34 |                55.12 | €135.17   | 68.75%          | €92.93   | 25.00%                  | MEDIUM        |
|        2024 | 2024-07      | PEAK          | Camera Superior            |                   41 |                47.71 | €269.03   | 105.24%         | €283.13  | 15.69%                  | MEDIUM        |
|        2024 | 2024-08      | PEAK          | Camera Superior            |                   39 |                23.82 | €249.71   | 104.84%         | €261.79  | 26.42%                  | MEDIUM        |
|        2025 | 2025-06      | SHOULDER      | Camera Superior            |                   42 |                34.57 | €132.19   | 77.50%          | €102.45  | 26.32%                  | MEDIUM        |
|        2025 | 2025-07      | PEAK          | Camera Superior            |                   50 |                58.94 | €198.84   | 101.21%         | €201.25  | 26.47%                  | MEDIUM        |
|        2025 | 2025-08      | PEAK          | Camera Superior            |                   50 |                62.12 | €240.91   | 109.27%         | €263.26  | 37.50%                  | MEDIUM        |
|        2026 | 2026-06      | SHOULDER      | Camera Superior            |                   44 |                37.61 | €159.01   | 78.75%          | €125.22  | 22.81%                  | MEDIUM        |
|        2026 | 2026-07      | PEAK          | Camera Superior            |                   35 |                53.43 | €245.94   | 113.33%         | €278.73  | 28.57%                  | MEDIUM        |

Use this table to test whether an all-history room profile is structural. For example, an 83-day all-season booking window is only useful if it remains similar across comparable stay periods; large monthly/yearly shifts mean pricing should use period-specific lead times.

### Room × year × season / month × booking window

|   stay_year | stay_month   | season_band   | room_name                  | booking_window_band   |   confirmed_bookings | avg_adr   | revenue    |   avg_los | reliability   |
|------------:|:-------------|:--------------|:---------------------------|:----------------------|---------------------:|:----------|:-----------|----------:|:--------------|
|        2024 | 2024-06      | SHOULDER      | Appartamento Area Giardino | 15-30                 |                   11 | €67.60    | €3,541.50  |      5.18 | LOW           |
|        2024 | 2024-06      | SHOULDER      | Appartamento Area Giardino | 31-60                 |                   12 | €144.02   | €9,255.50  |      5.92 | LOW           |
|        2024 | 2024-06      | SHOULDER      | Appartamento Area Giardino | 61-90                 |                   43 | €83.92    | €27,991.50 |      7.81 | MEDIUM        |
|        2024 | 2024-06      | SHOULDER      | Appartamento Area Giardino | 91-180                |                   34 | €219.04   | €63,563.40 |      8.5  | MEDIUM        |
|        2024 | 2024-07      | PEAK          | Appartamento Area Giardino | 61-90                 |                   17 | €82.13    | €11,011.50 |      8.18 | LOW           |
|        2024 | 2024-07      | PEAK          | Appartamento Area Giardino | 91-180                |                   72 | €100.14   | €64,037.50 |      8.53 | MEDIUM        |
|        2024 | 2024-08      | PEAK          | Appartamento Area Giardino | 91-180                |                   92 | €63.67    | €54,133.00 |      8.18 | MEDIUM        |
|        2024 | 2024-09      | SHOULDER      | Appartamento Area Giardino | 0-7                   |                   21 | €142.36   | €16,899.43 |      5.33 | LOW           |
|        2025 | 2025-06      | SHOULDER      | Appartamento Area Giardino | 0-7                   |                   34 | €167.08   | €19,929.84 |      3.59 | MEDIUM        |
|        2025 | 2025-06      | SHOULDER      | Appartamento Area Giardino | 8-14                  |                   20 | €167.14   | €15,723.28 |      4.5  | LOW           |
|        2025 | 2025-06      | SHOULDER      | Appartamento Area Giardino | 15-30                 |                   18 | €200.27   | €12,483.69 |      3.28 | LOW           |
|        2025 | 2025-06      | SHOULDER      | Appartamento Area Giardino | 91-180                |                   12 | €80.72    | €7,298.00  |      7.92 | LOW           |
|        2025 | 2025-07      | PEAK          | Appartamento Area Giardino | 0-7                   |                   17 | €208.30   | €16,114.00 |      4.65 | LOW           |
|        2025 | 2025-07      | PEAK          | Appartamento Area Giardino | 8-14                  |                   10 | €229.12   | €15,981.50 |      6.6  | LOW           |
|        2025 | 2025-07      | PEAK          | Appartamento Area Giardino | 91-180                |                   63 | €122.69   | €63,198.43 |      8.63 | MEDIUM        |
|        2025 | 2025-08      | PEAK          | Appartamento Area Giardino | 0-7                   |                   21 | €233.18   | €28,852.06 |      5.95 | LOW           |
|        2025 | 2025-08      | PEAK          | Appartamento Area Giardino | 8-14                  |                   10 | €269.51   | €15,439.79 |      5.4  | LOW           |
|        2025 | 2025-08      | PEAK          | Appartamento Area Giardino | 91-180                |                   69 | €110.63   | €67,252.86 |      8.36 | MEDIUM        |
|        2025 | 2025-09      | SHOULDER      | Appartamento Area Giardino | 0-7                   |                   36 | €201.05   | €23,453.54 |      3.22 | MEDIUM        |
|        2026 | 2026-05      | LOW           | Appartamento Area Giardino | 0-7                   |                   26 | €165.17   | €8,548.50  |      1.96 | LOW           |
|        2026 | 2026-05      | LOW           | Appartamento Area Giardino | 15-30                 |                   20 | €152.40   | €10,023.00 |      3.25 | LOW           |
|        2026 | 2026-06      | SHOULDER      | Appartamento Area Giardino | 0-7                   |                   10 | €115.38   | €3,214.27  |      3.2  | LOW           |
|        2026 | 2026-06      | SHOULDER      | Appartamento Area Giardino | 31-60                 |                   13 | €206.11   | €20,105.36 |      7.69 | LOW           |
|        2026 | 2026-06      | SHOULDER      | Appartamento Area Giardino | 61-90                 |                   12 | €207.48   | €21,620.52 |      8.58 | LOW           |
|        2026 | 2026-06      | SHOULDER      | Appartamento Area Giardino | 181+                  |                   17 | €75.22    | €12,771.00 |      8.24 | LOW           |
|        2026 | 2026-07      | PEAK          | Appartamento Area Giardino | 0-7                   |                   10 | €270.53   | €15,102.60 |      4.5  | LOW           |
|        2026 | 2026-07      | PEAK          | Appartamento Area Giardino | 181+                  |                   45 | €95.04    | €30,470.99 |      7.4  | MEDIUM        |
|        2024 | 2024-06      | SHOULDER      | Appartamento Area Piscina  | 0-7                   |                   10 | €135.57   | €9,696.50  |      6.3  | LOW           |
|        2024 | 2024-06      | SHOULDER      | Appartamento Area Piscina  | 31-60                 |                   14 | €234.78   | €24,133.00 |      7.64 | LOW           |
|        2024 | 2024-06      | SHOULDER      | Appartamento Area Piscina  | 61-90                 |                   42 | €120.16   | €26,452.00 |      4.98 | MEDIUM        |
|        2024 | 2024-07      | PEAK          | Appartamento Area Piscina  | 61-90                 |                   10 | €294.71   | €22,641.00 |      7.4  | LOW           |
|        2024 | 2024-07      | PEAK          | Appartamento Area Piscina  | 91-180                |                   16 | €264.08   | €33,772.00 |      7.94 | LOW           |
|        2024 | 2024-08      | PEAK          | Appartamento Area Piscina  | 31-60                 |                   17 | €412.67   | €50,487.50 |      7.18 | LOW           |
|        2024 | 2024-08      | PEAK          | Appartamento Area Piscina  | 91-180                |                   20 | €261.64   | €45,428.50 |      9.45 | LOW           |
|        2025 | 2025-05      | LOW           | Appartamento Area Piscina  | 15-30                 |                   15 | €250.81   | €7,860.05  |      2.13 | LOW           |
|        2025 | 2025-06      | SHOULDER      | Appartamento Area Piscina  | 0-7                   |                   12 | €132.10   | €5,275.31  |      3.42 | LOW           |
|        2025 | 2025-06      | SHOULDER      | Appartamento Area Piscina  | 8-14                  |                   18 | €122.18   | €8,705.06  |      3.83 | LOW           |
|        2025 | 2025-06      | SHOULDER      | Appartamento Area Piscina  | 15-30                 |                   12 | €192.46   | €12,186.46 |      4.75 | LOW           |
|        2025 | 2025-06      | SHOULDER      | Appartamento Area Piscina  | 31-60                 |                   21 | €203.07   | €28,341.44 |      6.52 | LOW           |
|        2025 | 2025-07      | PEAK          | Appartamento Area Piscina  | 0-7                   |                   15 | €203.53   | €14,574.31 |      4.47 | LOW           |
|        2025 | 2025-07      | PEAK          | Appartamento Area Piscina  | 8-14                  |                   10 | €288.28   | €17,027.64 |      6.2  | LOW           |
|        2025 | 2025-07      | PEAK          | Appartamento Area Piscina  | 15-30                 |                   16 | €258.03   | €30,981.84 |      7.56 | LOW           |
|        2025 | 2025-07      | PEAK          | Appartamento Area Piscina  | 61-90                 |                   11 | €223.68   | €22,598.90 |     10.82 | LOW           |
|        2025 | 2025-08      | PEAK          | Appartamento Area Piscina  | 8-14                  |                   11 | €279.51   | €18,781.67 |      6.18 | LOW           |
|        2025 | 2025-08      | PEAK          | Appartamento Area Piscina  | 15-30                 |                   10 | €239.75   | €14,272.33 |      6.3  | LOW           |
|        2025 | 2025-08      | PEAK          | Appartamento Area Piscina  | 31-60                 |                   14 | €284.40   | €30,462.19 |      7.5  | LOW           |
|        2025 | 2025-08      | PEAK          | Appartamento Area Piscina  | 91-180                |                   21 | €193.84   | €39,289.12 |     10.38 | LOW           |
|        2025 | 2025-09      | SHOULDER      | Appartamento Area Piscina  | 0-7                   |                   14 | €157.25   | €10,263.60 |      4.64 | LOW           |
|        2025 | 2025-09      | SHOULDER      | Appartamento Area Piscina  | 15-30                 |                   11 | €204.44   | €10,880.21 |      5    | LOW           |
|        2026 | 2026-05      | LOW           | Appartamento Area Piscina  | 31-60                 |                   15 | €82.13    | €3,082.95  |      2.8  | LOW           |
|        2026 | 2026-06      | SHOULDER      | Appartamento Area Piscina  | 0-7                   |                   15 | €169.41   | €8,491.55  |      3.2  | LOW           |
|        2026 | 2026-06      | SHOULDER      | Appartamento Area Piscina  | 15-30                 |                   16 | €184.82   | €14,584.73 |      4.88 | LOW           |
|        2026 | 2026-06      | SHOULDER      | Appartamento Area Piscina  | 31-60                 |                   10 | €210.02   | €16,556.14 |      7.9  | LOW           |
|        2026 | 2026-07      | PEAK          | Appartamento Area Piscina  | 0-7                   |                   18 | €226.38   | €16,627.80 |      3.11 | LOW           |
|        2026 | 2026-07      | PEAK          | Appartamento Area Piscina  | 31-60                 |                   15 | €300.87   | €31,189.41 |      6.93 | LOW           |
|        2024 | 2024-06      | SHOULDER      | Camera  Standard           | 31-60                 |                   10 | €38.97    | €2,059.46  |      4.4  | LOW           |
|        2024 | 2024-06      | SHOULDER      | Camera  Standard           | 61-90                 |                   36 | €89.74    | €22,666.10 |      7.06 | MEDIUM        |
|        2024 | 2024-06      | SHOULDER      | Camera  Standard           | 91-180                |                   20 | €151.94   | €20,529.00 |      6.75 | LOW           |
|        2024 | 2024-07      | PEAK          | Camera  Standard           | 91-180                |                   23 | €89.68    | €14,079.50 |      6.96 | LOW           |
|        2024 | 2024-08      | PEAK          | Camera  Standard           | 0-7                   |                   18 | €229.03   | €23,652.00 |      5.17 | LOW           |
|        2024 | 2024-08      | PEAK          | Camera  Standard           | 91-180                |                   22 | €53.57    | €15,507.50 |      8.18 | LOW           |
|        2024 | 2024-09      | SHOULDER      | Camera  Standard           | 91-180                |                   12 | €82.37    | €6,798.00  |      6.92 | LOW           |
|        2025 | 2025-06      | SHOULDER      | Camera  Standard           | 0-7                   |                   26 | €108.95   | €6,740.71  |      2.19 | LOW           |
|        2025 | 2025-06      | SHOULDER      | Camera  Standard           | 8-14                  |                   11 | €120.78   | €5,483.85  |      3.45 | LOW           |
|        2025 | 2025-06      | SHOULDER      | Camera  Standard           | 15-30                 |                   13 | €133.13   | €6,536.46  |      3.92 | LOW           |
|        2025 | 2025-06      | SHOULDER      | Camera  Standard           | 31-60                 |                   17 | €143.11   | €8,648.56  |      3.35 | LOW           |
|        2025 | 2025-06      | SHOULDER      | Camera  Standard           | 91-180                |                   10 | €160.18   | €10,848.13 |      6.6  | LOW           |
|        2025 | 2025-07      | PEAK          | Camera  Standard           | 0-7                   |                   27 | €97.30    | €7,708.20  |      2.7  | LOW           |
|        2025 | 2025-07      | PEAK          | Camera  Standard           | 8-14                  |                   15 | €156.64   | €8,537.32  |      3.33 | LOW           |
|        2025 | 2025-07      | PEAK          | Camera  Standard           | 15-30                 |                   15 | €150.37   | €11,751.01 |      4    | LOW           |
|        2025 | 2025-07      | PEAK          | Camera  Standard           | 31-60                 |                   20 | €179.74   | €20,066.66 |      5.6  | LOW           |
|        2025 | 2025-07      | PEAK          | Camera  Standard           | 61-90                 |                   19 | €178.81   | €17,583.27 |      5.21 | LOW           |
|        2025 | 2025-07      | PEAK          | Camera  Standard           | 91-180                |                   10 | €179.67   | €11,629.48 |      6.4  | LOW           |
|        2025 | 2025-08      | PEAK          | Camera  Standard           | 0-7                   |                   19 | €138.34   | €7,638.87  |      2.95 | LOW           |
|        2025 | 2025-08      | PEAK          | Camera  Standard           | 15-30                 |                   15 | €119.85   | €8,105.51  |      3.53 | LOW           |
|        2025 | 2025-08      | PEAK          | Camera  Standard           | 61-90                 |                   11 | €237.94   | €20,854.09 |      7.18 | LOW           |
|        2025 | 2025-08      | PEAK          | Camera  Standard           | 91-180                |                   24 | €205.43   | €37,277.71 |      7.33 | LOW           |
|        2025 | 2025-09      | SHOULDER      | Camera  Standard           | 0-7                   |                   33 | €113.02   | €9,173.59  |      2.39 | MEDIUM        |
|        2025 | 2025-09      | SHOULDER      | Camera  Standard           | 8-14                  |                   12 | €119.02   | €5,339.05  |      3.58 | LOW           |
|        2025 | 2025-09      | SHOULDER      | Camera  Standard           | 15-30                 |                   11 | €146.30   | €3,566.00  |      2.18 | LOW           |
|        2025 | 2025-11      | LOW           | Camera  Standard           | 0-7                   |                   13 | €0.00     | €0.00      |      1    | LOW           |
|        2026 | 2026-05      | LOW           | Camera  Standard           | 15-30                 |                   12 | €263.79   | €9,954.59  |      2.67 | LOW           |
|        2026 | 2026-05      | LOW           | Camera  Standard           | 31-60                 |                   11 | €75.61    | €2,889.99  |      3.27 | LOW           |
|        2026 | 2026-06      | SHOULDER      | Camera  Standard           | 0-7                   |                   24 | €99.15    | €6,029.24  |      2.54 | LOW           |
|        2026 | 2026-06      | SHOULDER      | Camera  Standard           | 15-30                 |                   14 | €157.11   | €8,944.46  |      4.07 | LOW           |
|        2026 | 2026-06      | SHOULDER      | Camera  Standard           | 31-60                 |                   11 | €142.26   | €10,500.93 |      6.64 | LOW           |
|        2026 | 2026-07      | PEAK          | Camera  Standard           | 31-60                 |                   10 | €219.95   | €11,997.05 |      5.6  | LOW           |
|        2026 | 2026-07      | PEAK          | Camera  Standard           | 61-90                 |                   15 | €207.83   | €21,853.41 |      7    | LOW           |
|        2026 | 2026-07      | PEAK          | Camera  Standard           | 91-180                |                   11 | €198.53   | €16,781.39 |      7.73 | LOW           |
|        2024 | 2024-06      | SHOULDER      | Camera Deluxe              | 91-180                |                   12 | €227.57   | €18,837.00 |      6.92 | LOW           |
|        2024 | 2024-07      | PEAK          | Camera Deluxe              | 91-180                |                   11 | €302.29   | €24,323.50 |      7.27 | LOW           |
|        2024 | 2024-08      | PEAK          | Camera Deluxe              | 0-7                   |                   11 | €298.27   | €21,351.50 |      6.55 | LOW           |
|        2024 | 2024-07      | PEAK          | Camera Superior            | 0-7                   |                   12 | €226.65   | €14,194.55 |      4.67 | LOW           |
|        2024 | 2024-07      | PEAK          | Camera Superior            | 8-14                  |                   11 | €297.52   | €16,345.50 |      4.82 | LOW           |
|        2024 | 2024-07      | PEAK          | Camera Superior            | 91-180                |                   13 | €246.39   | €25,887.00 |      7.92 | LOW           |
|        2024 | 2024-08      | PEAK          | Camera Superior            | 0-7                   |                   22 | €218.90   | €33,351.50 |      6.14 | LOW           |
|        2025 | 2025-06      | SHOULDER      | Camera Superior            | 0-7                   |                   10 | €122.66   | €3,331.55  |      2.6  | LOW           |
|        2025 | 2025-06      | SHOULDER      | Camera Superior            | 31-60                 |                   12 | €124.03   | €8,638.51  |      5.25 | LOW           |
|        2025 | 2025-07      | PEAK          | Camera Superior            | 0-7                   |                   11 | €158.48   | €3,031.66  |      1.64 | LOW           |
|        2025 | 2025-07      | PEAK          | Camera Superior            | 31-60                 |                   10 | €220.91   | €13,284.58 |      5.9  | LOW           |
|        2025 | 2025-07      | PEAK          | Camera Superior            | 91-180                |                   12 | €199.72   | €15,158.95 |      6.33 | LOW           |
|        2025 | 2025-08      | PEAK          | Camera Superior            | 31-60                 |                   11 | €270.24   | €16,478.29 |      5.55 | LOW           |
|        2025 | 2025-08      | PEAK          | Camera Superior            | 91-180                |                   16 | €280.64   | €34,147.50 |      7.62 | LOW           |
|        2025 | 2025-09      | SHOULDER      | Camera Superior            | 0-7                   |                   14 | €121.37   | €3,397.74  |      1.71 | LOW           |
|        2026 | 2026-05      | LOW           | Camera Superior            | 15-30                 |                   10 | €148.29   | €4,068.63  |      2.5  | LOW           |
|        2026 | 2026-06      | SHOULDER      | Camera Superior            | 0-7                   |                   10 | €106.26   | €2,264.89  |      2.2  | LOW           |
|        2026 | 2026-06      | SHOULDER      | Camera Superior            | 31-60                 |                   16 | €175.48   | €17,316.12 |      5.75 | LOW           |

This is the core table for understanding **when each room is actually booked** and whether realized ADR changes as arrival approaches.

### Conversion × room × year × season / month × booking window

|   stay_year | stay_month   | season_band   | room_name                     | booking_window_band   |   quoted_requests |   same_room_converted_requests | same_room_conversion_pct   | overall_conversion_pct   | avg_quote_amount   |
|------------:|:-------------|:--------------|:------------------------------|:----------------------|------------------:|-------------------------------:|:---------------------------|:-------------------------|:-------------------|
|        2024 | 2024-06      | SHOULDER      | Appartamento Area Giardino    | 8-14                  |                30 |                              2 | 6.67%                      | 6.67%                    | €1,560.00          |
|        2024 | 2024-06      | SHOULDER      | Appartamento Area Giardino    | 15-30                 |                87 |                              0 | 0.00%                      | 1.15%                    | €1,607.24          |
|        2024 | 2024-06      | SHOULDER      | Appartamento Area Giardino    | 31-60                 |                58 |                              2 | 3.45%                      | 6.90%                    | €2,136.65          |
|        2024 | 2024-06      | SHOULDER      | Appartamento Area Giardino    | 91-180                |                75 |                              8 | 10.67%                     | 13.33%                   | €1,879.58          |
|        2024 | 2024-07      | PEAK          | Appartamento Area Giardino    | 8-14                  |                43 |                              4 | 9.30%                      | 11.63%                   | €2,617.48          |
|        2024 | 2024-07      | PEAK          | Appartamento Area Giardino    | 91-180                |               112 |                              6 | 5.36%                      | 7.14%                    | €2,789.16          |
|        2024 | 2024-07      | PEAK          | Appartamento Area Giardino    | 181+                  |                47 |                              5 | 10.64%                     | 12.77%                   | €2,869.94          |
|        2024 | 2024-08      | PEAK          | Appartamento Area Giardino    | 31-60                 |                38 |                              0 | 0.00%                      | 2.63%                    | €4,420.79          |
|        2024 | 2024-08      | PEAK          | Appartamento Area Giardino    | 91-180                |               115 |                              4 | 3.48%                      | 4.35%                    | €3,703.39          |
|        2024 | 2024-08      | PEAK          | Appartamento Area Giardino    | 181+                  |                90 |                              3 | 3.33%                      | 3.33%                    | €3,959.22          |
|        2024 | 2024-09      | SHOULDER      | Appartamento Area Giardino    | 8-14                  |                64 |                              1 | 1.56%                      | 1.56%                    | €1,734.79          |
|        2024 | 2024-09      | SHOULDER      | Appartamento Area Giardino    | 15-30                 |                55 |                              1 | 1.82%                      | 1.82%                    | €1,467.15          |
|        2024 | 2024-09      | SHOULDER      | Appartamento Area Giardino    | 61-90                 |                48 |                              1 | 2.08%                      | 2.08%                    | €1,889.54          |
|        2024 | 2024-09      | SHOULDER      | Appartamento Area Giardino    | 91-180                |                83 |                              0 | 0.00%                      | 2.41%                    | €1,819.72          |
|        2025 | 2025-05      | LOW           | Appartamento Area Giardino    | 15-30                 |                39 |                              2 | 5.13%                      | 7.69%                    | €575.80            |
|        2025 | 2025-06      | SHOULDER      | Appartamento Area Giardino    | 0-7                   |                55 |                             12 | 21.82%                     | 23.64%                   | €863.29            |
|        2025 | 2025-06      | SHOULDER      | Appartamento Area Giardino    | 8-14                  |                69 |                              7 | 10.14%                     | 11.59%                   | €1,232.70          |
|        2025 | 2025-06      | SHOULDER      | Appartamento Area Giardino    | 15-30                 |               119 |                              2 | 1.68%                      | 4.20%                    | €1,647.89          |
|        2025 | 2025-06      | SHOULDER      | Appartamento Area Giardino    | 31-60                 |                88 |                              3 | 3.41%                      | 3.41%                    | €2,029.42          |
|        2025 | 2025-06      | SHOULDER      | Appartamento Area Giardino    | 61-90                 |                53 |                              1 | 1.89%                      | 3.77%                    | €2,356.65          |
|        2025 | 2025-06      | SHOULDER      | Appartamento Area Giardino    | 91-180                |                43 |                              0 | 0.00%                      | 2.33%                    | €2,658.75          |
|        2025 | 2025-07      | PEAK          | Appartamento Area Giardino    | 0-7                   |                71 |                              2 | 2.82%                      | 4.23%                    | €1,703.06          |
|        2025 | 2025-07      | PEAK          | Appartamento Area Giardino    | 8-14                  |                62 |                              3 | 4.84%                      | 8.06%                    | €1,966.57          |
|        2025 | 2025-07      | PEAK          | Appartamento Area Giardino    | 15-30                 |               129 |                              3 | 2.33%                      | 3.88%                    | €2,203.71          |
|        2025 | 2025-07      | PEAK          | Appartamento Area Giardino    | 31-60                 |                47 |                              1 | 2.13%                      | 2.13%                    | €2,783.01          |
|        2025 | 2025-07      | PEAK          | Appartamento Area Giardino    | 61-90                 |                35 |                              0 | 0.00%                      | 0.00%                    | €2,854.84          |
|        2025 | 2025-07      | PEAK          | Appartamento Area Giardino    | 91-180                |               116 |                              4 | 3.45%                      | 3.45%                    | €3,106.34          |
|        2025 | 2025-08      | PEAK          | Appartamento Area Giardino    | 0-7                   |                82 |                              7 | 8.54%                      | 9.76%                    | €1,673.00          |
|        2025 | 2025-08      | PEAK          | Appartamento Area Giardino    | 8-14                  |                63 |                              5 | 7.94%                      | 7.94%                    | €1,775.17          |
|        2025 | 2025-08      | PEAK          | Appartamento Area Giardino    | 15-30                 |                64 |                              3 | 4.69%                      | 4.69%                    | €2,406.41          |
|        2025 | 2025-08      | PEAK          | Appartamento Area Giardino    | 31-60                 |                81 |                              1 | 1.23%                      | 1.23%                    | €3,201.76          |
|        2025 | 2025-08      | PEAK          | Appartamento Area Giardino    | 61-90                 |               164 |                              2 | 1.22%                      | 1.22%                    | €3,161.04          |
|        2025 | 2025-08      | PEAK          | Appartamento Area Giardino    | 91-180                |               172 |                              0 | 0.00%                      | 0.58%                    | €3,480.77          |
|        2025 | 2025-09      | SHOULDER      | Appartamento Area Giardino    | 0-7                   |                33 |                              8 | 24.24%                     | 24.24%                   | €896.05            |
|        2026 | 2026-05      | LOW           | Appartamento Area Giardino    | 0-7                   |                36 |                              3 | 8.33%                      | 8.33%                    | €361.02            |
|        2026 | 2026-06      | SHOULDER      | Appartamento Area Giardino    | 0-7                   |                59 |                              3 | 5.08%                      | 6.78%                    | €1,159.00          |
|        2026 | 2026-06      | SHOULDER      | Appartamento Area Giardino    | 8-14                  |                32 |                              0 | 0.00%                      | 0.00%                    | €1,368.81          |
|        2026 | 2026-06      | SHOULDER      | Appartamento Area Giardino    | 15-30                 |                64 |                              4 | 6.25%                      | 9.38%                    | €1,426.13          |
|        2026 | 2026-06      | SHOULDER      | Appartamento Area Giardino    | 31-60                 |                69 |                              1 | 1.45%                      | 1.45%                    | €1,633.69          |
|        2026 | 2026-06      | SHOULDER      | Appartamento Area Giardino    | 61-90                 |               115 |                              4 | 3.48%                      | 4.35%                    | €2,060.85          |
|        2026 | 2026-06      | SHOULDER      | Appartamento Area Giardino    | 91-180                |                51 |                              3 | 5.88%                      | 5.88%                    | €2,411.08          |
|        2026 | 2026-07      | PEAK          | Appartamento Area Giardino    | 0-7                   |                61 |                              1 | 1.64%                      | 1.64%                    | €2,280.32          |
|        2026 | 2026-07      | PEAK          | Appartamento Area Giardino    | 8-14                  |                65 |                              0 | 0.00%                      | 0.00%                    | €2,607.06          |
|        2026 | 2026-07      | PEAK          | Appartamento Area Giardino    | 15-30                 |                84 |                              1 | 1.19%                      | 1.19%                    | €2,579.15          |
|        2026 | 2026-07      | PEAK          | Appartamento Area Giardino    | 31-60                 |                70 |                              2 | 2.86%                      | 2.86%                    | €2,455.77          |
|        2026 | 2026-07      | PEAK          | Appartamento Area Giardino    | 61-90                 |                60 |                              3 | 5.00%                      | 5.00%                    | €2,494.12          |
|        2026 | 2026-07      | PEAK          | Appartamento Area Giardino    | 91-180                |               159 |                              5 | 3.14%                      | 5.66%                    | €3,235.65          |
|        2024 | 2024-06      | SHOULDER      | Appartamento Area Piscina     | 0-7                   |                42 |                              2 | 4.76%                      | 4.76%                    | €1,493.42          |
|        2024 | 2024-06      | SHOULDER      | Appartamento Area Piscina     | 8-14                  |                32 |                              0 | 0.00%                      | 3.12%                    | €1,917.22          |
|        2024 | 2024-06      | SHOULDER      | Appartamento Area Piscina     | 15-30                 |               105 |                              1 | 0.95%                      | 0.95%                    | €2,060.14          |
|        2024 | 2024-06      | SHOULDER      | Appartamento Area Piscina     | 31-60                 |                58 |                              3 | 5.17%                      | 6.90%                    | €2,444.44          |
|        2024 | 2024-06      | SHOULDER      | Appartamento Area Piscina     | 61-90                 |                48 |                              3 | 6.25%                      | 6.25%                    | €2,319.93          |
|        2024 | 2024-06      | SHOULDER      | Appartamento Area Piscina     | 91-180                |                54 |                              4 | 7.41%                      | 9.26%                    | €1,944.45          |
|        2024 | 2024-07      | PEAK          | Appartamento Area Piscina     | 8-14                  |                42 |                              2 | 4.76%                      | 4.76%                    | €2,602.46          |
|        2024 | 2024-07      | PEAK          | Appartamento Area Piscina     | 15-30                 |               137 |                              3 | 2.19%                      | 2.92%                    | €2,812.56          |
|        2024 | 2024-07      | PEAK          | Appartamento Area Piscina     | 31-60                 |                87 |                              2 | 2.30%                      | 3.45%                    | €3,397.38          |
|        2024 | 2024-07      | PEAK          | Appartamento Area Piscina     | 61-90                 |                66 |                              2 | 3.03%                      | 3.03%                    | €3,458.67          |
|        2024 | 2024-07      | PEAK          | Appartamento Area Piscina     | 91-180                |               110 |                              8 | 7.27%                      | 10.00%                   | €2,845.15          |
|        2024 | 2024-08      | PEAK          | Appartamento Area Piscina     | 15-30                 |                54 |                              2 | 3.70%                      | 3.70%                    | €3,325.46          |
|        2024 | 2024-08      | PEAK          | Appartamento Area Piscina     | 31-60                 |               161 |                              9 | 5.59%                      | 5.59%                    | €3,810.61          |
|        2024 | 2024-08      | PEAK          | Appartamento Area Piscina     | 61-90                 |                87 |                              0 | 0.00%                      | 0.00%                    | €4,156.72          |
|        2024 | 2024-08      | PEAK          | Appartamento Area Piscina     | 91-180                |               188 |                              7 | 3.72%                      | 4.26%                    | €3,970.14          |
|        2024 | 2024-09      | SHOULDER      | Appartamento Area Piscina     | 15-30                 |                34 |                              3 | 8.82%                      | 8.82%                    | €1,460.26          |
|        2024 | 2024-09      | SHOULDER      | Appartamento Area Piscina     | 31-60                 |                31 |                              1 | 3.23%                      | 3.23%                    | €1,752.69          |
|        2024 | 2024-09      | SHOULDER      | Appartamento Area Piscina     | 91-180                |                43 |                              2 | 4.65%                      | 4.65%                    | €1,786.22          |
|        2025 | 2025-06      | SHOULDER      | Appartamento Area Piscina     | 8-14                  |                31 |                              4 | 12.90%                     | 19.35%                   | €938.29            |
|        2025 | 2025-06      | SHOULDER      | Appartamento Area Piscina     | 15-30                 |                59 |                              4 | 6.78%                      | 6.78%                    | €1,344.03          |
|        2025 | 2025-06      | SHOULDER      | Appartamento Area Piscina     | 31-60                 |               185 |                              7 | 3.78%                      | 4.86%                    | €1,897.03          |
|        2025 | 2025-06      | SHOULDER      | Appartamento Area Piscina     | 61-90                 |                86 |                              2 | 2.33%                      | 3.49%                    | €2,069.68          |
|        2025 | 2025-06      | SHOULDER      | Appartamento Area Piscina     | 91-180                |                65 |                              0 | 0.00%                      | 0.00%                    | €2,282.87          |
|        2025 | 2025-07      | PEAK          | Appartamento Area Piscina     | 0-7                   |                54 |                              3 | 5.56%                      | 9.26%                    | €1,631.20          |
|        2025 | 2025-07      | PEAK          | Appartamento Area Piscina     | 8-14                  |                94 |                              2 | 2.13%                      | 3.19%                    | €1,860.16          |
|        2025 | 2025-07      | PEAK          | Appartamento Area Piscina     | 15-30                 |               191 |                              6 | 3.14%                      | 4.19%                    | €2,162.25          |
|        2025 | 2025-07      | PEAK          | Appartamento Area Piscina     | 31-60                 |               211 |                              2 | 0.95%                      | 1.42%                    | €2,373.17          |
|        2025 | 2025-07      | PEAK          | Appartamento Area Piscina     | 61-90                 |                78 |                              1 | 1.28%                      | 1.28%                    | €2,320.71          |
|        2025 | 2025-07      | PEAK          | Appartamento Area Piscina     | 91-180                |               147 |                              4 | 2.72%                      | 3.40%                    | €2,687.18          |
|        2025 | 2025-08      | PEAK          | Appartamento Area Piscina     | 8-14                  |                51 |                              5 | 9.80%                      | 9.80%                    | €2,004.26          |
|        2025 | 2025-08      | PEAK          | Appartamento Area Piscina     | 15-30                 |               202 |                              5 | 2.48%                      | 3.47%                    | €2,286.39          |
|        2025 | 2025-08      | PEAK          | Appartamento Area Piscina     | 31-60                 |               297 |                              3 | 1.01%                      | 1.01%                    | €2,793.96          |
|        2025 | 2025-08      | PEAK          | Appartamento Area Piscina     | 61-90                 |               291 |                              4 | 1.37%                      | 1.37%                    | €2,993.67          |
|        2025 | 2025-08      | PEAK          | Appartamento Area Piscina     | 91-180                |               321 |                              3 | 0.93%                      | 1.87%                    | €3,049.73          |
|        2026 | 2026-06      | SHOULDER      | Appartamento Area Piscina     | 0-7                   |                41 |                              1 | 2.44%                      | 2.44%                    | €816.98            |
|        2026 | 2026-06      | SHOULDER      | Appartamento Area Piscina     | 8-14                  |                38 |                              2 | 5.26%                      | 5.26%                    | €1,198.67          |
|        2026 | 2026-06      | SHOULDER      | Appartamento Area Piscina     | 15-30                 |                82 |                              2 | 2.44%                      | 4.88%                    | €1,412.47          |
|        2026 | 2026-06      | SHOULDER      | Appartamento Area Piscina     | 31-60                 |                62 |                              1 | 1.61%                      | 3.23%                    | €1,631.42          |
|        2026 | 2026-06      | SHOULDER      | Appartamento Area Piscina     | 61-90                 |                64 |                              1 | 1.56%                      | 1.56%                    | €1,954.94          |
|        2026 | 2026-06      | SHOULDER      | Appartamento Area Piscina     | 91-180                |               197 |                              0 | 0.00%                      | 1.52%                    | €2,333.16          |
|        2026 | 2026-07      | PEAK          | Appartamento Area Piscina     | 0-7                   |                62 |                              1 | 1.61%                      | 1.61%                    | €1,998.46          |
|        2026 | 2026-07      | PEAK          | Appartamento Area Piscina     | 8-14                  |                88 |                              2 | 2.27%                      | 2.27%                    | €2,546.25          |
|        2026 | 2026-07      | PEAK          | Appartamento Area Piscina     | 15-30                 |               154 |                              0 | 0.00%                      | 0.00%                    | €2,762.33          |
|        2026 | 2026-07      | PEAK          | Appartamento Area Piscina     | 31-60                 |               146 |                              0 | 0.00%                      | 0.68%                    | €2,515.67          |
|        2026 | 2026-07      | PEAK          | Appartamento Area Piscina     | 61-90                 |               143 |                              0 | 0.00%                      | 1.40%                    | €2,964.72          |
|        2026 | 2026-07      | PEAK          | Appartamento Area Piscina     | 91-180                |               539 |                              4 | 0.74%                      | 2.04%                    | €3,206.27          |
|        2026 | 2026-07      | PEAK          | Appartamento Area Piscina     | 181+                  |                59 |                              1 | 1.69%                      | 1.69%                    | €3,373.19          |
|        2024 | 2024-06      | SHOULDER      | Camera  Standard              | 15-30                 |                33 |                              1 | 3.03%                      | 3.03%                    | €1,532.42          |
|        2024 | 2024-06      | SHOULDER      | Camera  Standard              | 91-180                |               104 |                              4 | 3.85%                      | 4.81%                    | €1,328.07          |
|        2024 | 2024-07      | PEAK          | Camera  Standard              | 8-14                  |                50 |                              1 | 2.00%                      | 4.00%                    | €1,948.93          |
|        2024 | 2024-07      | PEAK          | Camera  Standard              | 15-30                 |                80 |                              4 | 5.00%                      | 5.00%                    | €2,369.25          |
|        2024 | 2024-07      | PEAK          | Camera  Standard              | 31-60                 |                57 |                              1 | 1.75%                      | 1.75%                    | €2,326.67          |
|        2024 | 2024-07      | PEAK          | Camera  Standard              | 61-90                 |                31 |                              2 | 6.45%                      | 6.45%                    | €2,377.06          |
|        2024 | 2024-07      | PEAK          | Camera  Standard              | 91-180                |                90 |                              2 | 2.22%                      | 3.33%                    | €1,948.19          |
|        2024 | 2024-08      | PEAK          | Camera  Standard              | 0-7                   |                70 |                              9 | 12.86%                     | 12.86%                   | €1,983.54          |
|        2024 | 2024-08      | PEAK          | Camera  Standard              | 8-14                  |                46 |                              0 | 0.00%                      | 2.17%                    | €2,446.52          |
|        2024 | 2024-08      | PEAK          | Camera  Standard              | 15-30                 |                91 |                              4 | 4.40%                      | 4.40%                    | €2,809.37          |
|        2024 | 2024-08      | PEAK          | Camera  Standard              | 31-60                 |               122 |                              2 | 1.64%                      | 2.46%                    | €3,096.89          |
|        2024 | 2024-08      | PEAK          | Camera  Standard              | 61-90                 |               100 |                              0 | 0.00%                      | 0.00%                    | €3,236.57          |
|        2024 | 2024-08      | PEAK          | Camera  Standard              | 91-180                |               137 |                              0 | 0.00%                      | 0.73%                    | €3,213.75          |
|        2024 | 2024-08      | PEAK          | Camera  Standard              | 181+                  |                61 |                              0 | 0.00%                      | 0.00%                    | €3,152.30          |
|        2024 | 2024-09      | SHOULDER      | Camera  Standard              | 8-14                  |                37 |                              1 | 2.70%                      | 2.70%                    | €1,107.16          |
|        2024 | 2024-09      | SHOULDER      | Camera  Standard              | 15-30                 |                85 |                              2 | 2.35%                      | 2.35%                    | €1,131.25          |
|        2024 | 2024-09      | SHOULDER      | Camera  Standard              | 31-60                 |                55 |                              3 | 5.45%                      | 5.45%                    | €1,192.67          |
|        2024 | 2024-09      | SHOULDER      | Camera  Standard              | 61-90                 |                53 |                              0 | 0.00%                      | 0.00%                    | €1,238.58          |
|        2024 | 2024-09      | SHOULDER      | Camera  Standard              | 91-180                |                77 |                              2 | 2.60%                      | 2.60%                    | €1,331.30          |
|        2025 | 2025-06      | SHOULDER      | Camera  Standard              | 8-14                  |                30 |                              5 | 16.67%                     | 20.00%                   | €612.39            |
|        2025 | 2025-06      | SHOULDER      | Camera  Standard              | 15-30                 |                62 |                              3 | 4.84%                      | 4.84%                    | €881.24            |
|        2025 | 2025-06      | SHOULDER      | Camera  Standard              | 31-60                 |               118 |                              1 | 0.85%                      | 1.69%                    | €1,046.23          |
|        2025 | 2025-06      | SHOULDER      | Camera  Standard              | 61-90                 |                87 |                              3 | 3.45%                      | 4.60%                    | €1,446.86          |
|        2025 | 2025-06      | SHOULDER      | Camera  Standard              | 91-180                |                50 |                              3 | 6.00%                      | 6.00%                    | €1,544.16          |
|        2025 | 2025-07      | PEAK          | Camera  Standard              | 15-30                 |                54 |                              8 | 14.81%                     | 14.81%                   | €1,221.26          |
|        2025 | 2025-07      | PEAK          | Camera  Standard              | 31-60                 |               121 |                              6 | 4.96%                      | 5.79%                    | €1,503.79          |
|        2025 | 2025-07      | PEAK          | Camera  Standard              | 61-90                 |                85 |                              1 | 1.18%                      | 1.18%                    | €1,574.70          |
|        2025 | 2025-07      | PEAK          | Camera  Standard              | 91-180                |               163 |                              2 | 1.23%                      | 1.84%                    | €1,860.57          |
|        2025 | 2025-08      | PEAK          | Camera  Standard              | 0-7                   |                35 |                              7 | 20.00%                     | 20.00%                   | €688.13            |
|        2025 | 2025-08      | PEAK          | Camera  Standard              | 15-30                 |                54 |                              5 | 9.26%                      | 9.26%                    | €1,148.65          |
|        2025 | 2025-08      | PEAK          | Camera  Standard              | 31-60                 |               115 |                              2 | 1.74%                      | 3.48%                    | €1,613.89          |
|        2025 | 2025-08      | PEAK          | Camera  Standard              | 61-90                 |               125 |                              3 | 2.40%                      | 3.20%                    | €1,799.75          |
|        2025 | 2025-08      | PEAK          | Camera  Standard              | 91-180                |               283 |                              3 | 1.06%                      | 1.41%                    | €1,931.78          |
|        2025 | 2025-09      | SHOULDER      | Camera  Standard              | 8-14                  |                36 |                              2 | 5.56%                      | 8.33%                    | €524.61            |
|        2025 | 2025-09      | SHOULDER      | Camera  Standard              | 15-30                 |                55 |                              1 | 1.82%                      | 1.82%                    | €594.89            |
|        2025 | 2025-09      | SHOULDER      | Camera  Standard              | 31-60                 |                60 |                              4 | 6.67%                      | 6.67%                    | €857.96            |
|        2025 | 2025-09      | SHOULDER      | Camera  Standard              | 61-90                 |                32 |                              1 | 3.12%                      | 3.12%                    | €1,047.86          |
|        2025 | 2025-09      | SHOULDER      | Camera  Standard              | 91-180                |                39 |                              0 | 0.00%                      | 0.00%                    | €1,388.17          |
|        2026 | 2026-06      | SHOULDER      | Camera  Standard              | 15-30                 |                32 |                              2 | 6.25%                      | 9.38%                    | €566.66            |
|        2026 | 2026-06      | SHOULDER      | Camera  Standard              | 31-60                 |                70 |                              4 | 5.71%                      | 5.71%                    | €1,064.03          |
|        2026 | 2026-06      | SHOULDER      | Camera  Standard              | 61-90                 |                93 |                              1 | 1.08%                      | 2.15%                    | €1,223.82          |
|        2026 | 2026-06      | SHOULDER      | Camera  Standard              | 91-180                |               118 |                              3 | 2.54%                      | 2.54%                    | €1,412.39          |
|        2026 | 2026-07      | PEAK          | Camera  Standard              | 15-30                 |                33 |                              1 | 3.03%                      | 3.03%                    | €1,130.90          |
|        2026 | 2026-07      | PEAK          | Camera  Standard              | 31-60                 |                73 |                              2 | 2.74%                      | 2.74%                    | €1,777.06          |
|        2026 | 2026-07      | PEAK          | Camera  Standard              | 61-90                 |               123 |                              4 | 3.25%                      | 4.88%                    | €1,596.55          |
|        2026 | 2026-07      | PEAK          | Camera  Standard              | 91-180                |               253 |                              4 | 1.58%                      | 1.58%                    | €1,939.06          |
|        2024 | 2024-06      | SHOULDER      | Camera Deluxe                 | 91-180                |                53 |                              5 | 9.43%                      | 11.32%                   | €1,886.16          |
|        2024 | 2024-07      | PEAK          | Camera Deluxe                 | 8-14                  |                53 |                              2 | 3.77%                      | 5.66%                    | €2,725.98          |
|        2024 | 2024-07      | PEAK          | Camera Deluxe                 | 15-30                 |                52 |                              2 | 3.85%                      | 5.77%                    | €2,659.76          |
|        2024 | 2024-07      | PEAK          | Camera Deluxe                 | 31-60                 |                66 |                              0 | 0.00%                      | 4.55%                    | €2,795.05          |
|        2024 | 2024-07      | PEAK          | Camera Deluxe                 | 91-180                |                62 |                              3 | 4.84%                      | 4.84%                    | €2,598.99          |
|        2024 | 2024-07      | PEAK          | Camera Deluxe                 | 181+                  |                30 |                              0 | 0.00%                      | 0.00%                    | €2,748.33          |
|        2024 | 2024-08      | PEAK          | Camera Deluxe                 | 0-7                   |                30 |                              2 | 6.67%                      | 10.00%                   | €2,628.87          |
|        2024 | 2024-08      | PEAK          | Camera Deluxe                 | 8-14                  |                67 |                              1 | 1.49%                      | 4.48%                    | €3,080.17          |
|        2024 | 2024-08      | PEAK          | Camera Deluxe                 | 15-30                 |               160 |                              1 | 0.62%                      | 1.25%                    | €3,425.85          |
|        2024 | 2024-08      | PEAK          | Camera Deluxe                 | 31-60                 |               106 |                              0 | 0.00%                      | 0.94%                    | €3,461.46          |
|        2024 | 2024-08      | PEAK          | Camera Deluxe                 | 61-90                 |                65 |                              1 | 1.54%                      | 1.54%                    | €3,655.64          |
|        2024 | 2024-08      | PEAK          | Camera Deluxe                 | 91-180                |                98 |                              4 | 4.08%                      | 5.10%                    | €3,865.41          |
|        2024 | 2024-08      | PEAK          | Camera Deluxe                 | 181+                  |                45 |                              0 | 0.00%                      | 2.22%                    | €4,005.19          |
|        2024 | 2024-09      | SHOULDER      | Camera Deluxe                 | 31-60                 |                33 |                              1 | 3.03%                      | 3.03%                    | €1,807.47          |
|        2024 | 2024-09      | SHOULDER      | Camera Deluxe                 | 61-90                 |                32 |                              1 | 3.12%                      | 3.12%                    | €1,801.46          |
|        2024 | 2024-09      | SHOULDER      | Camera Deluxe                 | 91-180                |                49 |                              0 | 0.00%                      | 0.00%                    | €1,771.02          |
|        2025 | 2025-06      | SHOULDER      | Camera Deluxe                 | 15-30                 |                49 |                              1 | 2.04%                      | 2.04%                    | €1,360.04          |
|        2025 | 2025-06      | SHOULDER      | Camera Deluxe                 | 31-60                 |               109 |                              2 | 1.83%                      | 3.67%                    | €1,434.91          |
|        2025 | 2025-06      | SHOULDER      | Camera Deluxe                 | 61-90                 |                65 |                              1 | 1.54%                      | 3.08%                    | €1,859.02          |
|        2025 | 2025-07      | PEAK          | Camera Deluxe                 | 15-30                 |                46 |                              3 | 6.52%                      | 6.52%                    | €2,095.40          |
|        2025 | 2025-07      | PEAK          | Camera Deluxe                 | 31-60                 |                73 |                              0 | 0.00%                      | 0.00%                    | €2,395.79          |
|        2025 | 2025-07      | PEAK          | Camera Deluxe                 | 61-90                 |               111 |                              2 | 1.80%                      | 1.80%                    | €2,503.61          |
|        2025 | 2025-07      | PEAK          | Camera Deluxe                 | 91-180                |               259 |                              1 | 0.39%                      | 1.16%                    | €2,740.00          |
|        2025 | 2025-08      | PEAK          | Camera Deluxe                 | 31-60                 |                64 |                              1 | 1.56%                      | 1.56%                    | €2,195.68          |
|        2025 | 2025-08      | PEAK          | Camera Deluxe                 | 61-90                 |                82 |                              2 | 2.44%                      | 2.44%                    | €2,940.33          |
|        2025 | 2025-08      | PEAK          | Camera Deluxe                 | 91-180                |               464 |                              1 | 0.22%                      | 1.51%                    | €3,298.46          |
|        2025 | 2025-09      | SHOULDER      | Camera Deluxe                 | 8-14                  |                40 |                              3 | 7.50%                      | 7.50%                    | €1,003.39          |
|        2026 | 2026-06      | SHOULDER      | Camera Deluxe                 | 15-30                 |                72 |                              1 | 1.39%                      | 4.17%                    | €1,547.13          |
|        2026 | 2026-06      | SHOULDER      | Camera Deluxe                 | 31-60                 |               106 |                              0 | 0.00%                      | 1.89%                    | €1,713.15          |
|        2026 | 2026-06      | SHOULDER      | Camera Deluxe                 | 61-90                 |                84 |                              0 | 0.00%                      | 4.76%                    | €2,261.74          |
|        2026 | 2026-06      | SHOULDER      | Camera Deluxe                 | 91-180                |               152 |                              0 | 0.00%                      | 0.66%                    | €2,526.97          |
|        2026 | 2026-07      | PEAK          | Camera Deluxe                 | 8-14                  |                36 |                              0 | 0.00%                      | 0.00%                    | €2,746.91          |
|        2026 | 2026-07      | PEAK          | Camera Deluxe                 | 15-30                 |               194 |                              0 | 0.00%                      | 0.52%                    | €2,899.80          |
|        2026 | 2026-07      | PEAK          | Camera Deluxe                 | 31-60                 |               280 |                              1 | 0.36%                      | 0.36%                    | €3,105.67          |
|        2026 | 2026-07      | PEAK          | Camera Deluxe                 | 61-90                 |               227 |                              1 | 0.44%                      | 2.20%                    | €2,960.87          |
|        2026 | 2026-07      | PEAK          | Camera Deluxe                 | 91-180                |               430 |                              2 | 0.47%                      | 1.40%                    | €3,412.62          |
|        2026 | 2026-07      | PEAK          | Camera Deluxe                 | 181+                  |                35 |                              0 | 0.00%                      | 2.86%                    | €3,603.06          |
|        2024 | 2024-06      | SHOULDER      | Camera Superior               | 91-180                |                63 |                              0 | 0.00%                      | 1.59%                    | €1,592.28          |
|        2024 | 2024-07      | PEAK          | Camera Superior               | 8-14                  |                64 |                              8 | 12.50%                     | 17.19%                   | €2,262.89          |
|        2024 | 2024-07      | PEAK          | Camera Superior               | 15-30                 |                63 |                              0 | 0.00%                      | 1.59%                    | €2,358.19          |
|        2024 | 2024-07      | PEAK          | Camera Superior               | 31-60                 |                64 |                              1 | 1.56%                      | 1.56%                    | €2,729.50          |
|        2024 | 2024-07      | PEAK          | Camera Superior               | 61-90                 |                40 |                              0 | 0.00%                      | 0.00%                    | €2,337.08          |
|        2024 | 2024-07      | PEAK          | Camera Superior               | 91-180                |               108 |                              5 | 4.63%                      | 6.48%                    | €2,325.86          |
|        2024 | 2024-08      | PEAK          | Camera Superior               | 0-7                   |                45 |                              5 | 11.11%                     | 11.11%                   | €2,306.81          |
|        2024 | 2024-08      | PEAK          | Camera Superior               | 8-14                  |                41 |                              4 | 9.76%                      | 9.76%                    | €2,887.56          |
|        2024 | 2024-08      | PEAK          | Camera Superior               | 15-30                 |                98 |                              2 | 2.04%                      | 2.04%                    | €2,815.82          |
|        2024 | 2024-08      | PEAK          | Camera Superior               | 31-60                 |               100 |                              2 | 2.00%                      | 3.00%                    | €3,341.56          |
|        2024 | 2024-08      | PEAK          | Camera Superior               | 61-90                 |                88 |                              0 | 0.00%                      | 0.00%                    | €3,376.55          |
|        2024 | 2024-08      | PEAK          | Camera Superior               | 91-180                |               124 |                              1 | 0.81%                      | 0.81%                    | €3,436.63          |
|        2024 | 2024-08      | PEAK          | Camera Superior               | 181+                  |                74 |                              0 | 0.00%                      | 0.00%                    | €3,486.07          |
|        2024 | 2024-09      | SHOULDER      | Camera Superior               | 31-60                 |                37 |                              0 | 0.00%                      | 0.00%                    | €1,536.15          |
|        2024 | 2024-09      | SHOULDER      | Camera Superior               | 61-90                 |                50 |                              0 | 0.00%                      | 0.00%                    | €1,538.80          |
|        2024 | 2024-09      | SHOULDER      | Camera Superior               | 91-180                |                68 |                              1 | 1.47%                      | 1.47%                    | €1,559.19          |
|        2025 | 2025-06      | SHOULDER      | Camera Superior               | 15-30                 |                52 |                              0 | 0.00%                      | 1.92%                    | €1,257.19          |
|        2025 | 2025-06      | SHOULDER      | Camera Superior               | 31-60                 |               133 |                              3 | 2.26%                      | 4.51%                    | €1,378.50          |
|        2025 | 2025-06      | SHOULDER      | Camera Superior               | 61-90                 |                96 |                              1 | 1.04%                      | 3.12%                    | €1,694.24          |
|        2025 | 2025-06      | SHOULDER      | Camera Superior               | 91-180                |                51 |                              1 | 1.96%                      | 1.96%                    | €1,971.88          |
|        2025 | 2025-07      | PEAK          | Camera Superior               | 31-60                 |               112 |                              2 | 1.79%                      | 2.68%                    | €1,968.45          |
|        2025 | 2025-07      | PEAK          | Camera Superior               | 61-90                 |               101 |                              1 | 0.99%                      | 2.97%                    | €2,154.13          |
|        2025 | 2025-07      | PEAK          | Camera Superior               | 91-180                |               212 |                              1 | 0.47%                      | 0.94%                    | €2,280.72          |
|        2025 | 2025-08      | PEAK          | Camera Superior               | 15-30                 |                34 |                              1 | 2.94%                      | 5.88%                    | €1,254.19          |
|        2025 | 2025-08      | PEAK          | Camera Superior               | 31-60                 |               114 |                              2 | 1.75%                      | 2.63%                    | €2,244.00          |
|        2025 | 2025-08      | PEAK          | Camera Superior               | 61-90                 |                68 |                              1 | 1.47%                      | 2.94%                    | €2,131.19          |
|        2025 | 2025-08      | PEAK          | Camera Superior               | 91-180                |               316 |                              6 | 1.90%                      | 2.53%                    | €2,648.05          |
|        2025 | 2025-08      | PEAK          | Camera Superior               | 181+                  |                33 |                              0 | 0.00%                      | 0.00%                    | €2,813.26          |
|        2026 | 2026-06      | SHOULDER      | Camera Superior               | 15-30                 |                30 |                              1 | 3.33%                      | 6.67%                    | €1,126.03          |
|        2026 | 2026-06      | SHOULDER      | Camera Superior               | 31-60                 |                71 |                              4 | 5.63%                      | 8.45%                    | €1,309.35          |
|        2026 | 2026-06      | SHOULDER      | Camera Superior               | 61-90                 |                83 |                              1 | 1.20%                      | 3.61%                    | €1,562.16          |
|        2026 | 2026-06      | SHOULDER      | Camera Superior               | 91-180                |               119 |                              1 | 0.84%                      | 0.84%                    | €1,967.16          |
|        2026 | 2026-07      | PEAK          | Camera Superior               | 8-14                  |                33 |                              1 | 3.03%                      | 3.03%                    | €1,799.27          |
|        2026 | 2026-07      | PEAK          | Camera Superior               | 15-30                 |               190 |                              1 | 0.53%                      | 0.53%                    | €2,090.98          |
|        2026 | 2026-07      | PEAK          | Camera Superior               | 31-60                 |               114 |                              0 | 0.00%                      | 0.88%                    | €2,033.14          |
|        2026 | 2026-07      | PEAK          | Camera Superior               | 61-90                 |                84 |                              2 | 2.38%                      | 2.38%                    | €2,146.53          |
|        2026 | 2026-07      | PEAK          | Camera Superior               | 91-180                |               309 |                              6 | 1.94%                      | 4.21%                    | €2,599.59          |
|        2026 | 2026-07      | PEAK          | Camera Superior               | 181+                  |                38 |                              1 | 2.63%                      | 2.63%                    | €2,767.29          |
|        2026 | 2026-07      | PEAK          | Suite Familiare               | 91-180                |                50 |                              0 | 0.00%                      | 2.00%                    | €3,826.04          |
|        2025 | 2025-07      | PEAK          | Suite Familiare Vista Piscina | 31-60                 |                82 |                              0 | 0.00%                      | 0.00%                    | €2,872.45          |
|        2025 | 2025-07      | PEAK          | Suite Familiare Vista Piscina | 61-90                 |                39 |                              0 | 0.00%                      | 0.00%                    | €2,809.98          |
|        2026 | 2026-07      | PEAK          | Suite Familiare Vista Piscina | 91-180                |               162 |                              1 | 0.62%                      | 1.23%                    | €3,989.00          |
|        2026 | 2026-07      | PEAK          | Villino 2Ten                  | 31-60                 |                41 |                              0 | 0.00%                      | 2.44%                    | €1,656.68          |
|        2026 | 2026-07      | PEAK          | Villino Double                | 91-180                |                37 |                              1 | 2.70%                      | 2.70%                    | €3,004.12          |

This is the main demand-quality crossover: it shows whether the same room becomes more or less likely to convert at different stay periods and lead times. Only completed historical stay months are included here, so partial future 2026 periods are not treated as final.

### Conversion × year × season / month × booking window

|   stay_year | stay_month   | season_band   | booking_window_band   |   requests |   quoted_requests |   converted_requests | quote_rate_pct   | conversion_pct   |
|------------:|:-------------|:--------------|:----------------------|-----------:|------------------:|---------------------:|:-----------------|:-----------------|
|        2024 | 2024-06      | SHOULDER      | 0-7                   |        109 |                89 |                    6 | 81.65%           | 5.50%            |
|        2024 | 2024-06      | SHOULDER      | 8-14                  |        139 |               104 |                    6 | 74.82%           | 4.32%            |
|        2024 | 2024-06      | SHOULDER      | 15-30                 |        321 |               292 |                    5 | 90.97%           | 1.56%            |
|        2024 | 2024-06      | SHOULDER      | 31-60                 |        182 |               174 |                    9 | 95.63%           | 4.92%            |
|        2024 | 2024-06      | SHOULDER      | 61-90                 |        134 |               123 |                   14 | 91.85%           | 10.37%           |
|        2024 | 2024-06      | SHOULDER      | 91-180                |        310 |               295 |                   23 | 95.18%           | 7.40%            |
|        2024 | 2024-06      | SHOULDER      | 181+                  |         65 |                60 |                    7 | 92.31%           | 10.77%           |
|        2024 | 2024-07      | PEAK          | 0-7                   |        121 |                99 |                    5 | 81.82%           | 4.13%            |
|        2024 | 2024-07      | PEAK          | 8-14                  |        254 |               236 |                   21 | 92.94%           | 8.24%            |
|        2024 | 2024-07      | PEAK          | 15-30                 |        358 |               334 |                   10 | 93.30%           | 2.79%            |
|        2024 | 2024-07      | PEAK          | 31-60                 |        304 |               299 |                   10 | 98.36%           | 3.28%            |
|        2024 | 2024-07      | PEAK          | 61-90                 |        169 |               162 |                    6 | 95.86%           | 3.55%            |
|        2024 | 2024-07      | PEAK          | 91-180                |        430 |               416 |                   32 | 96.79%           | 7.34%            |
|        2024 | 2024-07      | PEAK          | 181+                  |        125 |               113 |                    7 | 90.40%           | 5.60%            |
|        2024 | 2024-08      | PEAK          | 0-7                   |        191 |               154 |                   19 | 80.83%           | 9.84%            |
|        2024 | 2024-08      | PEAK          | 8-14                  |        212 |               186 |                   10 | 87.74%           | 4.72%            |
|        2024 | 2024-08      | PEAK          | 15-30                 |        435 |               402 |                   12 | 92.41%           | 2.76%            |
|        2024 | 2024-08      | PEAK          | 31-60                 |        518 |               496 |                   17 | 95.75%           | 3.28%            |
|        2024 | 2024-08      | PEAK          | 61-90                 |        349 |               339 |                    1 | 97.13%           | 0.29%            |
|        2024 | 2024-08      | PEAK          | 91-180                |        625 |               609 |                   18 | 97.44%           | 2.88%            |
|        2024 | 2024-08      | PEAK          | 181+                  |        251 |               243 |                    5 | 96.81%           | 1.99%            |
|        2024 | 2024-09      | SHOULDER      | 0-7                   |         48 |                38 |                    7 | 79.17%           | 14.58%           |
|        2024 | 2024-09      | SHOULDER      | 8-14                  |        137 |               127 |                    4 | 92.70%           | 2.92%            |
|        2024 | 2024-09      | SHOULDER      | 15-30                 |        199 |               191 |                    7 | 95.98%           | 3.52%            |
|        2024 | 2024-09      | SHOULDER      | 31-60                 |        170 |               162 |                    7 | 95.29%           | 4.12%            |
|        2024 | 2024-09      | SHOULDER      | 61-90                 |        205 |               198 |                    3 | 96.59%           | 1.46%            |
|        2024 | 2024-09      | SHOULDER      | 91-180                |        325 |               320 |                    6 | 98.46%           | 1.85%            |
|        2024 | 2024-09      | SHOULDER      | 181+                  |         39 |                36 |                    2 | 92.31%           | 5.13%            |
|        2025 | 2025-05      | LOW           | 15-30                 |         90 |                80 |                   12 | 89.01%           | 13.19%           |
|        2025 | 2025-06      | SHOULDER      | 0-7                   |        158 |               118 |                   32 | 74.53%           | 19.88%           |
|        2025 | 2025-06      | SHOULDER      | 8-14                  |        172 |               147 |                   26 | 85.71%           | 14.86%           |
|        2025 | 2025-06      | SHOULDER      | 15-30                 |        329 |               319 |                   15 | 96.98%           | 4.53%            |
|        2025 | 2025-06      | SHOULDER      | 31-60                 |        563 |               548 |                   16 | 97.34%           | 2.84%            |
|        2025 | 2025-06      | SHOULDER      | 61-90                 |        293 |               291 |                   10 | 99.32%           | 3.41%            |
|        2025 | 2025-06      | SHOULDER      | 91-180                |        203 |               201 |                    6 | 99.01%           | 2.96%            |
|        2025 | 2025-07      | PEAK          | 0-7                   |        194 |               151 |                   14 | 77.84%           | 7.22%            |
|        2025 | 2025-07      | PEAK          | 8-14                  |        252 |               210 |                   16 | 83.33%           | 6.35%            |
|        2025 | 2025-07      | PEAK          | 15-30                 |        465 |               433 |                   24 | 93.13%           | 5.15%            |
|        2025 | 2025-07      | PEAK          | 31-60                 |        583 |               557 |                   19 | 95.06%           | 3.24%            |
|        2025 | 2025-07      | PEAK          | 61-90                 |        385 |               379 |                    6 | 98.44%           | 1.56%            |
|        2025 | 2025-07      | PEAK          | 91-180                |        749 |               745 |                   16 | 99.47%           | 2.13%            |
|        2025 | 2025-07      | PEAK          | 181+                  |         51 |                45 |                    2 | 88.24%           | 3.92%            |
|        2025 | 2025-08      | PEAK          | 0-7                   |        384 |               165 |                   23 | 42.97%           | 5.99%            |
|        2025 | 2025-08      | PEAK          | 8-14                  |        340 |               177 |                   16 | 52.06%           | 4.71%            |
|        2025 | 2025-08      | PEAK          | 15-30                 |        732 |               381 |                   18 | 52.05%           | 2.46%            |
|        2025 | 2025-08      | PEAK          | 31-60                 |        898 |               648 |                   17 | 72.06%           | 1.88%            |
|        2025 | 2025-08      | PEAK          | 61-90                 |        706 |               666 |                   13 | 94.33%           | 1.84%            |
|        2025 | 2025-08      | PEAK          | 91-180                |       1339 |              1324 |                   25 | 98.73%           | 1.86%            |
|        2025 | 2025-08      | PEAK          | 181+                  |         88 |                82 |                    1 | 93.18%           | 1.14%            |
|        2025 | 2025-09      | SHOULDER      | 0-7                   |        182 |                96 |                   36 | 53.48%           | 19.25%           |
|        2025 | 2025-09      | SHOULDER      | 8-14                  |        133 |               108 |                   14 | 81.20%           | 10.53%           |
|        2025 | 2025-09      | SHOULDER      | 15-30                 |        131 |               116 |                    5 | 88.55%           | 3.82%            |
|        2025 | 2025-09      | SHOULDER      | 31-60                 |        146 |               141 |                   11 | 96.64%           | 7.38%            |
|        2025 | 2025-09      | SHOULDER      | 61-90                 |         84 |                80 |                    5 | 95.24%           | 5.95%            |
|        2025 | 2025-09      | SHOULDER      | 91-180                |        108 |               102 |                    1 | 94.44%           | 0.93%            |
|        2026 | 2026-05      | LOW           | 0-7                   |         79 |                38 |                    3 | 48.10%           | 3.80%            |
|        2026 | 2026-05      | LOW           | 15-30                 |         45 |                25 |                    1 | 55.56%           | 2.22%            |
|        2026 | 2026-05      | LOW           | 31-60                 |         49 |                22 |                    2 | 46.00%           | 4.00%            |
|        2026 | 2026-05      | LOW           | 91-180                |         46 |                24 |                    3 | 53.19%           | 6.38%            |
|        2026 | 2026-06      | SHOULDER      | 0-7                   |        158 |                91 |                    7 | 57.59%           | 4.43%            |
|        2026 | 2026-06      | SHOULDER      | 8-14                  |        120 |                80 |                    7 | 65.57%           | 5.74%            |
|        2026 | 2026-06      | SHOULDER      | 15-30                 |        287 |               201 |                   20 | 69.52%           | 6.85%            |
|        2026 | 2026-06      | SHOULDER      | 31-60                 |        335 |               254 |                   15 | 75.67%           | 4.45%            |
|        2026 | 2026-06      | SHOULDER      | 61-90                 |        329 |               280 |                    8 | 85.11%           | 2.43%            |
|        2026 | 2026-06      | SHOULDER      | 91-180                |        666 |               426 |                    9 | 63.96%           | 1.35%            |
|        2026 | 2026-06      | SHOULDER      | 181+                  |         84 |                55 |                    2 | 65.48%           | 2.38%            |
|        2026 | 2026-07      | PEAK          | 0-7                   |        223 |               152 |                    3 | 68.16%           | 1.35%            |
|        2026 | 2026-07      | PEAK          | 8-14                  |        258 |               186 |                    4 | 72.09%           | 1.55%            |
|        2026 | 2026-07      | PEAK          | 15-30                 |        595 |               455 |                    3 | 76.47%           | 0.50%            |
|        2026 | 2026-07      | PEAK          | 31-60                 |        802 |               591 |                    5 | 73.69%           | 0.62%            |
|        2026 | 2026-07      | PEAK          | 61-90                 |        551 |               482 |                   17 | 87.48%           | 3.09%            |
|        2026 | 2026-07      | PEAK          | 91-180                |       1389 |              1111 |                   33 | 80.04%           | 2.37%            |
|        2026 | 2026-07      | PEAK          | 181+                  |        212 |               137 |                    4 | 64.62%           | 1.89%            |

### Treatment × year × season / month

|   stay_year | stay_month   | season_band   | arrangement_name   |   confirmed_bookings |   avg_booking_window | avg_adr   | revenue     | revenue_per_booking   | cancellation_rate_pct   | reliability   |
|------------:|:-------------|:--------------|:-------------------|---------------------:|---------------------:|:----------|:------------|:----------------------|:------------------------|:--------------|
|        2025 | 2025-06      | SHOULDER      | Bed & Breakfast    |                   89 |                28.71 | €102.79   | €32,940.09  | €370.11               | 18.35%                  | MEDIUM        |
|        2025 | 2025-07      | PEAK          | Bed & Breakfast    |                   73 |                46.68 | €155.08   | €58,590.70  | €802.61               | 28.43%                  | MEDIUM        |
|        2025 | 2025-08      | PEAK          | Bed & Breakfast    |                   69 |                60.42 | €167.64   | €59,031.89  | €855.53               | 25.00%                  | MEDIUM        |
|        2025 | 2025-09      | SHOULDER      | Bed & Breakfast    |                   35 |                12.83 | €110.61   | €12,733.71  | €363.82               | 32.69%                  | MEDIUM        |
|        2024 | 2024-06      | SHOULDER      | Mezza Pensione     |                  143 |                73.92 | €155.63   | €148,882.70 | €1,041.14             | 17.71%                  | HIGH          |
|        2024 | 2024-07      | PEAK          | Mezza Pensione     |                   69 |                68.77 | €260.75   | €126,309.05 | €1,830.57             | 10.13%                  | MEDIUM        |
|        2024 | 2024-08      | PEAK          | Mezza Pensione     |                   74 |                64.74 | €343.12   | €187,228.50 | €2,530.11             | 14.44%                  | MEDIUM        |
|        2024 | 2024-09      | SHOULDER      | Mezza Pensione     |                   74 |                63.16 | €144.93   | €65,809.85  | €889.32               | 13.95%                  | MEDIUM        |
|        2025 | 2025-06      | SHOULDER      | Mezza Pensione     |                  145 |                35.78 | €171.77   | €130,649.50 | €901.03               | 18.08%                  | HIGH          |
|        2025 | 2025-07      | PEAK          | Mezza Pensione     |                  156 |                53.07 | €225.62   | €217,181.59 | €1,392.19             | 24.27%                  | HIGH          |
|        2025 | 2025-08      | PEAK          | Mezza Pensione     |                  157 |                70.4  | €252.85   | €266,529.52 | €1,697.64             | 23.41%                  | HIGH          |
|        2025 | 2025-09      | SHOULDER      | Mezza Pensione     |                  105 |                15.68 | €183.19   | €71,057.06  | €676.73               | 17.97%                  | HIGH          |
|        2026 | 2026-05      | LOW           | Mezza Pensione     |                   48 |                14.94 | €162.44   | €18,767.03  | €390.98               | 11.11%                  | MEDIUM        |
|        2026 | 2026-06      | SHOULDER      | Mezza Pensione     |                  182 |                38.71 | €175.11   | €187,431.96 | €1,029.85             | 19.47%                  | HIGH          |
|        2026 | 2026-07      | PEAK          | Mezza Pensione     |                  152 |                56.05 | €261.87   | €250,311.12 | €1,646.78             | 18.72%                  | HIGH          |
|        2025 | 2025-07      | PEAK          | Only Bed           |                   36 |               119    | €69.01    | €20,812.98  | €578.14               | 10.00%                  | MEDIUM        |
|        2025 | 2025-08      | PEAK          | Only Bed           |                   54 |               139.06 | €92.27    | €49,291.35  | €912.80               | 8.47%                   | MEDIUM        |
|        2024 | 2024-06      | SHOULDER      | Pensione Completa  |                  194 |                72.61 | €137.82   | €187,920.80 | €968.66               | 14.10%                  | HIGH          |
|        2024 | 2024-07      | PEAK          | Pensione Completa  |                  188 |                72.69 | €216.11   | €294,901.50 | €1,568.62             | 18.45%                  | HIGH          |
|        2024 | 2024-08      | PEAK          | Pensione Completa  |                  189 |                65.63 | €214.33   | €309,949.00 | €1,639.94             | 24.51%                  | HIGH          |
|        2024 | 2024-09      | SHOULDER      | Pensione Completa  |                   71 |                57.2  | €163.16   | €70,898.00  | €998.56               | 22.45%                  | MEDIUM        |
|        2025 | 2025-05      | LOW           | Pensione Completa  |                   30 |                24.93 | €191.58   | €11,974.35  | €399.15               | 11.76%                  | MEDIUM        |
|        2025 | 2025-06      | SHOULDER      | Pensione Completa  |                   82 |                55.87 | €202.72   | €84,593.88  | €1,031.63             | 29.91%                  | MEDIUM        |
|        2025 | 2025-07      | PEAK          | Pensione Completa  |                  107 |                53.45 | €184.73   | €126,450.58 | €1,181.78             | 33.12%                  | HIGH          |
|        2025 | 2025-08      | PEAK          | Pensione Completa  |                   83 |                57.39 | €219.48   | €120,109.09 | €1,447.10             | 44.30%                  | MEDIUM        |
|        2025 | 2025-09      | SHOULDER      | Pensione Completa  |                   36 |                16.56 | €150.23   | €20,645.50  | €573.49               | 23.40%                  | MEDIUM        |
|        2026 | 2026-05      | LOW           | Pensione Completa  |                   98 |                26.98 | €149.76   | €44,015.75  | €449.14               | 8.41%                   | MEDIUM        |
|        2026 | 2026-06      | SHOULDER      | Pensione Completa  |                   75 |                35.69 | €179.76   | €79,074.03  | €1,054.32             | 15.73%                  | MEDIUM        |
|        2026 | 2026-07      | PEAK          | Pensione Completa  |                   57 |                55.91 | €271.42   | €99,528.08  | €1,746.11             | 18.92%                  | MEDIUM        |

### Treatment × year × season / month × booking window

|   stay_year | stay_month   | season_band   | arrangement_name   | booking_window_band   |   confirmed_bookings | avg_adr   | revenue     |   avg_los | reliability   |
|------------:|:-------------|:--------------|:-------------------|:----------------------|---------------------:|:----------|:------------|----------:|:--------------|
|        2025 | 2025-06      | SHOULDER      | Bed & Breakfast    | 0-7                   |                   28 | €98.87    | €5,774.85   |      2.25 | LOW           |
|        2025 | 2025-06      | SHOULDER      | Bed & Breakfast    | 8-14                  |                   13 | €110.76   | €4,496.06   |      3.08 | LOW           |
|        2025 | 2025-06      | SHOULDER      | Bed & Breakfast    | 15-30                 |                   18 | €108.60   | €5,861.82   |      2.94 | LOW           |
|        2025 | 2025-06      | SHOULDER      | Bed & Breakfast    | 31-60                 |                   16 | €74.43    | €5,717.91   |      3.56 | LOW           |
|        2025 | 2025-07      | PEAK          | Bed & Breakfast    | 0-7                   |                   17 | €138.94   | €5,847.95   |      2.35 | LOW           |
|        2025 | 2025-07      | PEAK          | Bed & Breakfast    | 15-30                 |                   13 | €189.96   | €13,321.34  |      5.38 | LOW           |
|        2025 | 2025-07      | PEAK          | Bed & Breakfast    | 31-60                 |                   12 | €178.97   | €12,973.55  |      6    | LOW           |
|        2025 | 2025-07      | PEAK          | Bed & Breakfast    | 91-180                |                   16 | €127.09   | €13,468.81  |      7    | LOW           |
|        2025 | 2025-08      | PEAK          | Bed & Breakfast    | 0-7                   |                   18 | €179.48   | €11,108.87  |      3.56 | LOW           |
|        2025 | 2025-08      | PEAK          | Bed & Breakfast    | 15-30                 |                   13 | €145.73   | €7,540.75   |      4.08 | LOW           |
|        2025 | 2025-08      | PEAK          | Bed & Breakfast    | 91-180                |                   22 | €140.92   | €21,424.10  |      6.73 | LOW           |
|        2025 | 2025-09      | SHOULDER      | Bed & Breakfast    | 0-7                   |                   22 | €110.21   | €6,544.01   |      2.64 | LOW           |
|        2024 | 2024-06      | SHOULDER      | Mezza Pensione     | 8-14                  |                   11 | €183.91   | €12,757.10  |      5.64 | LOW           |
|        2024 | 2024-06      | SHOULDER      | Mezza Pensione     | 31-60                 |                   13 | €239.66   | €22,267.00  |      7.69 | LOW           |
|        2024 | 2024-06      | SHOULDER      | Mezza Pensione     | 61-90                 |                   73 | €110.41   | €47,520.60  |      5.88 | MEDIUM        |
|        2024 | 2024-06      | SHOULDER      | Mezza Pensione     | 91-180                |                   29 | €217.40   | €45,851.00  |      7.34 | LOW           |
|        2024 | 2024-07      | PEAK          | Mezza Pensione     | 0-7                   |                   10 | €253.92   | €14,284.55  |      4.9  | LOW           |
|        2024 | 2024-07      | PEAK          | Mezza Pensione     | 8-14                  |                   11 | €376.03   | €19,338.00  |      5    | LOW           |
|        2024 | 2024-07      | PEAK          | Mezza Pensione     | 61-90                 |                   11 | €259.28   | €23,228.00  |      7.73 | LOW           |
|        2024 | 2024-07      | PEAK          | Mezza Pensione     | 91-180                |                   26 | €182.05   | €40,533.50  |      8.77 | LOW           |
|        2024 | 2024-08      | PEAK          | Mezza Pensione     | 0-7                   |                   22 | €287.01   | €37,713.00  |      5.45 | LOW           |
|        2024 | 2024-08      | PEAK          | Mezza Pensione     | 31-60                 |                   12 | €422.94   | €38,972.00  |      7.67 | LOW           |
|        2024 | 2024-08      | PEAK          | Mezza Pensione     | 91-180                |                   23 | €294.38   | €56,246.00  |      8.52 | LOW           |
|        2024 | 2024-09      | SHOULDER      | Mezza Pensione     | 0-7                   |                   30 | €134.54   | €19,113.35  |      4.73 | MEDIUM        |
|        2024 | 2024-09      | SHOULDER      | Mezza Pensione     | 91-180                |                   20 | €128.16   | €18,348.00  |      7.05 | LOW           |
|        2025 | 2025-06      | SHOULDER      | Mezza Pensione     | 0-7                   |                   43 | €154.92   | €21,986.83  |      3.23 | MEDIUM        |
|        2025 | 2025-06      | SHOULDER      | Mezza Pensione     | 8-14                  |                   27 | €148.78   | €18,944.20  |      4.22 | LOW           |
|        2025 | 2025-06      | SHOULDER      | Mezza Pensione     | 15-30                 |                   25 | €197.79   | €21,689.30  |      4.52 | LOW           |
|        2025 | 2025-06      | SHOULDER      | Mezza Pensione     | 31-60                 |                   25 | €191.87   | €30,567.43  |      6.28 | LOW           |
|        2025 | 2025-06      | SHOULDER      | Mezza Pensione     | 91-180                |                   13 | €167.47   | €15,846.69  |      7.54 | LOW           |
|        2025 | 2025-07      | PEAK          | Mezza Pensione     | 0-7                   |                   30 | €217.23   | €28,634.06  |      4.27 | MEDIUM        |
|        2025 | 2025-07      | PEAK          | Mezza Pensione     | 8-14                  |                   20 | €259.24   | €25,151.63  |      4.7  | LOW           |
|        2025 | 2025-07      | PEAK          | Mezza Pensione     | 15-30                 |                   23 | €234.76   | €32,468.19  |      5.61 | LOW           |
|        2025 | 2025-07      | PEAK          | Mezza Pensione     | 31-60                 |                   25 | €227.09   | €39,089.07  |      6.76 | LOW           |
|        2025 | 2025-07      | PEAK          | Mezza Pensione     | 61-90                 |                   18 | €228.21   | €27,806.65  |      6.5  | LOW           |
|        2025 | 2025-07      | PEAK          | Mezza Pensione     | 91-180                |                   39 | €206.13   | €60,241.99  |      7.18 | MEDIUM        |
|        2025 | 2025-08      | PEAK          | Mezza Pensione     | 0-7                   |                   22 | €225.24   | €24,674.58  |      4.55 | LOW           |
|        2025 | 2025-08      | PEAK          | Mezza Pensione     | 8-14                  |                   19 | €244.26   | €21,668.25  |      4.42 | LOW           |
|        2025 | 2025-08      | PEAK          | Mezza Pensione     | 15-30                 |                   15 | €237.32   | €17,478.08  |      4.87 | LOW           |
|        2025 | 2025-08      | PEAK          | Mezza Pensione     | 31-60                 |                   22 | €286.57   | €39,120.10  |      6.36 | LOW           |
|        2025 | 2025-08      | PEAK          | Mezza Pensione     | 61-90                 |                   22 | €306.87   | €53,443.11  |      7.55 | LOW           |
|        2025 | 2025-08      | PEAK          | Mezza Pensione     | 91-180                |                   57 | €236.61   | €110,145.40 |      8.32 | MEDIUM        |
|        2025 | 2025-09      | SHOULDER      | Mezza Pensione     | 0-7                   |                   61 | €181.82   | €33,926.48  |      3.05 | MEDIUM        |
|        2025 | 2025-09      | SHOULDER      | Mezza Pensione     | 8-14                  |                   17 | €189.92   | €14,899.84  |      4.82 | LOW           |
|        2025 | 2025-09      | SHOULDER      | Mezza Pensione     | 15-30                 |                   17 | €181.57   | €11,574.23  |      3.59 | LOW           |
|        2026 | 2026-05      | LOW           | Mezza Pensione     | 0-7                   |                   20 | €173.72   | €7,707.48   |      2.2  | LOW           |
|        2026 | 2026-05      | LOW           | Mezza Pensione     | 8-14                  |                   13 | €157.99   | €4,107.64   |      2    | LOW           |
|        2026 | 2026-05      | LOW           | Mezza Pensione     | 15-30                 |                   11 | €143.88   | €3,280.61   |      2.09 | LOW           |
|        2026 | 2026-06      | SHOULDER      | Mezza Pensione     | 0-7                   |                   41 | €149.26   | €16,279.00  |      2.76 | MEDIUM        |
|        2026 | 2026-06      | SHOULDER      | Mezza Pensione     | 8-14                  |                   21 | €160.50   | €11,012.94  |      3.48 | LOW           |
|        2026 | 2026-06      | SHOULDER      | Mezza Pensione     | 15-30                 |                   39 | €183.28   | €38,729.13  |      5.21 | MEDIUM        |
|        2026 | 2026-06      | SHOULDER      | Mezza Pensione     | 31-60                 |                   39 | €172.89   | €46,818.43  |      6.82 | MEDIUM        |
|        2026 | 2026-06      | SHOULDER      | Mezza Pensione     | 61-90                 |                   19 | €191.00   | €30,456.10  |      8.26 | LOW           |
|        2026 | 2026-06      | SHOULDER      | Mezza Pensione     | 91-180                |                   20 | €207.09   | €34,196.36  |      8.25 | LOW           |
|        2026 | 2026-07      | PEAK          | Mezza Pensione     | 0-7                   |                   32 | €277.31   | €37,504.04  |      3.72 | MEDIUM        |
|        2026 | 2026-07      | PEAK          | Mezza Pensione     | 8-14                  |                   13 | €244.19   | €13,864.72  |      4.08 | LOW           |
|        2026 | 2026-07      | PEAK          | Mezza Pensione     | 15-30                 |                   21 | €284.94   | €30,030.00  |      4.9  | LOW           |
|        2026 | 2026-07      | PEAK          | Mezza Pensione     | 31-60                 |                   21 | €249.47   | €36,853.11  |      7    | LOW           |
|        2026 | 2026-07      | PEAK          | Mezza Pensione     | 61-90                 |                   34 | €257.36   | €66,692.49  |      7.59 | MEDIUM        |
|        2026 | 2026-07      | PEAK          | Mezza Pensione     | 91-180                |                   26 | €247.63   | €52,592.27  |      8.04 | LOW           |
|        2025 | 2025-07      | PEAK          | Only Bed           | 91-180                |                   32 | €69.85    | €20,031.98  |      9.62 | MEDIUM        |
|        2025 | 2025-08      | PEAK          | Only Bed           | 91-180                |                   49 | €86.82    | €43,801.70  |      9.18 | MEDIUM        |
|        2024 | 2024-06      | SHOULDER      | Pensione Completa  | 0-7                   |                   21 | €119.12   | €13,694.00  |      4.95 | LOW           |
|        2024 | 2024-06      | SHOULDER      | Pensione Completa  | 8-14                  |                   14 | €87.83    | €4,732.00   |      2.86 | LOW           |
|        2024 | 2024-06      | SHOULDER      | Pensione Completa  | 15-30                 |                   25 | €110.68   | €14,849.50  |      5    | LOW           |
|        2024 | 2024-06      | SHOULDER      | Pensione Completa  | 31-60                 |                   22 | €108.76   | €14,573.90  |      5.77 | LOW           |
|        2024 | 2024-06      | SHOULDER      | Pensione Completa  | 61-90                 |                   50 | €111.82   | €41,845.50  |      7.2  | MEDIUM        |
|        2024 | 2024-06      | SHOULDER      | Pensione Completa  | 91-180                |                   54 | €194.58   | €83,828.40  |      7.78 | MEDIUM        |
|        2024 | 2024-07      | PEAK          | Pensione Completa  | 0-7                   |                   29 | €192.58   | €29,834.50  |      5    | LOW           |
|        2024 | 2024-07      | PEAK          | Pensione Completa  | 8-14                  |                   30 | €258.26   | €55,703.00  |      6.33 | MEDIUM        |
|        2024 | 2024-07      | PEAK          | Pensione Completa  | 31-60                 |                   16 | €257.35   | €29,996.00  |      7.38 | LOW           |
|        2024 | 2024-07      | PEAK          | Pensione Completa  | 61-90                 |                   21 | €170.44   | €25,041.00  |      6.76 | LOW           |
|        2024 | 2024-07      | PEAK          | Pensione Completa  | 91-180                |                   78 | €192.90   | €119,839.50 |      7.53 | MEDIUM        |
|        2024 | 2024-08      | PEAK          | Pensione Completa  | 0-7                   |                   46 | €220.65   | €67,042.50  |      5.74 | MEDIUM        |
|        2024 | 2024-08      | PEAK          | Pensione Completa  | 8-14                  |                   23 | €291.49   | €48,904.50  |      6.35 | LOW           |
|        2024 | 2024-08      | PEAK          | Pensione Completa  | 15-30                 |                   16 | €343.59   | €39,128.00  |      6.88 | LOW           |
|        2024 | 2024-08      | PEAK          | Pensione Completa  | 31-60                 |                   20 | €299.91   | €43,103.00  |      7.15 | LOW           |
|        2024 | 2024-08      | PEAK          | Pensione Completa  | 91-180                |                   75 | €117.92   | €82,244.50  |      7.97 | MEDIUM        |
|        2024 | 2024-09      | SHOULDER      | Pensione Completa  | 0-7                   |                   15 | €171.49   | €10,882.00  |      3.67 | LOW           |
|        2024 | 2024-09      | SHOULDER      | Pensione Completa  | 8-14                  |                   10 | €139.79   | €8,752.00   |      5.7  | LOW           |
|        2024 | 2024-09      | SHOULDER      | Pensione Completa  | 31-60                 |                   15 | €130.77   | €13,866.00  |      4.93 | LOW           |
|        2024 | 2024-09      | SHOULDER      | Pensione Completa  | 91-180                |                   16 | €129.58   | €13,462.50  |      6.69 | LOW           |
|        2025 | 2025-05      | LOW           | Pensione Completa  | 15-30                 |                   24 | €220.09   | €11,044.35  |      2.12 | LOW           |
|        2025 | 2025-06      | SHOULDER      | Pensione Completa  | 0-7                   |                   15 | €168.01   | €8,345.63   |      3.6  | LOW           |
|        2025 | 2025-06      | SHOULDER      | Pensione Completa  | 8-14                  |                   13 | €167.59   | €9,677.32   |      4.15 | LOW           |
|        2025 | 2025-06      | SHOULDER      | Pensione Completa  | 15-30                 |                   13 | €226.43   | €11,976.62  |      3.77 | LOW           |
|        2025 | 2025-06      | SHOULDER      | Pensione Completa  | 31-60                 |                   20 | €220.97   | €21,876.08  |      4.85 | LOW           |
|        2025 | 2025-06      | SHOULDER      | Pensione Completa  | 181+                  |                   10 | €185.96   | €13,067.50  |      6.9  | LOW           |
|        2025 | 2025-07      | PEAK          | Pensione Completa  | 0-7                   |                   34 | €111.05   | €10,100.16  |      2.53 | MEDIUM        |
|        2025 | 2025-07      | PEAK          | Pensione Completa  | 8-14                  |                   15 | €159.91   | €16,612.70  |      4.87 | LOW           |
|        2025 | 2025-07      | PEAK          | Pensione Completa  | 15-30                 |                   13 | €260.69   | €20,180.21  |      4.69 | LOW           |
|        2025 | 2025-07      | PEAK          | Pensione Completa  | 61-90                 |                   16 | €218.30   | €22,915.50  |      7.56 | LOW           |
|        2025 | 2025-07      | PEAK          | Pensione Completa  | 91-180                |                   16 | €223.55   | €33,171.08  |      9.06 | LOW           |
|        2025 | 2025-08      | PEAK          | Pensione Completa  | 0-7                   |                   23 | €146.15   | €18,128.15  |      4.04 | LOW           |
|        2025 | 2025-08      | PEAK          | Pensione Completa  | 8-14                  |                   11 | €270.52   | €16,791.30  |      4.91 | LOW           |
|        2025 | 2025-08      | PEAK          | Pensione Completa  | 15-30                 |                   11 | €180.90   | €8,640.50   |      3.36 | LOW           |
|        2025 | 2025-08      | PEAK          | Pensione Completa  | 31-60                 |                   11 | €248.50   | €19,097.95  |      6.09 | LOW           |
|        2025 | 2025-08      | PEAK          | Pensione Completa  | 61-90                 |                   10 | €269.42   | €22,017.35  |      7.6  | LOW           |
|        2025 | 2025-09      | SHOULDER      | Pensione Completa  | 0-7                   |                   21 | €110.81   | €9,039.93   |      2.71 | LOW           |
|        2026 | 2026-05      | LOW           | Pensione Completa  | 0-7                   |                   12 | €145.44   | €3,490.58   |      1.83 | LOW           |
|        2026 | 2026-05      | LOW           | Pensione Completa  | 15-30                 |                   47 | €179.08   | €26,855.03  |      3.02 | MEDIUM        |
|        2026 | 2026-05      | LOW           | Pensione Completa  | 31-60                 |                   36 | €110.98   | €12,631.64  |      3.11 | MEDIUM        |
|        2026 | 2026-06      | SHOULDER      | Pensione Completa  | 0-7                   |                   22 | €89.86    | €7,545.86   |      3.23 | LOW           |
|        2026 | 2026-06      | SHOULDER      | Pensione Completa  | 15-30                 |                   20 | €193.02   | €17,568.16  |      4.5  | LOW           |
|        2026 | 2026-06      | SHOULDER      | Pensione Completa  | 31-60                 |                   14 | €214.11   | €21,776.07  |      7.07 | LOW           |
|        2026 | 2026-07      | PEAK          | Pensione Completa  | 31-60                 |                   18 | €296.99   | €31,251.67  |      5.67 | LOW           |
|        2026 | 2026-07      | PEAK          | Pensione Completa  | 61-90                 |                   15 | €318.96   | €32,561.25  |      6.8  | LOW           |

### Conversion × treatment × year × season / month × booking window

|   stay_year | stay_month   | season_band   | arrangement_name   | booking_window_band   |   quoted_requests |   same_treatment_converted_requests | same_treatment_conversion_pct   | overall_conversion_pct   | avg_quote_amount   |
|------------:|:-------------|:--------------|:-------------------|:----------------------|------------------:|------------------------------------:|:--------------------------------|:-------------------------|:-------------------|
|        2025 | 2025-06      | SHOULDER      | Bed & Breakfast    | 8-14                  |                31 |                                   3 | 9.68%                           | 16.13%                   | €628.66            |
|        2025 | 2025-06      | SHOULDER      | Bed & Breakfast    | 15-30                 |                42 |                                   2 | 4.76%                           | 7.14%                    | €773.96            |
|        2025 | 2025-06      | SHOULDER      | Bed & Breakfast    | 31-60                 |                51 |                                   1 | 1.96%                           | 3.92%                    | €955.91            |
|        2025 | 2025-06      | SHOULDER      | Bed & Breakfast    | 61-90                 |                46 |                                   1 | 2.17%                           | 4.35%                    | €1,157.47          |
|        2025 | 2025-07      | PEAK          | Bed & Breakfast    | 0-7                   |                31 |                                   1 | 3.23%                           | 6.45%                    | €1,096.42          |
|        2025 | 2025-07      | PEAK          | Bed & Breakfast    | 8-14                  |                36 |                                   2 | 5.56%                           | 8.33%                    | €1,070.90          |
|        2025 | 2025-07      | PEAK          | Bed & Breakfast    | 15-30                 |                71 |                                   2 | 2.82%                           | 2.82%                    | €1,479.81          |
|        2025 | 2025-07      | PEAK          | Bed & Breakfast    | 31-60                 |                65 |                                   1 | 1.54%                           | 4.62%                    | €1,602.19          |
|        2025 | 2025-07      | PEAK          | Bed & Breakfast    | 61-90                 |                39 |                                   0 | 0.00%                           | 0.00%                    | €1,724.58          |
|        2025 | 2025-07      | PEAK          | Bed & Breakfast    | 91-180                |                84 |                                   1 | 1.19%                           | 2.38%                    | €1,741.37          |
|        2025 | 2025-08      | PEAK          | Bed & Breakfast    | 0-7                   |                38 |                                   7 | 18.42%                          | 18.42%                   | €722.23            |
|        2025 | 2025-08      | PEAK          | Bed & Breakfast    | 8-14                  |                36 |                                   3 | 8.33%                           | 16.67%                   | €973.29            |
|        2025 | 2025-08      | PEAK          | Bed & Breakfast    | 15-30                 |                57 |                                   4 | 7.02%                           | 8.77%                    | €1,219.62          |
|        2025 | 2025-08      | PEAK          | Bed & Breakfast    | 31-60                 |                92 |                                   1 | 1.09%                           | 2.17%                    | €1,792.47          |
|        2025 | 2025-08      | PEAK          | Bed & Breakfast    | 61-90                 |                71 |                                   2 | 2.82%                           | 2.82%                    | €2,208.34          |
|        2025 | 2025-08      | PEAK          | Bed & Breakfast    | 91-180                |               160 |                                   0 | 0.00%                           | 1.25%                    | €2,256.70          |
|        2025 | 2025-09      | SHOULDER      | Bed & Breakfast    | 15-30                 |                30 |                                   1 | 3.33%                           | 3.33%                    | €532.25            |
|        2024 | 2024-06      | SHOULDER      | Mezza Pensione     | 0-7                   |                68 |                                   3 | 4.41%                           | 4.41%                    | €1,120.66          |
|        2024 | 2024-06      | SHOULDER      | Mezza Pensione     | 8-14                  |                65 |                                   5 | 7.69%                           | 9.23%                    | €1,532.45          |
|        2024 | 2024-06      | SHOULDER      | Mezza Pensione     | 15-30                 |               204 |                                   2 | 0.98%                           | 0.98%                    | €1,680.69          |
|        2024 | 2024-06      | SHOULDER      | Mezza Pensione     | 31-60                 |               106 |                                   5 | 4.72%                           | 5.66%                    | €2,005.74          |
|        2024 | 2024-06      | SHOULDER      | Mezza Pensione     | 61-90                 |                58 |                                   4 | 6.90%                           | 8.62%                    | €1,809.84          |
|        2024 | 2024-06      | SHOULDER      | Mezza Pensione     | 91-180                |               148 |                                  11 | 7.43%                           | 8.11%                    | €1,620.74          |
|        2024 | 2024-06      | SHOULDER      | Mezza Pensione     | 181+                  |                32 |                                   1 | 3.12%                           | 6.25%                    | €1,622.75          |
|        2024 | 2024-07      | PEAK          | Mezza Pensione     | 0-7                   |                60 |                                   1 | 1.67%                           | 1.67%                    | €2,074.77          |
|        2024 | 2024-07      | PEAK          | Mezza Pensione     | 8-14                  |               129 |                                   7 | 5.43%                           | 8.53%                    | €2,251.39          |
|        2024 | 2024-07      | PEAK          | Mezza Pensione     | 15-30                 |               202 |                                   2 | 0.99%                           | 1.98%                    | €2,494.49          |
|        2024 | 2024-07      | PEAK          | Mezza Pensione     | 31-60                 |               142 |                                   3 | 2.11%                           | 2.82%                    | €2,848.51          |
|        2024 | 2024-07      | PEAK          | Mezza Pensione     | 61-90                 |                66 |                                   1 | 1.52%                           | 1.52%                    | €2,740.45          |
|        2024 | 2024-07      | PEAK          | Mezza Pensione     | 91-180                |               193 |                                   6 | 3.11%                           | 5.70%                    | €2,605.81          |
|        2024 | 2024-07      | PEAK          | Mezza Pensione     | 181+                  |                40 |                                   0 | 0.00%                           | 0.00%                    | €2,771.66          |
|        2024 | 2024-08      | PEAK          | Mezza Pensione     | 0-7                   |                86 |                                   9 | 10.47%                          | 11.63%                   | €2,190.36          |
|        2024 | 2024-08      | PEAK          | Mezza Pensione     | 8-14                  |               108 |                                   0 | 0.00%                           | 1.85%                    | €2,715.32          |
|        2024 | 2024-08      | PEAK          | Mezza Pensione     | 15-30                 |               247 |                                   2 | 0.81%                           | 1.62%                    | €2,980.20          |
|        2024 | 2024-08      | PEAK          | Mezza Pensione     | 31-60                 |               294 |                                   8 | 2.72%                           | 3.74%                    | €3,470.92          |
|        2024 | 2024-08      | PEAK          | Mezza Pensione     | 61-90                 |               180 |                                   0 | 0.00%                           | 0.56%                    | €3,579.11          |
|        2024 | 2024-08      | PEAK          | Mezza Pensione     | 91-180                |               334 |                                   7 | 2.10%                           | 2.10%                    | €3,812.85          |
|        2024 | 2024-08      | PEAK          | Mezza Pensione     | 181+                  |               117 |                                   3 | 2.56%                           | 3.42%                    | €3,717.07          |
|        2024 | 2024-09      | SHOULDER      | Mezza Pensione     | 8-14                  |                76 |                                   2 | 2.63%                           | 2.63%                    | €1,350.79          |
|        2024 | 2024-09      | SHOULDER      | Mezza Pensione     | 15-30                 |               135 |                                   3 | 2.22%                           | 2.96%                    | €1,213.73          |
|        2024 | 2024-09      | SHOULDER      | Mezza Pensione     | 31-60                 |                87 |                                   4 | 4.60%                           | 4.60%                    | €1,307.84          |
|        2024 | 2024-09      | SHOULDER      | Mezza Pensione     | 61-90                 |               139 |                                   0 | 0.00%                           | 0.00%                    | €1,492.17          |
|        2024 | 2024-09      | SHOULDER      | Mezza Pensione     | 91-180                |               201 |                                   2 | 1.00%                           | 1.49%                    | €1,529.69          |
|        2025 | 2025-05      | LOW           | Mezza Pensione     | 15-30                 |                34 |                                   2 | 5.88%                           | 20.59%                   | €500.13            |
|        2025 | 2025-06      | SHOULDER      | Mezza Pensione     | 0-7                   |                68 |                                  18 | 26.47%                          | 30.88%                   | €747.13            |
|        2025 | 2025-06      | SHOULDER      | Mezza Pensione     | 8-14                  |                85 |                                  12 | 14.12%                          | 20.00%                   | €890.89            |
|        2025 | 2025-06      | SHOULDER      | Mezza Pensione     | 15-30                 |               135 |                                   3 | 2.22%                           | 3.70%                    | €1,233.36          |
|        2025 | 2025-06      | SHOULDER      | Mezza Pensione     | 31-60                 |               196 |                                   8 | 4.08%                           | 4.08%                    | €1,328.31          |
|        2025 | 2025-06      | SHOULDER      | Mezza Pensione     | 61-90                 |               121 |                                   6 | 4.96%                           | 5.79%                    | €1,650.38          |
|        2025 | 2025-06      | SHOULDER      | Mezza Pensione     | 91-180                |                86 |                                   5 | 5.81%                           | 5.81%                    | €1,938.78          |
|        2025 | 2025-07      | PEAK          | Mezza Pensione     | 0-7                   |                78 |                                   8 | 10.26%                          | 10.26%                   | €1,483.34          |
|        2025 | 2025-07      | PEAK          | Mezza Pensione     | 8-14                  |                91 |                                   7 | 7.69%                           | 9.89%                    | €1,580.64          |
|        2025 | 2025-07      | PEAK          | Mezza Pensione     | 15-30                 |               214 |                                  13 | 6.07%                           | 7.01%                    | €1,857.54          |
|        2025 | 2025-07      | PEAK          | Mezza Pensione     | 31-60                 |               249 |                                   8 | 3.21%                           | 4.42%                    | €1,993.15          |
|        2025 | 2025-07      | PEAK          | Mezza Pensione     | 61-90                 |               139 |                                   4 | 2.88%                           | 2.88%                    | €2,045.88          |
|        2025 | 2025-07      | PEAK          | Mezza Pensione     | 91-180                |               311 |                                   6 | 1.93%                           | 1.93%                    | €2,320.18          |
|        2025 | 2025-08      | PEAK          | Mezza Pensione     | 0-7                   |                81 |                                   9 | 11.11%                          | 14.81%                   | €1,182.90          |
|        2025 | 2025-08      | PEAK          | Mezza Pensione     | 8-14                  |                84 |                                   7 | 8.33%                           | 11.90%                   | €1,368.77          |
|        2025 | 2025-08      | PEAK          | Mezza Pensione     | 15-30                 |               197 |                                   8 | 4.06%                           | 6.60%                    | €1,757.10          |
|        2025 | 2025-08      | PEAK          | Mezza Pensione     | 31-60                 |               311 |                                   7 | 2.25%                           | 2.57%                    | €2,342.03          |
|        2025 | 2025-08      | PEAK          | Mezza Pensione     | 61-90                 |               292 |                                   7 | 2.40%                           | 3.77%                    | €2,614.70          |
|        2025 | 2025-08      | PEAK          | Mezza Pensione     | 91-180                |               548 |                                  14 | 2.55%                           | 3.10%                    | €2,784.08          |
|        2025 | 2025-08      | PEAK          | Mezza Pensione     | 181+                  |                32 |                                   0 | 0.00%                           | 0.00%                    | €3,809.55          |
|        2025 | 2025-09      | SHOULDER      | Mezza Pensione     | 0-7                   |                65 |                                  19 | 29.23%                          | 30.77%                   | €677.69            |
|        2025 | 2025-09      | SHOULDER      | Mezza Pensione     | 8-14                  |                71 |                                   7 | 9.86%                           | 9.86%                    | €824.96            |
|        2025 | 2025-09      | SHOULDER      | Mezza Pensione     | 15-30                 |                66 |                                   3 | 4.55%                           | 4.55%                    | €764.58            |
|        2025 | 2025-09      | SHOULDER      | Mezza Pensione     | 31-60                 |                66 |                                   2 | 3.03%                           | 4.55%                    | €1,168.95          |
|        2025 | 2025-09      | SHOULDER      | Mezza Pensione     | 61-90                 |                37 |                                   3 | 8.11%                           | 8.11%                    | €1,155.13          |
|        2025 | 2025-09      | SHOULDER      | Mezza Pensione     | 91-180                |                43 |                                   0 | 0.00%                           | 0.00%                    | €1,448.64          |
|        2026 | 2026-06      | SHOULDER      | Mezza Pensione     | 0-7                   |                54 |                                   6 | 11.11%                          | 11.11%                   | €676.21            |
|        2026 | 2026-06      | SHOULDER      | Mezza Pensione     | 8-14                  |                44 |                                   4 | 9.09%                           | 9.09%                    | €765.89            |
|        2026 | 2026-06      | SHOULDER      | Mezza Pensione     | 15-30                 |               104 |                                   7 | 6.73%                           | 6.73%                    | €940.30            |
|        2026 | 2026-06      | SHOULDER      | Mezza Pensione     | 31-60                 |               123 |                                   8 | 6.50%                           | 7.32%                    | €1,064.64          |
|        2026 | 2026-06      | SHOULDER      | Mezza Pensione     | 61-90                 |               137 |                                   7 | 5.11%                           | 5.11%                    | €1,444.61          |
|        2026 | 2026-06      | SHOULDER      | Mezza Pensione     | 91-180                |               194 |                                   6 | 3.09%                           | 3.09%                    | €1,777.96          |
|        2026 | 2026-07      | PEAK          | Mezza Pensione     | 0-7                   |                65 |                                   2 | 3.08%                           | 3.08%                    | €1,404.81          |
|        2026 | 2026-07      | PEAK          | Mezza Pensione     | 8-14                  |                93 |                                   3 | 3.23%                           | 3.23%                    | €1,851.96          |
|        2026 | 2026-07      | PEAK          | Mezza Pensione     | 15-30                 |               245 |                                   3 | 1.22%                           | 1.22%                    | €2,089.58          |
|        2026 | 2026-07      | PEAK          | Mezza Pensione     | 31-60                 |               269 |                                   4 | 1.49%                           | 1.49%                    | €2,277.83          |
|        2026 | 2026-07      | PEAK          | Mezza Pensione     | 61-90                 |               229 |                                  10 | 4.37%                           | 4.37%                    | €2,207.72          |
|        2026 | 2026-07      | PEAK          | Mezza Pensione     | 91-180                |               488 |                                  18 | 3.69%                           | 3.69%                    | €2,524.73          |
|        2026 | 2026-07      | PEAK          | Mezza Pensione     | 181+                  |                49 |                                   4 | 8.16%                           | 8.16%                    | €2,756.82          |
|        2025 | 2025-07      | PEAK          | Only Bed           | 15-30                 |                39 |                                   0 | 0.00%                           | 0.00%                    | €1,887.26          |
|        2025 | 2025-07      | PEAK          | Only Bed           | 31-60                 |                32 |                                   0 | 0.00%                           | 3.12%                    | €1,826.25          |
|        2025 | 2025-08      | PEAK          | Only Bed           | 31-60                 |                40 |                                   1 | 2.50%                           | 2.50%                    | €2,226.78          |
|        2025 | 2025-08      | PEAK          | Only Bed           | 61-90                 |                48 |                                   0 | 0.00%                           | 0.00%                    | €2,427.89          |
|        2025 | 2025-08      | PEAK          | Only Bed           | 91-180                |               103 |                                   1 | 0.97%                           | 0.97%                    | €2,495.11          |
|        2024 | 2024-06      | SHOULDER      | Pensione Completa  | 0-7                   |                38 |                                   2 | 5.26%                           | 5.26%                    | €1,373.78          |
|        2024 | 2024-06      | SHOULDER      | Pensione Completa  | 8-14                  |                58 |                                   1 | 1.72%                           | 1.72%                    | €1,616.06          |
|        2024 | 2024-06      | SHOULDER      | Pensione Completa  | 15-30                 |               149 |                                   2 | 1.34%                           | 1.34%                    | €2,030.20          |
|        2024 | 2024-06      | SHOULDER      | Pensione Completa  | 31-60                 |                83 |                                   3 | 3.61%                           | 3.61%                    | €2,246.57          |
|        2024 | 2024-06      | SHOULDER      | Pensione Completa  | 61-90                 |                72 |                                   8 | 11.11%                          | 11.11%                   | €1,814.48          |
|        2024 | 2024-06      | SHOULDER      | Pensione Completa  | 91-180                |               162 |                                  10 | 6.17%                           | 7.41%                    | €1,682.39          |
|        2024 | 2024-06      | SHOULDER      | Pensione Completa  | 181+                  |                32 |                                   6 | 18.75%                          | 18.75%                   | €1,862.29          |
|        2024 | 2024-07      | PEAK          | Pensione Completa  | 0-7                   |                51 |                                   3 | 5.88%                           | 5.88%                    | €2,127.55          |
|        2024 | 2024-07      | PEAK          | Pensione Completa  | 8-14                  |               127 |                                  11 | 8.66%                           | 8.66%                    | €2,527.54          |
|        2024 | 2024-07      | PEAK          | Pensione Completa  | 15-30                 |               185 |                                   8 | 4.32%                           | 4.32%                    | €2,760.33          |
|        2024 | 2024-07      | PEAK          | Pensione Completa  | 31-60                 |               188 |                                   5 | 2.66%                           | 2.66%                    | €3,019.00          |
|        2024 | 2024-07      | PEAK          | Pensione Completa  | 61-90                 |               113 |                                   5 | 4.42%                           | 4.42%                    | €2,877.76          |
|        2024 | 2024-07      | PEAK          | Pensione Completa  | 91-180                |               244 |                                  17 | 6.97%                           | 6.97%                    | €2,478.18          |
|        2024 | 2024-07      | PEAK          | Pensione Completa  | 181+                  |                77 |                                   7 | 9.09%                           | 9.09%                    | €2,493.92          |
|        2024 | 2024-08      | PEAK          | Pensione Completa  | 0-7                   |                78 |                                   7 | 8.97%                           | 8.97%                    | €2,240.46          |
|        2024 | 2024-08      | PEAK          | Pensione Completa  | 8-14                  |                97 |                                  10 | 10.31%                          | 10.31%                   | €2,822.42          |
|        2024 | 2024-08      | PEAK          | Pensione Completa  | 15-30                 |               205 |                                   9 | 4.39%                           | 4.39%                    | €3,258.30          |
|        2024 | 2024-08      | PEAK          | Pensione Completa  | 31-60                 |               257 |                                   5 | 1.95%                           | 1.95%                    | €3,616.78          |
|        2024 | 2024-08      | PEAK          | Pensione Completa  | 61-90                 |               196 |                                   1 | 0.51%                           | 0.51%                    | €3,579.69          |
|        2024 | 2024-08      | PEAK          | Pensione Completa  | 91-180                |               317 |                                  10 | 3.15%                           | 3.15%                    | €3,529.46          |
|        2024 | 2024-08      | PEAK          | Pensione Completa  | 181+                  |               145 |                                   1 | 0.69%                           | 0.69%                    | €3,662.04          |
|        2024 | 2024-09      | SHOULDER      | Pensione Completa  | 8-14                  |                71 |                                   1 | 1.41%                           | 2.82%                    | €1,649.07          |
|        2024 | 2024-09      | SHOULDER      | Pensione Completa  | 15-30                 |               100 |                                   3 | 3.00%                           | 3.00%                    | €1,483.62          |
|        2024 | 2024-09      | SHOULDER      | Pensione Completa  | 31-60                 |               112 |                                   3 | 2.68%                           | 3.57%                    | €1,677.10          |
|        2024 | 2024-09      | SHOULDER      | Pensione Completa  | 61-90                 |               135 |                                   3 | 2.22%                           | 2.22%                    | €1,777.89          |
|        2024 | 2024-09      | SHOULDER      | Pensione Completa  | 91-180                |               175 |                                   4 | 2.29%                           | 2.29%                    | €1,799.48          |
|        2025 | 2025-05      | LOW           | Pensione Completa  | 15-30                 |                51 |                                   7 | 13.73%                          | 13.73%                   | €560.33            |
|        2025 | 2025-06      | SHOULDER      | Pensione Completa  | 0-7                   |                54 |                                   6 | 11.11%                          | 20.37%                   | €912.41            |
|        2025 | 2025-06      | SHOULDER      | Pensione Completa  | 8-14                  |                62 |                                   6 | 9.68%                           | 12.90%                   | €1,311.94          |
|        2025 | 2025-06      | SHOULDER      | Pensione Completa  | 15-30                 |               191 |                                   4 | 2.09%                           | 2.09%                    | €1,544.27          |
|        2025 | 2025-06      | SHOULDER      | Pensione Completa  | 31-60                 |               385 |                                   7 | 1.82%                           | 2.08%                    | €1,747.02          |
|        2025 | 2025-06      | SHOULDER      | Pensione Completa  | 61-90                 |               175 |                                   2 | 1.14%                           | 1.71%                    | €2,069.76          |
|        2025 | 2025-06      | SHOULDER      | Pensione Completa  | 91-180                |               121 |                                   1 | 0.83%                           | 0.83%                    | €2,333.76          |
|        2025 | 2025-07      | PEAK          | Pensione Completa  | 0-7                   |                78 |                                   3 | 3.85%                           | 5.13%                    | €1,810.82          |
|        2025 | 2025-07      | PEAK          | Pensione Completa  | 8-14                  |               121 |                                   2 | 1.65%                           | 3.31%                    | €2,021.59          |
|        2025 | 2025-07      | PEAK          | Pensione Completa  | 15-30                 |               231 |                                   7 | 3.03%                           | 3.46%                    | €2,383.21          |
|        2025 | 2025-07      | PEAK          | Pensione Completa  | 31-60                 |               347 |                                   2 | 0.58%                           | 1.15%                    | €2,484.02          |
|        2025 | 2025-07      | PEAK          | Pensione Completa  | 61-90                 |               246 |                                   2 | 0.81%                           | 1.22%                    | €2,498.22          |
|        2025 | 2025-07      | PEAK          | Pensione Completa  | 91-180                |               472 |                                   6 | 1.27%                           | 1.69%                    | €2,801.52          |
|        2025 | 2025-08      | PEAK          | Pensione Completa  | 0-7                   |                89 |                                   4 | 4.49%                           | 6.74%                    | €1,679.22          |
|        2025 | 2025-08      | PEAK          | Pensione Completa  | 8-14                  |                97 |                                   3 | 3.09%                           | 7.22%                    | €1,920.87          |
|        2025 | 2025-08      | PEAK          | Pensione Completa  | 15-30                 |               215 |                                   5 | 2.33%                           | 2.79%                    | €2,370.60          |
|        2025 | 2025-08      | PEAK          | Pensione Completa  | 31-60                 |               372 |                                   2 | 0.54%                           | 1.08%                    | €2,733.60          |
|        2025 | 2025-08      | PEAK          | Pensione Completa  | 61-90                 |               400 |                                   2 | 0.50%                           | 1.25%                    | €2,936.67          |
|        2025 | 2025-08      | PEAK          | Pensione Completa  | 91-180                |               781 |                                   3 | 0.38%                           | 0.90%                    | €3,147.17          |
|        2025 | 2025-08      | PEAK          | Pensione Completa  | 181+                  |                52 |                                   1 | 1.92%                           | 1.92%                    | €2,821.08          |
|        2025 | 2025-09      | SHOULDER      | Pensione Completa  | 0-7                   |                35 |                                   4 | 11.43%                          | 20.00%                   | €818.91            |
|        2025 | 2025-09      | SHOULDER      | Pensione Completa  | 8-14                  |                35 |                                   2 | 5.71%                           | 8.57%                    | €1,057.15          |
|        2025 | 2025-09      | SHOULDER      | Pensione Completa  | 15-30                 |                51 |                                   0 | 0.00%                           | 0.00%                    | €1,236.07          |
|        2025 | 2025-09      | SHOULDER      | Pensione Completa  | 31-60                 |                77 |                                   3 | 3.90%                           | 5.19%                    | €1,515.35          |
|        2025 | 2025-09      | SHOULDER      | Pensione Completa  | 61-90                 |                45 |                                   1 | 2.22%                           | 6.67%                    | €1,713.23          |
|        2025 | 2025-09      | SHOULDER      | Pensione Completa  | 91-180                |                65 |                                   1 | 1.54%                           | 1.54%                    | €1,889.16          |
|        2026 | 2026-06      | SHOULDER      | Pensione Completa  | 0-7                   |                54 |                                   1 | 1.85%                           | 7.41%                    | €1,169.05          |
|        2026 | 2026-06      | SHOULDER      | Pensione Completa  | 8-14                  |                49 |                                   0 | 0.00%                           | 0.00%                    | €1,291.50          |
|        2026 | 2026-06      | SHOULDER      | Pensione Completa  | 15-30                 |               119 |                                   3 | 2.52%                           | 5.04%                    | €1,513.80          |
|        2026 | 2026-06      | SHOULDER      | Pensione Completa  | 31-60                 |               167 |                                   3 | 1.80%                           | 2.40%                    | €1,649.74          |
|        2026 | 2026-06      | SHOULDER      | Pensione Completa  | 61-90                 |               173 |                                   0 | 0.00%                           | 1.16%                    | €1,920.36          |
|        2026 | 2026-06      | SHOULDER      | Pensione Completa  | 91-180                |               299 |                                   1 | 0.33%                           | 1.00%                    | €2,291.91          |
|        2026 | 2026-06      | SHOULDER      | Pensione Completa  | 181+                  |                37 |                                   0 | 0.00%                           | 2.70%                    | €2,306.28          |
|        2026 | 2026-07      | PEAK          | Pensione Completa  | 0-7                   |               101 |                                   1 | 0.99%                           | 0.99%                    | €2,127.07          |
|        2026 | 2026-07      | PEAK          | Pensione Completa  | 8-14                  |               121 |                                   0 | 0.00%                           | 2.48%                    | €2,572.28          |
|        2026 | 2026-07      | PEAK          | Pensione Completa  | 15-30                 |               265 |                                   0 | 0.00%                           | 0.00%                    | €2,719.66          |
|        2026 | 2026-07      | PEAK          | Pensione Completa  | 31-60                 |               398 |                                   1 | 0.25%                           | 0.25%                    | €2,766.60          |
|        2026 | 2026-07      | PEAK          | Pensione Completa  | 61-90                 |               311 |                                   2 | 0.64%                           | 1.29%                    | €2,673.74          |
|        2026 | 2026-07      | PEAK          | Pensione Completa  | 91-180                |               760 |                                   8 | 1.05%                           | 1.71%                    | €3,089.58          |
|        2026 | 2026-07      | PEAK          | Pensione Completa  | 181+                  |               102 |                                   0 | 0.00%                           | 1.96%                    | €3,220.42          |

### Room × treatment × year × season / month

|   stay_year | stay_month   | season_band   | room_name                  | arrangement_name   |   confirmed_bookings | avg_adr   | revenue    |   avg_booking_window |   avg_los | reliability   |
|------------:|:-------------|:--------------|:---------------------------|:-------------------|---------------------:|:----------|:-----------|---------------------:|----------:|:--------------|
|        2025 | 2025-06      | SHOULDER      | Appartamento Area Giardino | Bed & Breakfast    |                   20 | €111.07   | €8,260.87  |                31.1  |      3.75 | LOW           |
|        2025 | 2025-07      | PEAK          | Appartamento Area Giardino | Bed & Breakfast    |                   10 | €101.56   | €5,896.28  |                89.9  |      6.7  | LOW           |
|        2025 | 2025-08      | PEAK          | Appartamento Area Giardino | Bed & Breakfast    |                   20 | €151.68   | €17,398.90 |                79.3  |      6.15 | LOW           |
|        2024 | 2024-06      | SHOULDER      | Appartamento Area Giardino | Mezza Pensione     |                   48 | €174.42   | €55,186.00 |                78.35 |      6.77 | MEDIUM        |
|        2024 | 2024-07      | PEAK          | Appartamento Area Giardino | Mezza Pensione     |                   17 | €106.51   | €17,620.50 |                98.94 |      9.24 | LOW           |
|        2024 | 2024-08      | PEAK          | Appartamento Area Giardino | Mezza Pensione     |                   20 | €280.15   | €45,541.50 |               111.5  |      7.75 | LOW           |
|        2024 | 2024-09      | SHOULDER      | Appartamento Area Giardino | Mezza Pensione     |                   23 | €133.81   | €19,391.50 |                53.22 |      6.57 | LOW           |
|        2025 | 2025-06      | SHOULDER      | Appartamento Area Giardino | Mezza Pensione     |                   47 | €188.44   | €42,412.84 |                22.32 |      4.7  | MEDIUM        |
|        2025 | 2025-07      | PEAK          | Appartamento Area Giardino | Mezza Pensione     |                   42 | €234.81   | €65,764.25 |                68.31 |      6.62 | MEDIUM        |
|        2025 | 2025-08      | PEAK          | Appartamento Area Giardino | Mezza Pensione     |                   39 | €246.04   | €68,098.16 |                79.64 |      7.21 | MEDIUM        |
|        2025 | 2025-09      | SHOULDER      | Appartamento Area Giardino | Mezza Pensione     |                   32 | €214.86   | €22,051.44 |                11.19 |      3.22 | MEDIUM        |
|        2026 | 2026-05      | LOW           | Appartamento Area Giardino | Mezza Pensione     |                   19 | €173.35   | €6,546.78  |                 3.63 |      2    | LOW           |
|        2026 | 2026-06      | SHOULDER      | Appartamento Area Giardino | Mezza Pensione     |                   43 | €211.85   | €62,501.07 |                49.81 |      6.91 | MEDIUM        |
|        2026 | 2026-07      | PEAK          | Appartamento Area Giardino | Mezza Pensione     |                   33 | €277.48   | €63,839.62 |                53.67 |      6.58 | MEDIUM        |
|        2025 | 2025-07      | PEAK          | Appartamento Area Giardino | Only Bed           |                   34 | €73.07    | €20,812.98 |               120.47 |      9.26 | MEDIUM        |
|        2025 | 2025-08      | PEAK          | Appartamento Area Giardino | Only Bed           |                   46 | €88.54    | €38,472.85 |               142.63 |      8.54 | MEDIUM        |
|        2024 | 2024-06      | SHOULDER      | Appartamento Area Giardino | Pensione Completa  |                   58 | €138.62   | €67,131.90 |                82.05 |      7.38 | MEDIUM        |
|        2024 | 2024-07      | PEAK          | Appartamento Area Giardino | Pensione Completa  |                   58 | €208.08   | €91,752.00 |                95.78 |      7.22 | MEDIUM        |
|        2024 | 2024-08      | PEAK          | Appartamento Area Giardino | Pensione Completa  |                   60 | €147.15   | €70,789.00 |               104.22 |      7.45 | MEDIUM        |
|        2024 | 2024-09      | SHOULDER      | Appartamento Area Giardino | Pensione Completa  |                   18 | €200.62   | €22,161.00 |                32.89 |      5.39 | LOW           |
|        2025 | 2025-06      | SHOULDER      | Appartamento Area Giardino | Pensione Completa  |                   22 | €239.64   | €26,091.26 |                49.18 |      4.95 | LOW           |
|        2025 | 2025-07      | PEAK          | Appartamento Area Giardino | Pensione Completa  |                   15 | €246.26   | €25,793.00 |                95    |      6.87 | LOW           |
|        2025 | 2025-08      | PEAK          | Appartamento Area Giardino | Pensione Completa  |                   12 | €266.39   | €25,351.35 |                75.67 |      7.75 | LOW           |
|        2026 | 2026-05      | LOW           | Appartamento Area Giardino | Pensione Completa  |                   35 | €165.85   | €17,598.30 |                22.86 |      2.94 | MEDIUM        |
|        2026 | 2026-06      | SHOULDER      | Appartamento Area Giardino | Pensione Completa  |                   13 | €219.83   | €19,244.27 |                47.23 |      6.46 | LOW           |
|        2026 | 2026-07      | PEAK          | Appartamento Area Giardino | Pensione Completa  |                   10 | €290.68   | €18,283.39 |                77.9  |      5.8  | LOW           |
|        2025 | 2025-06      | SHOULDER      | Appartamento Area Piscina  | Bed & Breakfast    |                   22 | €109.29   | €7,674.71  |                18.09 |      3.14 | LOW           |
|        2025 | 2025-07      | PEAK          | Appartamento Area Piscina  | Bed & Breakfast    |                   12 | €210.99   | €20,273.03 |                34.67 |      8    | LOW           |
|        2024 | 2024-06      | SHOULDER      | Appartamento Area Piscina  | Mezza Pensione     |                   38 | €157.48   | €35,754.50 |                70    |      5.26 | MEDIUM        |
|        2024 | 2024-07      | PEAK          | Appartamento Area Piscina  | Mezza Pensione     |                   19 | €301.30   | €46,669.50 |                65.53 |      7.89 | LOW           |
|        2024 | 2024-08      | PEAK          | Appartamento Area Piscina  | Mezza Pensione     |                   22 | €394.53   | €63,874.00 |                59.68 |      7.45 | LOW           |
|        2024 | 2024-09      | SHOULDER      | Appartamento Area Piscina  | Mezza Pensione     |                   11 | €181.75   | €14,494.00 |                47.09 |      7.18 | LOW           |
|        2025 | 2025-06      | SHOULDER      | Appartamento Area Piscina  | Mezza Pensione     |                   32 | €185.80   | €36,357.59 |                32.81 |      6.03 | MEDIUM        |
|        2025 | 2025-07      | PEAK          | Appartamento Area Piscina  | Mezza Pensione     |                   35 | €258.82   | €59,934.97 |                35.91 |      6.66 | MEDIUM        |
|        2025 | 2025-08      | PEAK          | Appartamento Area Piscina  | Mezza Pensione     |                   38 | €280.64   | €79,045.87 |                59.76 |      7.53 | MEDIUM        |
|        2025 | 2025-09      | SHOULDER      | Appartamento Area Piscina  | Mezza Pensione     |                   19 | €181.67   | €17,252.65 |                14.79 |      5.16 | LOW           |
|        2026 | 2026-05      | LOW           | Appartamento Area Piscina  | Mezza Pensione     |                   13 | €163.52   | €7,349.84  |                32.69 |      3.31 | LOW           |
|        2026 | 2026-06      | SHOULDER      | Appartamento Area Piscina  | Mezza Pensione     |                   39 | €188.02   | €43,523.32 |                30.38 |      5.82 | MEDIUM        |
|        2026 | 2026-07      | PEAK          | Appartamento Area Piscina  | Mezza Pensione     |                   36 | €291.69   | €71,422.35 |                51.81 |      6.58 | MEDIUM        |
|        2024 | 2024-06      | SHOULDER      | Appartamento Area Piscina  | Pensione Completa  |                   42 | €162.40   | €45,022.50 |                57.05 |      6.36 | MEDIUM        |
|        2024 | 2024-07      | PEAK          | Appartamento Area Piscina  | Pensione Completa  |                   33 | €283.06   | €69,742.00 |                58.36 |      7.09 | MEDIUM        |
|        2024 | 2024-08      | PEAK          | Appartamento Area Piscina  | Pensione Completa  |                   34 | €342.67   | €86,844.50 |                55.47 |      7.29 | MEDIUM        |
|        2024 | 2024-09      | SHOULDER      | Appartamento Area Piscina  | Pensione Completa  |                   19 | €171.77   | €19,529.50 |                50.68 |      5    | LOW           |
|        2025 | 2025-05      | LOW           | Appartamento Area Piscina  | Pensione Completa  |                   14 | €242.21   | €6,946.35  |                21.86 |      2.14 | LOW           |
|        2025 | 2025-06      | SHOULDER      | Appartamento Area Piscina  | Pensione Completa  |                   15 | €210.96   | €19,143.23 |                42.27 |      6.07 | LOW           |
|        2025 | 2025-07      | PEAK          | Appartamento Area Piscina  | Pensione Completa  |                   22 | €219.47   | €37,219.90 |                55    |      7.27 | LOW           |
|        2025 | 2025-08      | PEAK          | Appartamento Area Piscina  | Pensione Completa  |                   20 | €219.49   | €30,480.50 |                59.15 |      6.65 | LOW           |
|        2026 | 2026-05      | LOW           | Appartamento Area Piscina  | Pensione Completa  |                   20 | €90.40    | €4,367.54  |                29.6  |      2.65 | LOW           |
|        2026 | 2026-06      | SHOULDER      | Appartamento Area Piscina  | Pensione Completa  |                   17 | €205.35   | €18,763.51 |                33.47 |      4.82 | LOW           |
|        2026 | 2026-07      | PEAK          | Appartamento Area Piscina  | Pensione Completa  |                   17 | €303.70   | €33,125.83 |                51.94 |      5.71 | LOW           |
|        2025 | 2025-06      | SHOULDER      | Camera  Standard           | Bed & Breakfast    |                   24 | €105.59   | €6,424.01  |                24.21 |      2.54 | LOW           |
|        2025 | 2025-07      | PEAK          | Camera  Standard           | Bed & Breakfast    |                   29 | €140.82   | €18,688.26 |                38.76 |      4.41 | LOW           |
|        2025 | 2025-08      | PEAK          | Camera  Standard           | Bed & Breakfast    |                   21 | €158.18   | €13,154.70 |                48.86 |      4.19 | LOW           |
|        2025 | 2025-09      | SHOULDER      | Camera  Standard           | Bed & Breakfast    |                   13 | €94.80    | €2,947.93  |                 8    |      2.38 | LOW           |
|        2024 | 2024-06      | SHOULDER      | Camera  Standard           | Mezza Pensione     |                   32 | €112.38   | €24,179.20 |                72.44 |      6.84 | MEDIUM        |
|        2024 | 2024-08      | PEAK          | Camera  Standard           | Mezza Pensione     |                   12 | €329.45   | €26,294.50 |                21.42 |      6.17 | LOW           |
|        2024 | 2024-09      | SHOULDER      | Camera  Standard           | Mezza Pensione     |                   19 | €118.06   | €14,306.50 |               103.74 |      5.95 | LOW           |
|        2025 | 2025-06      | SHOULDER      | Camera  Standard           | Mezza Pensione     |                   39 | €133.28   | €25,853.85 |                45.18 |      4.56 | MEDIUM        |
|        2025 | 2025-07      | PEAK          | Camera  Standard           | Mezza Pensione     |                   44 | €180.00   | €40,032.29 |                46.59 |      4.82 | MEDIUM        |
|        2025 | 2025-08      | PEAK          | Camera  Standard           | Mezza Pensione     |                   40 | €215.56   | €52,661.54 |                72.7  |      6    | MEDIUM        |
|        2025 | 2025-09      | SHOULDER      | Camera  Standard           | Mezza Pensione     |                   32 | €143.27   | €13,821.28 |                12.41 |      3    | MEDIUM        |
|        2026 | 2026-06      | SHOULDER      | Camera  Standard           | Mezza Pensione     |                   50 | €139.61   | €35,110.22 |                38.2  |      4.82 | MEDIUM        |
|        2026 | 2026-07      | PEAK          | Camera  Standard           | Mezza Pensione     |                   41 | €211.81   | €46,065.72 |                65    |      5.54 | MEDIUM        |
|        2024 | 2024-06      | SHOULDER      | Camera  Standard           | Pensione Completa  |                   46 | €93.97    | €29,043.50 |                76.46 |      6.11 | MEDIUM        |
|        2024 | 2024-07      | PEAK          | Camera  Standard           | Pensione Completa  |                   46 | €107.27   | €35,347.00 |                69.07 |      6.43 | MEDIUM        |
|        2024 | 2024-08      | PEAK          | Camera  Standard           | Pensione Completa  |                   35 | €91.38    | €28,446.00 |                76.91 |      7.09 | MEDIUM        |
|        2024 | 2024-09      | SHOULDER      | Camera  Standard           | Pensione Completa  |                   13 | €127.36   | €10,050.00 |                92.38 |      6.54 | LOW           |
|        2025 | 2025-06      | SHOULDER      | Camera  Standard           | Pensione Completa  |                   20 | €151.48   | €11,251.80 |                34.95 |      3.4  | LOW           |
|        2025 | 2025-07      | PEAK          | Camera  Standard           | Pensione Completa  |                   34 | €123.57   | €19,845.39 |                32.62 |      3.68 | MEDIUM        |
|        2025 | 2025-08      | PEAK          | Camera  Standard           | Pensione Completa  |                   26 | €164.54   | €25,994.14 |                49    |      4.54 | LOW           |
|        2025 | 2025-09      | SHOULDER      | Camera  Standard           | Pensione Completa  |                   16 | €106.64   | €4,907.74  |                19.12 |      2.62 | LOW           |
|        2026 | 2026-05      | LOW           | Camera  Standard           | Pensione Completa  |                   22 | €178.95   | €12,608.78 |                31.09 |      2.95 | LOW           |
|        2026 | 2026-06      | SHOULDER      | Camera  Standard           | Pensione Completa  |                   24 | €125.40   | €13,810.26 |                23.29 |      4.12 | LOW           |
|        2026 | 2026-07      | PEAK          | Camera  Standard           | Pensione Completa  |                   16 | €192.61   | €18,938.31 |                41.75 |      5.12 | LOW           |
|        2025 | 2025-07      | PEAK          | Camera Deluxe              | Mezza Pensione     |                   10 | €252.19   | €15,135.58 |                54.4  |      5.5  | LOW           |
|        2026 | 2026-06      | SHOULDER      | Camera Deluxe              | Mezza Pensione     |                   10 | €180.61   | €10,908.96 |                19.9  |      6    | LOW           |
|        2024 | 2024-06      | SHOULDER      | Camera Deluxe              | Pensione Completa  |                   19 | €178.72   | €23,991.00 |               103.89 |      6.53 | LOW           |
|        2024 | 2024-07      | PEAK          | Camera Deluxe              | Pensione Completa  |                   19 | €309.93   | €40,020.50 |                65    |      6.68 | LOW           |
|        2024 | 2024-08      | PEAK          | Camera Deluxe              | Pensione Completa  |                   20 | €351.77   | €50,911.50 |                36.3  |      6.9  | LOW           |
|        2025 | 2025-06      | SHOULDER      | Camera Deluxe              | Pensione Completa  |                   13 | €226.76   | €16,351.85 |               118.23 |      5.77 | LOW           |
|        2025 | 2025-07      | PEAK          | Camera Deluxe              | Pensione Completa  |                   13 | €218.04   | €16,076.40 |                59.54 |      4.62 | LOW           |
|        2025 | 2025-06      | SHOULDER      | Camera Superior            | Bed & Breakfast    |                   18 | €85.22    | €8,748.40  |                42.5  |      4.44 | LOW           |
|        2025 | 2025-07      | PEAK          | Camera Superior            | Bed & Breakfast    |                   15 | €165.69   | €9,317.53  |                47.73 |      3.67 | LOW           |
|        2025 | 2025-08      | PEAK          | Camera Superior            | Bed & Breakfast    |                   16 | €182.46   | €12,936.18 |                44.5  |      4.25 | LOW           |
|        2024 | 2024-06      | SHOULDER      | Camera Superior            | Mezza Pensione     |                   13 | €136.09   | €12,022.00 |                66.38 |      6.77 | LOW           |
|        2024 | 2024-07      | PEAK          | Camera Superior            | Mezza Pensione     |                   15 | €304.86   | €25,730.55 |                29.13 |      5.6  | LOW           |
|        2025 | 2025-06      | SHOULDER      | Camera Superior            | Mezza Pensione     |                   16 | €165.10   | €13,722.12 |                26.56 |      5.06 | LOW           |
|        2025 | 2025-07      | PEAK          | Camera Superior            | Mezza Pensione     |                   21 | €218.05   | €25,719.80 |                59.81 |      5.57 | LOW           |
|        2025 | 2025-08      | PEAK          | Camera Superior            | Mezza Pensione     |                   23 | €267.29   | €40,200.20 |                82.3  |      6.39 | LOW           |
|        2025 | 2025-09      | SHOULDER      | Camera Superior            | Mezza Pensione     |                   13 | €192.87   | €9,151.98  |                33.54 |      3.38 | LOW           |
|        2026 | 2026-06      | SHOULDER      | Camera Superior            | Mezza Pensione     |                   31 | €159.61   | €25,982.06 |                38.48 |      4.87 | MEDIUM        |
|        2026 | 2026-07      | PEAK          | Camera Superior            | Mezza Pensione     |                   29 | €256.37   | €45,600.39 |                57.03 |      6.1  | LOW           |
|        2024 | 2024-06      | SHOULDER      | Camera Superior            | Pensione Completa  |                   20 | €141.33   | €15,678.40 |                50.45 |      5.05 | LOW           |
|        2024 | 2024-07      | PEAK          | Camera Superior            | Pensione Completa  |                   26 | €248.36   | €41,474.50 |                58.42 |      6.19 | LOW           |
|        2024 | 2024-08      | PEAK          | Camera Superior            | Pensione Completa  |                   31 | €238.51   | €53,860.50 |                18.84 |      6.23 | MEDIUM        |
|        2024 | 2024-09      | SHOULDER      | Camera Superior            | Pensione Completa  |                   13 | €118.63   | €11,318.00 |                72.69 |      6.23 | LOW           |
|        2025 | 2025-07      | PEAK          | Camera Superior            | Pensione Completa  |                   14 | €205.55   | €16,917.19 |                69.64 |      6.79 | LOW           |
|        2025 | 2025-08      | PEAK          | Camera Superior            | Pensione Completa  |                   11 | €270.79   | €15,571.80 |                45.55 |      4.73 | LOW           |
|        2026 | 2026-05      | LOW           | Camera Superior            | Pensione Completa  |                   13 | €145.04   | €5,247.13  |                27.08 |      2.62 | LOW           |
|        2026 | 2026-06      | SHOULDER      | Camera Superior            | Pensione Completa  |                   13 | €157.58   | €12,948.31 |                35.54 |      5.15 | LOW           |

**Full-population evidence:** every crossover above is also written as a dedicated `crossover_*.csv` file in the output folder, including low-volume combinations that are intentionally filtered from the readable Markdown report.

## Data-quality checks

| check                   | dataset                   | status   |   details |
|:------------------------|:--------------------------|:---------|----------:|
| required_columns        | fact_prenotazioni         | PASS     |           |
| required_columns        | fact_richieste            | PASS     |           |
| required_columns        | fact_richieste_preventivi | PASS     |           |
| required_columns        | dim_camere                | PASS     |           |
| required_columns        | dim_trattamenti           | PASS     |           |
| unique_booking_code     | fact_prenotazioni         | PASS     |         0 |
| checkout_after_checkin  | fact_prenotazioni         | PASS     |         0 |
| nonnegative_stay_amount | fact_prenotazioni         | WARN     |        21 |
| quotes_have_request     | fact_richieste_preventivi | PASS     |         0 |

## Methodology and limits

- **Operating period:** inferred from months with meaningful occupied inventory. It is not an official opening calendar.
- **Room occupancy:** current catalogue capacity is applied historically. Room reassignment and historical capacity changes can create room-type/date values above 100%; these are flagged, not clipped.
- **Treatment comparability:** standard commercial board/rate plans are ranked together. Residence, multiproprietà and special categories remain visible but are excluded from directly comparable rankings.
- **Reliability:** full-population tables include every category. Reliable rankings generally require at least 30 observations.
- **Conversion:** request-to-booking conversion is reconstructed one-to-one because the source has no direct request-to-booking identifier. Room/treatment conversion therefore remains a proxy and should be used comparatively.
- **Same-room / same-treatment conversion:** these metrics measure whether a request containing a quoted solution ultimately matched to a booking of that same solution; they are more specific than overall request conversion.
- **Causality:** differences describe historical associations, not price elasticity or causal impact.
- **Cross-year comparison:** historical crossover tables use completed stay periods for bookings and completed stay months for conversion; incomplete future stay months are not treated as final YoY performance.
- **Live pickup:** a single extraction supports historical distributions; recurring snapshots are required for reliable acceleration/deceleration signals.
