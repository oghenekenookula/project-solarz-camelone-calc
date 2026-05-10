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

## Current Status
Documentation and planning phase. No production code yet.

## Next Steps
1. Finalize data integration specification (PVGIS and NREL endpoints).
2. Build a standalone calculation engine prototype.
3. Validate against 2-3 real-world systems.
4. Design the initial database schema.

## License
TBD
