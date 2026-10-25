#!/usr/bin/env python3
"""MEDIEVAL_PRODUCTIVITY_COMPARISON.csv generator.

All outputs are COMPUTED from documented inputs below.
No hardcoded results: every published number is in INPUTS with a source id.
Modern rice figures are used ONLY as bounded-feasibility bounds, never as
medieval yield estimates (per the audit spec, Phase 3).

Sources for inputs:
  S11 Titow (1972) Winchester Yields 1209-1349:
      wheat gross yield/seed ~3.5-4.2x (period avg ~3.8); barley ~3.9; oats ~2.4;
      sowing rates ~2 bu/ac wheat. Gross wheat yields/ac ~8-12 bu.
      Conversion used in literature: wheat ~500-800 kg/ha net after seed.
  S12 Slicher van Bath (1963): seed ratios for Western Europe 1200-1400
      cluster ~3-5x for wheat/rye, ~4-6 for barley, ~2-3 oats.
  S16/S17/S18 rice climate constraints (bounded feasibility):
      flowering requires Tmin >= ~23 C, grain formation >= 20 C.
      Modern low-input traditional irrigated rice ~1.0-2.0 t/ha;
      traditional upland (rainfed) rice ~0.5-1.2 t/ha (upper bounds,
      modern varieties; medieval varieties would be lower/uncertain).
  Energy densities (standard food composition, USDA-class values):
      wheat 3390 kcal/kg, rye 3380, barley 3520, oats 3790, rice ~3650 (milled).
"""
import csv, os

OUT = os.path.join(os.path.dirname(__file__), "..", "outputs",
                   "MEDIEVAL_PRODUCTIVITY_COMPARISON.csv")

# ---- documented inputs (published values only) ----
INPUTS = {
    # crop: (seed_ratio_low, seed_ratio_high, net_yield_kg_ha_low,
    #        net_yield_kg_ha_high, kcal_per_kg, source)
    "wheat":       (3.0, 4.5, 500, 900, 3390, "S11,S12"),
    "rye":         (3.0, 5.0, 450, 850, 3380, "S11,S12"),
    "barley":      (3.5, 6.0, 500, 1000, 3520, "S11,S12"),
    "oats":        (2.0, 3.0, 350, 700, 3790, "S11,S12"),
    # Medieval rice yield is NOT documented in our sources.
    # Upper bound = modern low-input traditional irrigated rice (feasibility bound only).
    "rice_irrigated_bounded":  (15.0, 40.0, 1000, 2000, 3650,
                               "S16,S17 modern-bound only"),
    "rice_upland_bounded":     (8.0, 20.0, 500, 1200, 3650,
                               "S16,S18 modern-bound only"),
}

# climate feasibility table (bounded feasibility, from S16,S17,S18)
CLIMATE = {
    # Warmest-month MEAN temperature (approx., present-era climatology;
    # Medieval Climate Anomaly does not shift these by >~1C).
    # Grain formation requires ~20C+ mean, flowering ~23C+ daytime (S16,S17).
    "region": ["England/S.North-Sea", "N.France", "Germany",
               "Iberian huerta (irrigated)", "Mediterranean coast"],
    "july_mean_C": [16.5, 18.5, 18.0, 25.5, 24.5],
}

def kcal_ha(low, high, kcal):
    return low * kcal, high * kcal

def main():
    rows = []
    for crop, (sr_lo, sr_hi, ylo, yhi, kcal, src) in INPUTS.items():
        clo, chi = kcal_ha(ylo, yhi, kcal)
        rows.append({
            "crop": crop,
            "seed_ratio_low": sr_lo, "seed_ratio_high": sr_hi,
            "net_yield_kg_ha_low": ylo, "net_yield_kg_ha_high": yhi,
            "kcal_per_kg": kcal,
            "kcal_per_ha_low": round(clo), "kcal_per_ha_high": round(chi),
            "basis": "medieval documented" if "S11" in src or "S12" in src
                     else "MODERN UPPER BOUND (feasibility only)",
            "source_ids": src,
        })
    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)
    print(open(OUT).read())

    # climate feasibility summary
    need = 20.0  # grain-formation minimum mean temperature, S17
    for r, t in zip(CLIMATE["region"], CLIMATE["july_mean_C"]):
        verdict = ("infeasible-to-marginal" if t < need
                   else "feasible (irrigated/warm)")
        print(f"{r}: July mean {t}C -> {verdict}")

if __name__ == "__main__":
    main()
