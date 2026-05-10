# Phase 1 Implementation Plan

## Objectives
- Establish core calculation engine.
- Integrate authoritative solar data sources.
- Deliver MVP for West Africa.

## Deliverables
- FastAPI backend with calculation endpoint.
- PVGIS data integration with fallback mock data.
- West Africa location data baseline.
- Documented data integration spec.

## Workstreams and Tasks

### 1) Calculation Engine
- Define input model and validation rules.
- Implement PV sizing, battery sizing, inverter sizing, charge controller sizing.
- Implement loss modeling with configurable factors.
- Add basic unit tests for calculations (phase 1.2).

### 2) Data Integration
- PVGIS TMY endpoint integration.
- NREL PVWatts spec documentation and placeholder for API key use.
- Provenance metadata returned with every calculation.
- Caching strategy definition for high-traffic locations.

### 3) MVP West Africa
- Baseline country list and metadata file.
- Default regional factors (heat, dust) for West Africa.
- MVP acceptance criteria and validation checklist.

## Acceptance Criteria
- /calculate returns PV, battery, inverter, controller sizes.
- Data source provenance is included in responses.
- Mock mode works for offline development.
- West Africa country list is included in the repo.

## Timeline (Suggested)
- Week 1: Models, calculation engine, mock data.
- Week 2: PVGIS integration, data spec, provenance.
- Week 3: Validation pass and MVP demo.

## Risks
- Data endpoints change or rate limit.
- Missing or inconsistent irradiance data.
- User input quality varies.

## Mitigations
- Include multi-source fallback and caching.
- Validate inputs with clear error messages.
- Maintain a data quality checklist.
