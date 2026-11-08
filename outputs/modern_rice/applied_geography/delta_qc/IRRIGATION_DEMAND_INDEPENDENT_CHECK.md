# Irrigation demand — independent check
Hand calculation (Python Decimal, independent of `ag_danube_demand.py`):
- A = 250,000 ha = 2,500,000,000 m²; D = 1.000 m → V = 2,500,000,000.000 m³
- T = 120 d × 86,400 s = 10,368,000 s
- Q_net = V/T = **241.1265 m³/s** (pipeline: 241 m³/s) ✔
- Q_gross = Q_net/0.75 = **321.5021 m³/s** (pipeline: 321 m³/s) ✔; at 0.60: 401.9 m³/s
- The former ~24 m³/s was a factor-of-ten error (withdrawn).

| Area (ha) | Depth (mm) | Days | Net (m³/s) | Gross @0.75 (m³/s) |
|---|---|---|---|---|
| 100,000 | 800 | 120 | 77.2 | 102.9 |
| 100,000 | 800 | 150 | 61.7 | 82.3 |
| 100,000 | 1000 | 120 | 96.5 | 128.6 |
| 100,000 | 1000 | 150 | 77.2 | 102.9 |
| 100,000 | 1200 | 120 | 115.7 | 154.3 |
| 100,000 | 1200 | 150 | 92.6 | 123.5 |
| 250,000 | 800 | 120 | 192.9 | 257.2 |
| 250,000 | 800 | 150 | 154.3 | 205.8 |
| 250,000 | 1000 | 120 | 241.1 | 321.5 |
| 250,000 | 1000 | 150 | 192.9 | 257.2 |
| 250,000 | 1200 | 120 | 289.4 | 385.8 |
| 250,000 | 1200 | 150 | 231.5 | 308.6 |

## Terms
- *Net field requirement*: seasonal depth D (crop ET + percolation + puddling − effective rain), Bouman et al. (2007) range 800–1,200 mm.
- *Gross abstraction*: net / conveyance-and-application efficiency (0.75 assumed).
- *Consumptive depletion*: evapotranspiration share only; not estimated here. *Return flow*: drainage/percolation partly re-entering the river downstream; not modelled.
- *Environmental flows and other uses*: not quantified; they reduce the allocable fraction of any discharge.
- The rate is a seasonal-average equivalent, not a peak rate.
