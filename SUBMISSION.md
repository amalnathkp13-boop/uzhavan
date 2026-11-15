# UZHAVAN: submission pack

Everything here is ready to paste into the Space Apps project form, except the parts in [square brackets]. Those are yours to fill: nothing in brackets has been invented.

Submit by 21:00 IST, 15 November. The form closes at 23:59.

## Still to do by the team

- [ ] Fill in team names and the farmer's name and village (with his consent).
- [ ] Record the screen demo using the shot list below.
- [ ] Edit it with the farmer footage, keep it under 4:00, add subtitles, upload (YouTube unlisted).
- [ ] Open the live site, the repo and the video in an incognito window. All three must load.
- [ ] Read the "Use of AI" and "Honest limits" sections and make sure you agree with every line before pasting.
- [ ] Paste, attach the four screenshots, submit.

## Links

- Live site: https://amalnathkp13-boop.github.io/uzhavan/
- Code: https://github.com/amalnathkp13-boop/uzhavan
- Video: [paste the video link]

## Project page text

### Summary (one paragraph)

UZHAVAN (உழவன், "The Farmer") is a free web page, in Tamil and English, that tells a farmer which crop to sow next, why, and whether that choice still holds in 2050. The farmer picks a village and sees its rain, temperature and soil from NASA POWER and ISRIC SoilGrids. Three crops are recommended, each with a score out of 100 that is split into water fit, soil effect and profit, with every step of the arithmetic on screen. A slider moves the climate from 2026 to 2050 using NASA NEX-GDDP-CMIP6 projections, and the crop cards re-rank. The farmer can ask questions in Tamil or English and gets answers built only from that village's numbers.

### The problem

Farmers in Erode plan around the north-east monsoon, and they tell us it no longer arrives when it used to. [One or two sentences from your farmer interview, in his words.] The data that could help is free and public, but it sits behind APIs, in English, in units nobody farms in.

### What it does

1. **Village health.** Monthly rain and temperature for the village (NASA POWER, 2001–2025 average) and a soil card: texture, pH and organic carbon (ISRIC SoilGrids).
2. **Crop rotation advisor.** The top three crops for the chosen sowing month, after the crop just harvested. The farmer's three sliders (save water, soil health, profit) are the weights in the score.
3. **Climate time machine.** Drag from 2026 to 2050. Rain and temperature shift by the month-by-month change projected by five NEX-GDDP-CMIP6 models under SSP2-4.5, and every crop is re-scored. Each card shows how many points it gained or lost against today.
4. **Ask your field.** Questions in Tamil or English, answered from the village's data and scores only. It works with no internet connection.
6. **Weeds, pests and diseases.** For the Erode crops, each card lists seed treatment, herbicides and pest controls from Tamil Nadu Agricultural University's 2020 guide, dated from the sowing month, with chemicals India has since banned or restricted taken out.
5. **Fertilizer plan.** Each crop card opens to the published fertilizer recommendation for that crop and place: nitrogen, phosphorus and potash per hectare, the same as bags of urea, super phosphate and potash per acre, plus farmyard manure and biofertilizer where the source gives them.

It runs for three pilot places with the same engine: Vellode (Erode, India), Fresno County (California, USA) and Kano (Nigeria). A drop-down adds 15 more places across Erode district. Tapping the map loads the climate for any other point on Earth.

### How the score works

```
water fit = min(1, (0.7 x season rain + irrigation top-up) / crop water need)
            top-up = 45% of need, for irrigated crops only
base      = weighted mean of water fit, soil effect and profit (weights = the farmer's sliders)
score     = 100 x base x (1 - 0.6 x temperature stress)
            - 50 if the crop is in the same family as the last crop
            + 8 if a legume follows a soil-exhausting crop
```

Profit is a rank from 1 to 5, set from published figures: 5 if the crop earns at least half of the village's best crop, 4 at least a quarter, 3 an eighth, 2 a sixteenth, otherwise 1.

