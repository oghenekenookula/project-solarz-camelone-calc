# Solar Off-Grid Energy System Calculator

Design and size off-grid solar systems based on energy needs and backup time, optimized for West African conditions. The roadmap includes North and Southern Africa expansion.

## Goals
- Accurate sizing with transparent data sources.
- Region-aware adjustments for temperature and seasonality.
- Usable by installers, engineers, and NGOs.

## Key Capabilities (Planned)
- Location-based solar resource assessment.
- PV array, battery, inverter, and charge controller sizing.
- Loss modeling for wiring, conversion, dust, and heat.
- Scenario comparison and report generation.
- Data provenance per calculation result.

## Trusted Data Sources
- PVGIS (EU Commission)
- NREL PVWatts (US NREL)
- NASA MERRA-2
- SOLARGIS (optional premium)
- Regional meteorological agencies

## Documentation
- High-Level Design: [HLD.md](HLD.md)
- Roadmap: [ROADMAP.md](ROADMAP.md)
- Phase 1 Plan: [docs/PHASE1_PLAN.md](docs/PHASE1_PLAN.md)
- Data Integration Spec: [docs/DATA_INTEGRATION_SPEC.md](docs/DATA_INTEGRATION_SPEC.md)

## Current Status
Phase 1 backend scaffold in progress (calculation engine and data integration).

## Backend Quick Start
1. Create a virtual environment.
2. Install dependencies:

```bash
pip install -r backend/requirements.txt
```

3. Run the API:

```bash
uvicorn app.main:app --reload --app-dir backend
```

4. Try a calculation:

```bash
curl -X POST http://127.0.0.1:8000/calculate \
	-H "Content-Type: application/json" \
	-d '{"country":"Ghana","latitude":5.6,"longitude":-0.2,"daily_energy_kwh":8,"autonomy_days":3,"peak_load_kw":2,"use_mock":true}'
```

## Tests
```bash
pytest
```

## Next Steps
1. Finalize data integration specification (PVGIS and NREL endpoints).
2. Build a standalone calculation engine prototype.
3. Validate against 2-3 real-world systems.
4. Design the initial database schema.

## License
TBD
