# UZHAVAN (உழவன், "The Farmer")

NASA Space Apps Challenge 2026, "Field Shift: Adapting Farms with NASA Data".

A free Tamil + English web page that tells a farmer which crop to sow next, why, and whether it still works in 2050.

## Run it

It is one file, `index.html`. No build step, no key, no login.

- Local: `python -m http.server 8765`, then open http://localhost:8765
- GitHub Pages: push `index.html` to the repo root and enable Pages on the main branch.

## What it does

1. **Village health**: monthly rain and temperature from NASA POWER, plus a soil card from ISRIC SoilGrids.
2. **Crop rotation advisor**: top three crops with a 0-100 score split into water fit, soil effect and profit. The farmer's three sliders are the weights.
3. **Climate time machine**: the bar at the bottom moves the climate from 2026 to 2050 and the crop cards re-order.
4. **Ask your field**: Tamil or English questions answered only from the village's data and scores.

Pilot villages: Vellode (Erode, India), Fresno County (California, USA), Kano (Nigeria). Tapping the map loads any other point live from NASA POWER.

## Score formula

```
water fit = min(1, (0.7 x season rain + irrigation top-up) / crop water need)
            irrigation top-up = 45% of need, for irrigated crops only
base      = weighted mean of water fit, soil effect, profit (weights = the sliders)
score     = 100 x base x (1 - 0.6 x temperature stress) - 50 if same family as last crop
            + 8 if a legume follows an exhausting crop
temperature stress = how far the hottest (or coldest) month in the season is past the
            crop's limit, 4 deg C over = total stress
```

The "Check our work" panel runs three tests in the browser: turmeric in June after paddy (58), black gram in October after paddy (74), paddy after paddy (0).

## Data

| Source | Used for | Status |
|---|---|---|
| NASA POWER climatology API (MERRA-2, 2001-2025) | Rain (PRECTOTCORR), temperature (T2M, T2M_MAX) | Live call, saved copy as fallback |
| ISRIC SoilGrids v2.0 | Texture, pH, organic carbon, 0-5 cm | Live call, saved copy as fallback |
| NASA GIBS, MODIS Terra NDVI 8-day | Greenness layer on the map | Live tiles |
| NASA NEX-GDDP-CMIP6 | Time-machine shifts | **Not yet wired in.** Shifts shown are illustrative, in the direction of IPCC AR6 |
| NASA SMAP, NISAR | Soil moisture | Roadmap only |

## Known placeholders (fix before claiming them)

- **Crop table** (water need, duration, temperature limits, margin rank, irrigated or not) holds typical agronomy values. Check each against TNAU / KVK tables and the farmer.
- **2030-2050 shifts** (`scen` in `VILLAGES`) are illustrative. Replace with NEX-GDDP-CMIP6 deltas.
- Soil for Vellode and Kano is read from the nearest SoilGrids cell that has data (the exact village point returns no value).

## Use of AI

This prototype's code and Tamil text were drafted with an AI assistant (Claude) and must be reviewed by the team. The optional chat model (Anthropic API, key entered by the user) is given only the village's data and scores and told to refuse anything beyond them. Without a key, answers come from the scoring engine and work offline.