Temperature stress is 0 while the mean temperature over the crop's months in the field is inside the crop's optimal range, and rises to 1 at the crop's absolute limit.

The irrigation top-up matters. Vellode gets about 727 mm of rain a year and turmeric needs about 1,390 mm. A plain rain-against-need formula would tell Erode, the turmeric city, to stop growing turmeric. With the top-up, turmeric sown in June after paddy scores 65 with the note "needs assured irrigation". Paddy after paddy scores 0. The page runs these checks in the browser, under "Check our work".

### NASA and open data used

| Data | Used for | Link |
|---|---|---|
| NASA POWER climatology (MERRA-2, 2001–2025) | Monthly rain and temperature, called live | https://power.larc.nasa.gov/ |
| NASA NEX-GDDP-CMIP6 | 2030, 2040 and 2050 climate: daily temperature and rain at each village, SSP2-4.5, models ACCESS-CM2, GFDL-ESM4, IITM-ESM, MIROC6, MPI-ESM1-2-HR | https://www.nccs.nasa.gov/services/data-collections/land-based-products/nex-gddp-cmip6 |
| NASA GIBS, MODIS Terra NDVI 8-day | Greenness layer on the map | https://nasa-gibs.github.io/gibs-api-docs/ |
| ISRIC SoilGrids v2.0 | Soil texture, pH, organic carbon | https://soilgrids.org |
| TNAU Agritech Portal | Water need and duration of Tamil Nadu crops | https://agritech.tnau.ac.in |
| FAO Irrigation Water Management Training Manual 3 | Water need and duration of the other crops | https://www.fao.org/4/s2022e/s2022e00.htm |
| FAO EcoCrop | Crop temperature ranges | https://gaez.fao.org/pages/ecocrop |
| Govt of India DES, cost of cultivation 2021-22 | Profit rank for Tamil Nadu crops (net return per hectare) | https://desagri.gov.in/wp-content/uploads/2023/06/CS-Consolidated-Crop-year-wise-2021-22-4.xlsx |
| Statistical Hand Book of Tamil Nadu 2022-23, Table 5.4 | Which Tamil Nadu crops are irrigated | https://des.tn.gov.in/sites/default/files/2025-07/5.%20IRRIGATION.pdf |
| Fresno County Crop & Livestock Report 2025 | Profit rank for Fresno (gross value per acre) | https://www.fresnocountyca.gov/files/sharedassets/county/v/1/agricultural-commissioner/ag-crop-reports/ag-crop-and-livestock-report-2025.pdf |
| USDA Census of Agriculture 2022 | Which Fresno crops are irrigated | https://www.nass.usda.gov/Publications/AgCensus/2022/ |
| IITA KKM baseline study (Ayanwale et al. 2011) | Order of the rain-fed crops in Kano (gross margin) | https://cgspace.cgiar.org/bitstream/10568/88189/3/U11RepAyanwaleBaselineNothomDev.pdf |
| TNAU Crop Production Guide 2020 | Fertilizer plan for the Tamil Nadu crops (inorganic, farmyard manure, biofertilizer) | https://web.archive.org/web/20250521115847/https://agritech.tnau.ac.in//pdf/AGRICULTURE.pdf |
| CDFA FREP California Fertilization Guidelines | Fertilizer plan for Fresno | https://www.cdfa.ca.gov/is/ffldrs/frep/FertilizationGuidelines/ |
| Nigeria FMARD recommendation, in the IFDC AfricaFertilizer review 2018; NAERLS bulletins 239 and 242 | Fertilizer plan for Kano | https://api.hub.ifdc.org/server/api/core/bitstreams/6c5b908e-68d8-446d-90ca-4ac36076841e/content |
| FAO Fertilizer and Plant Nutrition Bulletin 16 | Soil effect classes: nitrogen fixed by legumes, nutrients taken up by other crops | https://www.fao.org/4/a0443e/a0443e03.pdf |

Roadmap, not used yet: NASA SMAP soil moisture, and NISAR, the radar satellite built by NASA and ISRO.

### Honest limits

