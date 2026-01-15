# Sahel Region Threat Index (SRTI)

RSS-first OSINT pipeline for Mali, Niger, and Burkina Faso. It produces a static
site by precomputing scores and embeddings (no client-side fetching).

## Local run
```bash
python "Sahel Region Threat Index (SRTI)/sahel_watch.py"
python "Sahel Region Threat Index (SRTI)/coup_detector.py"
python generate_pages.py
```

## Outputs
- `data/srti_latest.json`: current score, components, weights, sources, forecast.
- `data/srti_history.json`: hourly history for charting and trends.
- `data/srti_coup_alert.json`: simplified coup alert summary.
- `Sahel Region Threat Index (SRTI)/sahel_data.csv`: event log (trimmed to last 2000 rows).
- `Sahel Region Threat Index (SRTI)/index.html`: static site output.

## GitHub Actions
The workflow in `.github/workflows/srti_hourly.yml` runs hourly, updates data,
regenerates the static page, and commits the results.
