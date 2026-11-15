"""Turn nex_cache.json into the NEX constant for index.html.
Per model: monthly mean over each window, change vs that model's own 2001-2025 mean; then mean across models."""
import json, os, sys, io

HERE = os.path.dirname(os.path.abspath(__file__))
cache = json.load(open(os.path.join(HERE, "nex_cache.json")))
POINTS = ["vellode", "fresno", "kano"]
BASE = range(2001, 2026)
WINS = [range(2026, 2036), range(2036, 2046), range(2046, 2056)]
DAYS = [31, 28.25, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
models = sorted({k.split("|")[0] for k in cache})


def mean(model, var, years, p):
    rows = [cache.get(f"{model}|{var}|{y}|{p}") for y in years]
    if any(r is None for r in rows):
        return None
    return [sum(r[m] for r in rows) / len(rows) for m in range(12)]


complete = [m for m in models if all(mean(m, v, range(2001, 2056), p) for v in ("tas", "pr") for p in POINTS)]
out = {"models": complete, "scenario": "SSP2-4.5", "base": "2001–2025", "win": ["2026–2035", "2036–2045", "2046–2055"]}
for p in POINTS:
    dT, rR = [], []
    for w in WINS:
        dts, rrs = [], []
        for m in complete:
            b, f = mean(m, "tas", BASE, p), mean(m, "tas", w, p)
            dts.append([f[i] - b[i] for i in range(12)])
            b, f = mean(m, "pr", BASE, p), mean(m, "pr", w, p)
            # months where the model's own baseline is under 5 mm carry no usable ratio: leave rain unchanged
            rrs.append([(f[i] / b[i]) if b[i] * 86400 * DAYS[i] >= 5 else 1.0 for i in range(12)])
        n = len(complete)
        dT.append([round(sum(x[i] for x in dts) / n, 2) for i in range(12)])
        rR.append([round(sum(x[i] for x in rrs) / n, 3) for i in range(12)])
    out[p] = {"dT": dT, "rR": rR}
    print(p, "annual dT", [round(sum(x) / 12, 2) for x in dT], file=sys.stderr)
    print(p, "rR 2050", rR[2], file=sys.stderr)
print("models", complete, "of", models, file=sys.stderr)
js = json.dumps(out, ensure_ascii=False, separators=(",", ":"))
if len(sys.argv) > 1 and complete:
    s = io.open(sys.argv[1], encoding="utf-8", newline="").read()
    a, b = s.index("/*NEXDATA*/") + len("/*NEXDATA*/"), s.index("/*END*/")
    io.open(sys.argv[1], "w", encoding="utf-8", newline="").write(s[:a] + js + s[b:])
    print("injected", len(js), "chars", file=sys.stderr)