- The 2050 view is a scenario, not a forecast. The projected change is modest: about +0.9 °C and +6% annual rain at Vellode, +1.1 °C at Fresno, +1.0 °C at Kano.
- Some values are still the team's estimate because no published figure was found: the profit rank for sesame at Vellode and for rice, vegetables, sesame and soybean at Kano; whether turmeric, maize, the pulses and sesame count as irrigated at Vellode; water need for green gram, cowpea and garlic. The page marks each one under "See the math".
- The weed and pest schedules come from a 2020 guide, filtered against India's banned and restricted list of 31 October 2026. They are a starting point: the page tells the farmer to check the product label and ask the agricultural officer. They cover the Erode crops only.
- Fertilizer plans are the general published recommendation. At Vellode a farmer can enter Soil Health Card values and the plan adjusts by ICAR's rule (+25% where the soil is low, -25% where it is high). Compost rates for Fresno are a statewide rate, not crop-specific, and no manure quantity was found for five of the Kano crops.
- The profit figures are net return in Tamil Nadu, gross value in Fresno and gross margin in Kano, so ranks are compared only inside one village.
- The 0 to 1 soil effect given to each class of crop is the team's judgement; the classes come from FAO Bulletin 16.
- SoilGrids has no value at the exact Vellode and Kano points; the soil card uses the nearest cell that has data and says how far away it is.

### Use of AI

[Confirm this matches what your team actually did, then paste.] The prototype's code and its Tamil text were drafted with an AI assistant (Claude, by Anthropic) and reviewed by the team. The chat box can optionally call an AI model; it is given only the village's data and scores and is told to refuse anything beyond them. Without it, answers come from the scoring engine. No AI-generated images, video or audio are used.

### Team

[Names and roles]

## Screenshots

In the `screenshots` folder, taken from the live site:

1. `1-dashboard.png`: Vellode rain, temperature and soil card
2. `2-crop-cards.png`: top three crops for Vellode, November, after paddy
3. `3-time-machine-2050.png`: Vellode at 2050, onion has dropped out of the top three and turmeric has moved in
5. `5-fertilizer-plan.png`: the fertilizer plan opened on the groundnut card
4. `4-tamil-chat.png`: "Can I sow turmeric this month?" answered in Tamil

## Screen demo shot list (the 1:00–2:30 block, 90 seconds)

Record at 1280 × 720 or larger, in English with the Tamil toggle shown once. Every step below was checked on the live site today.

| Time | Do this | Say this |
|---|---|---|
| 0:00 | Page open on Vellode. Click **English**, scroll to the chart. | "This is Vellode's rain and temperature from NASA POWER, and its soil from SoilGrids." |
| 0:15 | Scroll to the advisor. Sowing month November, last crop paddy. | "For November after paddy: groundnut 65, onion 64, black gram 63." |
| 0:25 | Drag **Save water** and **Soil health** almost to zero, leave **Profit** high. | "The farmer says profit matters most. Turmeric jumps to first place." |
| 0:35 | Put the sliders back. Open **See the math** on the first card. | "Every number is visible. Rain, crop need, the rule, the result." |
| 0:50 | Drag the bottom slider slowly from 2026 to 2050. Point at the **2050 outlook** panel. | "Now the climate moves to 2050, using NASA NEX-GDDP-CMIP6. Onion loses 8 points to heat and drops out; turmeric moves into the top three." |
| 1:00 | Click **Kano**, slider still at 2050. | "Same engine in Nigeria: onion loses 6 points and tomato takes first place." |
| 1:10 | Click **Vellode**, slider back to 2026, click **தமிழ்**. Tap the first suggested question. | "And in Tamil: can I sow turmeric this month? The answer uses only this village's numbers." |
| 1:25 | Scroll to **Check our work**, show the three ticks. | "The page tests its own arithmetic every time it loads." |

One thing in the playbook's video script does not match the finished app, so change the narration:

- The rain and temperature on screen are the 2001–2025 average, not 1981 onwards. Say "25 years of NASA data", not 45.
