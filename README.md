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

The "Check our work" panel runs three tests in the browser on the Vellode data: turmeric in June after paddy (about 58), black gram in October after paddy (about 74), paddy after paddy (0).

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
| NASA SMAP, NISAR | Soil moisture | Roadmap only, not used |

## Known gaps

- No sourced seasonal water figure was found for green gram, cowpea or garlic; those three use the team's estimates.
- Soil effect, margin rank (1-5) and the irrigated flag are team judgement, not sourced. Check them with the farmer and TNAU / KVK.
- TNAU water figures are irrigation applied in Tamil Nadu; FAO figures are crop water need. They are different quantities and are used as published.
- EcoCrop does not say whether its temperatures are daily means or daytime highs; the app compares them with mean temperature.
- The time machine applies climate-model changes to a climatology. It is a scenario, not a forecast.

## Use of AI

This prototype's code and Tamil text were drafted with an AI assistant (Claude) and must be reviewed by the team. The optional chat model (Anthropic API, key entered by the user) is given only the village's data and scores and told to refuse anything beyond them. Without a key, answers come from the scoring engine and work offline.

## Reproduce the projections

`python tools/fetch_nex.py` pulls the daily NEX-GDDP-CMIP6 series (1,650 point requests, about 1.5 hours) into `tools/nex_cache.json`. `python tools/nex_deltas.py index.html` turns that cache into the monthly changes and writes them into the `NEX` constant in `index.html`.
