# UZHAVAN (உழவன், "The Farmer")

NASA Space Apps Challenge 2026, "Field Shift: Adapting Farms with NASA Data".

A free Tamil + English web page that tells a farmer which crop to sow next, why, and whether it still works in 2050.

Live site: https://amalnathkp13-boop.github.io/uzhavan/

## Run it

It is one file, `index.html`. No build step, no key, no login.

- Local: `python -m http.server 8765`, then open http://localhost:8765
- GitHub Pages: served from the `main` branch root.

## What it does

1. **Village health**: monthly rain and temperature from NASA POWER, plus a soil card from ISRIC SoilGrids.
2. **Crop rotation advisor**: top three crops with a 0-100 score split into water fit, soil effect and profit. The farmer's three sliders are the weights.
3. **Climate time machine**: the bar at the bottom moves the climate from 2026 to 2050 using NASA NEX-GDDP-CMIP6. Crop cards re-order and each shows its gain or loss against today.
4. **Ask your field**: Tamil or English questions answered only from the village's data and scores.
5. **Fertilizer plan**: each crop card opens to the published recommendation for that crop and place: N, P2O5 and K2O per hectare, the same as urea, super phosphate and potash per hectare and per acre, plus farmyard manure, biofertilizer and timing where the source gives them.

Pilot villages: Vellode (Erode, India), Fresno County (California, USA), Kano (Nigeria). Tapping the map loads any other point live from NASA POWER (without projections).

## Score formula

```
water fit = min(1, (0.7 x season rain + irrigation top-up) / crop water need)
            irrigation top-up = 45% of need, for irrigated crops only
base      = weighted mean of water fit, soil effect, profit (weights = the sliders)
score     = 100 x base x (1 - 0.6 x temperature stress) - 50 if same family as last crop
            + 8 if a legume follows an exhausting crop
temperature stress = 0 while the mean temperature over the crop's months in the field is
            inside the crop's optimal range; rises to 1 at the crop's absolute limit
            (heat above the range, cold below it)
```

Profit is a rank from 1 to 5: 5 if the crop earns at least half of the village's best crop, 4 at least a quarter, 3 an eighth, 2 a sixteenth, otherwise 1.

The "Check our work" panel runs three tests in the browser on the Vellode data: turmeric in June after paddy (water fit 0.73, about 65), black gram in October after paddy (about 74), paddy after paddy (0). The playbook's rehearsal figure for turmeric was 58, with an estimated profit rank of 4; the published figures put turmeric at 5, which gives 65.

## Data

