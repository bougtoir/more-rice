# Reproduction Commands & SHA
Baseline public main: 6f1fe122178f6d6e73d3ee52fc566f2998369f41
Clean clone: git clone https://github.com/bougtoir/more-rice && cd more-rice
Environment: python>=3.10, numpy, pandas, matplotlib, rasterio, python-docx (requirements.txt)
Re-fetch: python3 modern_rice/scripts/fetch_nasa_power.py (NASA POWER daily API; other raws per data/ACQUISITION_LEDGER.csv URLs)
Regenerate: python3 modern_rice/scripts/upland_water_balance.py ; suitability_pilot.py ; gates14.py ; risk_portfolio.py ; crop_comparison.py
Perturbation check: TAW 100->60 re-run changes all downstream metrics (verified).
