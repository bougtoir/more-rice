"""Post-merge public-main verification: fresh anonymous clone, ledger-checked raw inputs, full re-run, comparison."""
import csv, hashlib, io, json, os, re, shutil, subprocess, sys, zipfile, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW = os.path.join(ROOT, "modern_rice", "data", "raw")
FIN = os.path.join(ROOT, "outputs", "modern_rice", "ema", "finished")
WORK = os.path.expanduser(os.environ.get("POSTMERGE_DIR", "~/repro_postmerge"))
URL = "https://github.com/bougtoir/more-rice.git"
SCRIPTS = ["ag_grid_gates", "ag_germany_decomposition", "ema_threshold_sweep", "ema_figures", "ema_reports", "rpg_validation", "rpg_reports",
           "ema_known_answer_tests", "rpg_known_answer_tests", "build_ema_manuscript"]

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()

def git(*a, cwd=WORK): return subprocess.run(["git", *a], cwd=cwd, capture_output=True, check=True).stdout

# raw inputs vs ledgers
checked, bad = [], []
LEDGER = os.path.join(ROOT, "modern_rice", "data", "RAW_ACQUISITION_LEDGER_2026-11-08.csv")
for r in csv.DictReader(open(LEDGER)):
    f, s = (r.get("file") or "").strip(), (r.get("sha256") or "").strip()
    if not re.fullmatch(r"[0-9a-f]{64}", s): continue
    p = os.path.join(ROOT, f) if f.startswith("modern_rice/") else os.path.join(RAW, f.split("raw/", 1)[-1])
    (checked if os.path.exists(p) and sha(p) == s else bad).append(f)
for line in open(os.path.join(RAW, "rpg", "LEDGER.txt")):
    t = line.split()
    if len(t) >= 4 and t[0].endswith(".geojson"):
        p = os.path.join(RAW, "rpg", t[0]); (checked if os.path.exists(p) and sha(p) == t[3] else bad).append("rpg/" + t[0])

if os.path.exists(WORK):
    origin = subprocess.run(["git", "config", "--get", "remote.origin.url"], cwd=WORK, capture_output=True, text=True).stdout.strip()
    if origin.removesuffix(".git") != URL.removesuffix(".git") or os.path.realpath(WORK) == os.path.realpath(ROOT):
        sys.exit(f"{WORK} exists and is not a previous verification clone of {URL}; set POSTMERGE_DIR to a new path")
    shutil.rmtree(WORK)
subprocess.run(["git", "clone", "-q", URL, WORK], check=True, env={**os.environ, "GIT_TERMINAL_PROMPT": "0"})
commit = git("rev-parse", "HEAD").decode().strip(); subject = git("log", "-1", "--format=%s").decode().strip()
os.symlink(RAW, os.path.join(WORK, "modern_rice", "data", "raw"))
runs = []
for s in SCRIPTS:
    p = subprocess.run([sys.executable, f"modern_rice/scripts/{s}.py"], cwd=WORK, capture_output=True, text=True)
    runs.append(f"{s}={p.returncode}")
changed = [l[3:] for l in git("status", "--porcelain").decode().splitlines() if l.startswith(" M")]

def docx_parts(b):
    z = zipfile.ZipFile(io.BytesIO(b))
    return re.sub(r'w:rsid\w*="[^"]*"', "", z.read("word/document.xml").decode()), sorted(hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if n.startswith("word/media"))

def pdftext(b):
    return subprocess.run(["pdftotext", "-", "-"], input=b, capture_output=True).stdout

data_changed, sem, md = [], [], []
for f in changed:
    old, new = git("show", "HEAD:" + f), open(os.path.join(WORK, f), "rb").read()
    if f.endswith((".csv", ".json", ".png")): data_changed.append(f)
    elif f.endswith(".docx"): sem.append((f, "document.xml + media identical" if docx_parts(old) == docx_parts(new) else "DIFFERS"))
    elif f.endswith(".pdf"): sem.append((f, "extracted text identical" if pdftext(old) == pdftext(new) else "DIFFERS"))
    else: md.append(f)
kat = {}
for n, p in (("ema", "outputs/modern_rice/ema/KNOWN_ANSWER_TESTS_FINAL.csv"), ("rpg", "outputs/modern_rice/ema/rpg/RPG_KNOWN_ANSWER_TESTS.csv")):
    fp = os.path.join(WORK, p)
    if os.path.exists(fp):
        rows = list(csv.DictReader(open(fp))); col = next(c for c in rows[0] if c.lower() in ("result", "status", "pass"))
        kat[n] = f"{sum(str(r[col]).upper() in ('PASS', 'TRUE') for r in rows)}/{len(rows)}"
tracked = git("ls-files").decode().splitlines()
ok = (not bad and all(r.endswith("=0") for r in runs) and not data_changed and all(v != "DIFFERS" for _, v in sem)
      and not any(t.endswith(".geojson") for t in tracked))
R = {"repository": URL.removesuffix(".git"), "verified_commit": commit, "commit_subject": subject,
     "verified_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
     "clone_method": "fresh anonymous HTTPS clone (GIT_TERMINAL_PROMPT=0)",
     "raw_inputs": f"durable local store linked into the clone; {len(checked)} of {len(checked) + len(bad)} SHA-256 rows in the tracked ledgers (RAW_ACQUISITION_LEDGER_2026-11-08.csv + rpg/LEDGER.txt) matched, {len(bad)} mismatched/missing",
     "raw_mismatches": bad, "scripts": runs, "canonical_csv_json_png_changed": data_changed, "semantic_checks": sem,
     "prose_reports_regenerated": md, "tests": kat, "tracked_geojson": sum(t.endswith(".geojson") for t in tracked),
     "status": "PASS" if ok else "FAIL"}
json.dump(R, open(os.path.join(FIN, "POSTMERGE_PUBLIC_MAIN_RESULT.json"), "w"), indent=1)
print(json.dumps({k: R[k] for k in ("verified_commit", "status", "raw_inputs", "canonical_csv_json_png_changed", "prose_reports_regenerated", "tests")}, indent=1))
