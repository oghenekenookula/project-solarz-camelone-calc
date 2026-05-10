# Roadmap - Solar Off-Grid Energy System Calculator

## Phase 1: Foundation and Data Integration (Months 1-3)
**Objectives**
- Establish core calculation engine.
- Integrate authoritative solar data sources.
- Deliver MVP for West Africa.

**Deliverables**
- Calculation engine prototype.
- Data ingestion from PVGIS and NREL PVWatts.
- Location database for 3-5 West African countries.
- Basic reports (system summary, bill of materials).

**Milestones**
1. Define data integration spec and data quality checks.
2. Implement load analysis, PV sizing, battery sizing, and loss modeling.
3. Validate calculations against 2-3 real systems.
4. Publish API contract for calculation endpoint.

## Phase 2: Regional Refinement and Productization (Months 4-6)
**Objectives**
- Improve accuracy with local validation.
- Add advanced configuration options.
- Build user interface and external API.

**Deliverables**
- Temperature derating model for West Africa.
- Multi-day autonomy and hybrid generator sizing.
- Web dashboard and API documentation.
- Data provenance and confidence scores per result.

**Milestones**
1. Partner with regional installers for calibration data.
2. Add inverter partial-load curves and battery types.
3. Implement report export (PDF).

## Phase 3: Regional Expansion (Months 7-9)
**Objectives**
- Extend to North and Southern Africa.
- Add region-specific parameters and standards.

**Deliverables**
- North Africa data integration (RCREEE).
- Southern Africa data integration (SADC RE resources).
- Region-specific tuning and comparisons.

**Milestones**
1. Build region configuration profiles.
2. Validate seasonal adjustments for new regions.

## Phase 4: Optimization and ML Enhancements (Month 10+)
**Objectives**
- Improve prediction accuracy and personalization.
- Add performance monitoring and recommendations.

**Deliverables**
- ML-assisted demand profiling.
- Predictive maintenance signals.
- Optimization recommendations for CAPEX vs reliability.

## Implementation Notes
- Use PostgreSQL + PostGIS for geographic queries.
- Cache high-traffic location queries with Redis.
- Schedule data refreshes with a pipeline tool (Airflow or Prefect).
- Maintain a data provenance record for every dataset and calculation.
