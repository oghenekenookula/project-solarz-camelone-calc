from unittest.mock import patch

from app.services.solar_data import (
    _parse_nrel_psh,
    _parse_pvgis_hourly_psh,
    _parse_pvgis_monthly_psh,
    get_solar_inputs,
)


def test_parse_pvgis_monthly_psh() -> None:
    monthly = [
        {"month": 1, "G(h)": 150},
        {"month": 2, "G(h)": 140},
        {"month": 3, "G(h)": 160},
    ]
    value = _parse_pvgis_monthly_psh(monthly)
    assert value is not None
    assert value > 0


def test_parse_pvgis_hourly_psh() -> None:
    hourly = [{"G(h)": 500}] * 8760
    value = _parse_pvgis_hourly_psh(hourly)
    assert value is not None
    assert round(value, 2) == round((500 * 8760 / 1000) / 365, 2)


def test_parse_nrel_psh() -> None:
    value = _parse_nrel_psh([4.5, 5.0, 5.2, 0, -1])
    assert value == (4.5 + 5.0 + 5.2) / 3


def test_get_solar_inputs_nrel_fallback() -> None:
    class FakeResponse:
        def __init__(self, payload: dict) -> None:
            self._payload = payload

        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict:
            return self._payload

    def fake_requests_get(url: str, params: dict, timeout: int):
        if url.endswith("/tmy"):
            return FakeResponse({"outputs": {}})
        return FakeResponse({"outputs": {"solrad_monthly": [5.1] * 12}})

    with patch("app.services.solar_data.get_settings") as mock_settings:
        mock_settings.return_value.solar_use_mock = False
        mock_settings.return_value.pvgis_base_url = "https://re.jrc.ec.europa.eu/api/v5_2"
        mock_settings.return_value.nrel_base_url = "https://developer.nrel.gov"
        mock_settings.return_value.nrel_api_key = "demo-key"

        with patch("app.services.solar_data.requests.get", side_effect=fake_requests_get):
            result = get_solar_inputs(5.6, -0.2, use_mock=False)

    assert result.peak_sun_hours == 5.1
    assert result.data_sources[0].name == "NREL PVWatts"
    assert result.confidence_score == 0.75
