# Data Integration Specification

## Overview
Phase 1 integrates PVGIS for baseline solar resource data with NREL PVWatts as a fallback when PVGIS data is unavailable. NREL requests require an API key.

## PVGIS Integration
**Base URL:** https://re.jrc.ec.europa.eu/api/v5_2

**Endpoint:** /tmy

**Request Parameters**
- lat: float
- lon: float
- outputformat: json

**Response Fields (used)**
- outputs.tmy_monthly[].month
- outputs.tmy_monthly[].G(h)
- outputs.tmy_hourly[].G(h) (fallback)

**Derived Values**
- Peak Sun Hours (PSH) = monthly GHI / days in month

**Provenance Fields**
- data_sources.name = "PVGIS"
- data_sources.url = request URL
- data_sources.retrieved_at = UTC timestamp
- data_sources.notes = "TMY monthly irradiance"

## NREL PVWatts
**Base URL:** https://developer.nrel.gov

**Endpoint:** /api/pvwatts/v6.json

**Request Parameters**
- api_key: string
- lat, lon
- system_capacity
- module_type
- losses

**Response Fields**
- outputs.solrad_monthly

**Derived Values**
- Peak Sun Hours (PSH) = average of solrad_monthly

**Provenance Fields**
- data_sources.name = "NREL PVWatts"
- data_sources.url = request URL
- data_sources.retrieved_at = UTC timestamp
- data_sources.notes = "Monthly average daily solar radiation"

## Caching Strategy
- Cache PVGIS responses by lat/lon grid (0.1 degree).
- Cache lifetime: 30 days for baseline data.
- Store provenance records in database.

## Data Quality Checks
- Validate GHI values are positive.
- Flag missing months.
- If data is invalid, return mock data and include fallback note.
