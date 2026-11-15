"""Pull monthly tas/pr at 3 points from NASA NEX-GDDP-CMIP6 (NCCS THREDDS, NetCDF Subset point requests).
Caches every (model, var, year, point) result in nex_cache.json so it can be resumed."""
import json, os, re, sys, time, threading, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = "https://ds.nccs.nasa.gov/thredds"
BASE = "AMES/NEX/GDDP-CMIP6"
MODELS = ["ACCESS-CM2", "MPI-ESM1-2-HR", "GFDL-ESM4", "MIROC6", "IITM-ESM"]
POINTS = {"vellode": (11.34, 77.72), "fresno": (36.60, -119.90), "kano": (12.00, 8.52)}
YEARS = list(range(2001, 2056))
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nex_cache.json")
lock = threading.Lock()
cache = json.load(open(OUT)) if os.path.exists(OUT) else {}


def get(url, timeout=180):
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=timeout) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:
            err = e
            time.sleep(3 + 5 * attempt)
    raise err


def refs(path):
    return re.findall(r'catalogRef[^>]*xlink:title="([^"]+)"', get(f"{ROOT}/catalog/{path}/catalog.xml"))


def files(path):
    out = {}
    for u in re.findall(r'urlPath="([^"]+\.nc)"', get(f"{ROOT}/catalog/{path}/catalog.xml")):
        m = re.search(r"_(\d{4})(?:_v[\d.]+)?\.nc$", u)
        if m:
            y = int(m.group(1))
            if y not in out or u > out[y]:  # prefer the highest version suffix
                out[y] = u
    return out


def job(model, var, year, url, pname, lat, lon):
    key = f"{model}|{var}|{year}|{pname}"
    if key in cache:
        return key
    q = f"{ROOT}/ncss/grid/{url}?var={var}&latitude={lat}&longitude={lon}&time_start={year}-01-01T00:00:00Z&time_end={year}-12-31T23:59:59Z&accept=csv"
    txt = get(q)
    s, n = [0.0] * 12, [0] * 12
    for line in txt.splitlines()[1:]:
        p = line.split(",")
        if len(p) < 5:
            continue
        mo = int(p[0][5:7]) - 1
        s[mo] += float(p[-1]); n[mo] += 1
    if min(n) < 25:
        raise RuntimeError(f"short data {key} {n}")
    with lock:
        cache[key] = [s[i] / n[i] for i in range(12)]
    return key


tasks = []
for model in MODELS:
    try:
        member = refs(f"{BASE}/{model}/ssp245")[0]
        for var in ("tas", "pr"):
            fm = {}
            fm.update(files(f"{BASE}/{model}/historical/{member}/{var}"))
            fm.update(files(f"{BASE}/{model}/ssp245/{member}/{var}"))
            for y in YEARS:
                if y not in fm:
                    print("missing", model, var, y, flush=True); continue
                for pname, (lat, lon) in POINTS.items():
                    tasks.append((model, var, y, fm[y], pname, lat, lon))
        print("catalog ok", model, member, flush=True)
    except Exception as e:
        print("catalog FAIL", model, e, flush=True)

todo = [t for t in tasks if f"{t[0]}|{t[1]}|{t[2]}|{t[4]}" not in cache]
print("tasks", len(tasks), "todo", len(todo), flush=True)
done = fail = 0
t0 = time.time()
with ThreadPoolExecutor(8) as ex:
    futs = {ex.submit(job, *t): t for t in todo}
    for f in as_completed(futs):
        try:
            f.result(); done += 1
        except Exception as e:
            fail += 1; print("FAIL", futs[f][:3], futs[f][4], e, flush=True)
        if (done + fail) % 50 == 0:
            with lock:
                json.dump(cache, open(OUT, "w"))
            print(f"{done} done {fail} failed {int(time.time()-t0)}s", flush=True)
with lock:
    json.dump(cache, open(OUT, "w"))
print("FINISHED", done, "done", fail, "failed", int(time.time() - t0), "s", flush=True)
