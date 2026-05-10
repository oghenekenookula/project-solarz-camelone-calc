from app.models.schemas import CalculationRequest
from app.services.calculation import run_sizing
from app.models.schemas import DataSourceInfo


def test_run_sizing_basic() -> None:
    req = CalculationRequest(
        country="Ghana",
        latitude=5.6,
        longitude=-0.2,
        daily_energy_kwh=10,
        autonomy_days=2,
        depth_of_discharge=0.8,
        peak_load_kw=2,
        system_voltage=48,
        panel_efficiency=0.2,
        loss_factor=1.2,
        safety_factor=1.1,
        use_mock=True,
    )

    sources = [
        DataSourceInfo(
            name="PVGIS (mock)",
            url="https://re.jrc.ec.europa.eu/api/v5_2",
            retrieved_at="2026-05-10T00:00:00Z",
        )
    ]
    response = run_sizing(
        req,
        peak_sun_hours=5.0,
        confidence_score=0.9,
        data_sources=sources,
        notes=[],
    )

    assert response.pv_size_kwp > 0
    assert response.battery_capacity_kwh == 25.0
    assert response.inverter_kw == 2.5
    assert response.charge_controller_amps > 0
    assert response.temperature_derate_factor < 1.0
    assert response.confidence_score == 0.9
