from dataclasses import dataclass
from datetime import datetime, timezone
import calendar
import requests

from app.core.settings import get_settings
from app.models.schemas import DataSourceInfo


@dataclass(frozen=True)
class SolarInputs:
    peak_sun_hours: float
    data_sources: list[DataSourceInfo]
    notes: list[str]


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _mock_solar_inputs() -> SolarInputs:
    data_sources = [
        DataSourceInfo(
            name="PVGIS (mock)",
            url="https://re.jrc.ec.europa.eu/api/v5_2",
            retrieved_at=_utc_now(),
            notes="Mock data for offline development",
        )
    ]
    return SolarInputs(peak_sun_hours=5.2, data_sources=data_sources, notes=["Mock data used"])


def _parse_pvgis_monthly_psh(monthly: list[dict]) -> float | None:
    daily_psh = []
    for entry in monthly:
        try:
            month = int(entry.get("month", 0))
            ghi = float(entry.get("G(h)", 0))
            if month < 1 or month > 12 or ghi <= 0:
                continue
            days = calendar.monthrange(2026, month)[1]
            daily_psh.append(ghi / days)
        except (ValueError, TypeError):
            continue
    if not daily_psh:
        return None
    return sum(daily_psh) / len(daily_psh)


def _parse_pvgis_hourly_psh(hourly: list[dict]) -> float | None:
    total_ghi_wh = 0.0
    samples = 0
    for entry in hourly:
        try:
            ghi = float(entry.get("G(h)", 0))
            if ghi <= 0:
                continue
            total_ghi_wh += ghi
            samples += 1
        except (ValueError, TypeError):
            continue
    if samples == 0:
        return None
    annual_kwh = total_ghi_wh / 1000.0
    return annual_kwh / 365.0


def _parse_nrel_psh(solrad_monthly: list[float]) -> float | None:
    clean = [value for value in solrad_monthly if isinstance(value, (int, float)) and value > 0]
    if not clean:
        return None
    return sum(clean) / len(clean)


def _fetch_nrel_psh(lat: float, lon: float) -> SolarInputs | None:
    settings = get_settings()
    if not settings.nrel_api_key:
        return None

    url = f"{settings.nrel_base_url}/api/pvwatts/v6.json"
    response = requests.get(
        url,
        params={
            "api_key": settings.nrel_api_key,
            "lat": lat,
            "lon": lon,
            "system_capacity": 1,
            "module_type": 1,
            "losses": 14,
        },
        timeout=20,
    )
    response.raise_for_status()
    payload = response.json()
    solrad_monthly = payload.get("outputs", {}).get("solrad_monthly", [])
    peak_sun_hours = _parse_nrel_psh(solrad_monthly)
    if peak_sun_hours is None:
        raise ValueError("NREL response missing solrad_monthly")

    data_sources = [
        DataSourceInfo(
            name="NREL PVWatts",
            url=url,
            retrieved_at=_utc_now(),
            notes="Monthly average daily solar radiation",
        )
    ]
    return SolarInputs(
        peak_sun_hours=peak_sun_hours,
        data_sources=data_sources,
        notes=[],
    )


def get_solar_inputs(lat: float, lon: float, use_mock: bool) -> SolarInputs:
    settings = get_settings()
    if use_mock or settings.solar_use_mock:
        return _mock_solar_inputs()

    url = f"{settings.pvgis_base_url}/tmy"
    try:
        response = requests.get(
            url,
            params={"lat": lat, "lon": lon, "outputformat": "json"},
            timeout=15,
        )
        response.raise_for_status()
        payload = response.json()
        outputs = payload.get("outputs", {})
        monthly = outputs.get("tmy_monthly", [])
        peak_sun_hours = _parse_pvgis_monthly_psh(monthly)
        source_note = "TMY monthly irradiance"

        if peak_sun_hours is None:
            hourly = outputs.get("tmy_hourly", [])
            peak_sun_hours = _parse_pvgis_hourly_psh(hourly)
            source_note = "TMY hourly irradiance"

        if peak_sun_hours is None:
            raise ValueError("PVGIS response missing monthly and hourly irradiance")

        data_sources = [
            DataSourceInfo(
                name="PVGIS",
                url=url,
                retrieved_at=_utc_now(),
                notes=source_note,
            )
        ]
        return SolarInputs(
            peak_sun_hours=peak_sun_hours,
            data_sources=data_sources,
            notes=[],
        )
    except Exception as exc:
        notes = [f"PVGIS fallback used: {exc}"]
        try:
            nrel_inputs = _fetch_nrel_psh(lat, lon)
            if nrel_inputs is not None:
                nrel_inputs.notes.extend(notes)
                nrel_inputs.notes.append("NREL used as fallback")
                return nrel_inputs
        except Exception as nrel_exc:
            notes.append(f"NREL fallback failed: {nrel_exc}")

        fallback = _mock_solar_inputs()
        fallback.notes.extend(notes)
        return fallback