| Source | Used for | How |
|---|---|---|
| NASA POWER climatology API (MERRA-2, 2001-2025) | Rain (PRECTOTCORR), temperature (T2M) | Live call, saved copy as fallback |
| ISRIC SoilGrids v2.0 | Texture, pH, organic carbon, 0-5 cm | Live call, saved copy as fallback. Vellode and Kano use the nearest cell that has data |
| NASA GIBS, MODIS Terra NDVI 8-day | Greenness layer on the map | Live tiles |
| NASA NEX-GDDP-CMIP6 (NCCS THREDDS) | Time machine | Daily `tas` and `pr` at each village, SSP2-4.5, 2001-2055. Per model, monthly change of 2026-2035, 2036-2045 and 2046-2055 against that model's 2001-2025; then the mean across models, added to the POWER baseline. Years in between are interpolated. Rain is left unchanged in months where a model's own baseline is under 5 mm. The model list is shown on the page |
| TNAU Agritech water-requirement table; TNAU ARS Bhavanisagar (turmeric) | Water need and duration for Tamil Nadu crops | Typed into the crop table |
| FAO Irrigation Water Management Training Manual 3, Tables 4-5 | Water need and duration for the other crops | Midpoint of the published range |
| FAO EcoCrop | Optimal and absolute temperature ranges | Typed into the crop table |
| Govt of India DES, cost of cultivation estimates 2021-22 (Tamil Nadu) | Profit rank, Vellode: paddy, maize, sorghum, green gram, black gram, groundnut, cotton, onion, sugarcane | Net return per hectare = value of produce minus cost A2+FL. Turmeric comes from a separate Coimbatore study (Govindasamy et al. 2021); sesame has no figure |
| Statistical Hand Book of Tamil Nadu 2022-23, Table 5.4; TRS report 2021-22 (onion) | Irrigated flag, Vellode: paddy, sorghum, sugarcane, cotton, groundnut, onion | Irrigated when more than half the crop's area is irrigated |
| Fresno County Crop & Livestock Report 2025; UC Davis 2026 blackeye cost study | Profit rank, Fresno | Gross value per harvested acre (not net) |
| USDA Census of Agriculture 2022, Fresno County | Irrigated flag, Fresno: cotton, alfalfa, maize, wheat | Irrigated share of harvested acres |
| IITA KKM baseline (Ayanwale et al. 2011), Bunkure, 2008; Sufiyan et al. 2022 | Kano: order of millet, sorghum, maize, cowpea, groundnut; which crops are rain-fed or dry-season irrigated | Gross margin per hectare; the five are ranked against each other with groundnut held at 3 |
| FAO Fertilizer and Plant Nutrition Bulletin 16, Tables 22 and 29, chapter 8 | Soil effect classes | Legumes fix nitrogen, other crops draw nutrients down. The 0-1 value per class is the team's |
| TNAU Crop Production Guide 2020 (Agriculture, Horticulture) | Fertilizer plan, Vellode: all 11 crops | N, P2O5, K2O, farmyard manure, biofertilizer, timing. Rainfed dose for rainfed crops, with the irrigated dose in a note |
| CDFA FREP California Fertilization Guidelines; Tyler et al. 1988 (garlic); UC Davis 2026 blackeye study | Fertilizer plan, Fresno | Converted from lb/acre. Mostly ranges that depend on yield or soil test |
| Nigeria FMARD 2015 recommendation via the IFDC AfricaFertilizer review 2018; NAERLS bulletins 239 and 242; STDF/NEPC sesame farmers' guide 2014; ICRISAT handbooks 2020 | Fertilizer plan, Kano: all 10 crops | N, P2O5, K2O; manure for millet, sorghum, groundnut and sesame |
| CDFA Healthy Soils Program compost white paper; CDFA FREP tomato brochure | Fresno compost rate; processing-tomato season nitrogen | 3 to 5 tons/acre of compost a year for annual crops; about 175 lb N/acre |
| ICAR, Indian Farming 70(3):18-21, 2020 | Soil-test adjustment at Vellode | Low fertility +25%, high -25%, with the class limits |
| NASA SMAP, NISAR | Soil moisture | Roadmap only, not used |

## Known gaps

- No sourced seasonal water figure was found for green gram, cowpea or garlic; those three use the team's estimates.
- Still team estimates, because no published figure was found: profit rank for sesame (Vellode) and for rice, tomato, onion, sesame and soybean (Kano); the irrigated flag for turmeric, maize, the pulses and sesame (Vellode), tomato, garlic and onion (Fresno), sesame and soybean (Kano). The "See the math" panel marks each one.
- The profit figures are not the same measure in the three places: net return in Tamil Nadu, gross value in Fresno, gross margin in Kano. Ranks are only compared inside one village.
- The soil effect value given to each class of crop is team judgement; only the classes are sourced.
- Fresno wheat was 16% irrigated in the 2022 census (a drought year) and 63% in 2017; the app treats it as not irrigated.
- TNAU water figures are irrigation applied in Tamil Nadu; FAO figures are crop water need. They are different quantities and are used as published.
- EcoCrop does not say whether its temperatures are daily means or daytime highs; the app compares them with mean temperature.
- Fertilizer plans are general (blanket) recommendations. At Vellode the farmer can enter Soil Health Card values (organic carbon, available P and K) and each nutrient moves +25% where the soil is low and -25% where it is high (ICAR, Indian Farming 70(3), 2020). The SoilGrids organic carbon can be used instead, but it is a map estimate for the top 5 cm, not a lab test, and the page says so.
- Fresno compost rates are the CDFA Healthy Soils Program's statewide rate for annual crops, not crop-specific. Kano manure rates for millet, sorghum and groundnut come from ICRISAT handbooks written for north-east Nigeria; none was found for maize, soybean, cowpea, tomato or onion. The Kano sesame rate comes from a 2014 farmers' guide that names no zone.
- The time machine applies climate-model changes to a climatology. It is a scenario, not a forecast.

## Use of AI

This prototype's code and Tamil text were drafted with an AI assistant (Claude) and must be reviewed by the team. The optional chat model (Anthropic API, key entered by the user) is given only the village's data and scores and told to refuse anything beyond them. Without a key, answers come from the scoring engine and work offline.

## Reproduce the projections

`python tools/fetch_nex.py` pulls the daily NEX-GDDP-CMIP6 series (1,650 point requests, about 1.5 hours) into `tools/nex_cache.json`. `python tools/nex_deltas.py index.html` turns that cache into the monthly changes and writes them into the `NEX` constant in `index.html`.
