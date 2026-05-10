from app.models.schemas import CalculationRequest, CalculationResponse, DataSourceInfo
from app.services.losses import apply_losses


def run_sizing(
    req: CalculationRequest,
    peak_sun_hours: float,
    data_sources: list[DataSourceInfo],
    notes: list[str],
) -> CalculationResponse:
    effective_energy = apply_losses(req.daily_energy_kwh, req.loss_factor, req.safety_factor)

    pv_size_kwp = effective_energy / max(peak_sun_hours * req.panel_efficiency, 0.1)
    battery_capacity_kwh = (req.daily_energy_kwh * req.autonomy_days) / req.depth_of_discharge
    inverter_kw = req.peak_load_kw * 1.25
    charge_controller_amps = (pv_size_kwp * 1000) / req.system_voltage * 1.25

    return CalculationResponse(
        pv_size_kwp=round(pv_size_kwp, 2),
        battery_capacity_kwh=round(battery_capacity_kwh, 2),
        inverter_kw=round(inverter_kw, 2),
        charge_controller_amps=round(charge_controller_amps, 2),
        peak_sun_hours=round(peak_sun_hours, 2),
        data_sources=data_sources,
        notes=notes,
    )
