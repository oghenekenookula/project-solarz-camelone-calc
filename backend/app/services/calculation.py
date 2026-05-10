from app.models.schemas import CalculationRequest, CalculationResponse, DataSourceInfo
from app.services.losses import apply_losses


def _temperature_derate_factor(ambient_temp_c: float, temp_coeff_per_c: float) -> float:
    delta = max(ambient_temp_c - 25.0, 0.0)
    factor = 1.0 + (temp_coeff_per_c * delta)
    return max(min(factor, 1.0), 0.5)


def _hybrid_generator_kw(daily_energy_kwh: float, peak_load_kw: float) -> float:
    avg_kw = daily_energy_kwh / 24.0
    return max(peak_load_kw * 1.1, avg_kw * 1.25)


def run_sizing(
    req: CalculationRequest,
    peak_sun_hours: float,
    confidence_score: float,
    data_sources: list[DataSourceInfo],
    notes: list[str],
) -> CalculationResponse:
    effective_energy = apply_losses(req.daily_energy_kwh, req.loss_factor, req.safety_factor)
    temp_derate_factor = _temperature_derate_factor(req.ambient_temp_c, req.temp_coeff_per_c)
    panel_efficiency = req.panel_efficiency * temp_derate_factor

    if temp_derate_factor < 1.0:
        notes = notes + [
            f"Temperature derating applied (factor={temp_derate_factor:.2f})"
        ]

    pv_size_kwp = effective_energy / max(peak_sun_hours * panel_efficiency, 0.1)
    battery_capacity_kwh = (req.daily_energy_kwh * req.autonomy_days) / req.depth_of_discharge
    inverter_kw = req.peak_load_kw * 1.25
    generator_kw = (
        round(_hybrid_generator_kw(req.daily_energy_kwh, req.peak_load_kw), 2)
        if req.enable_hybrid_generator
        else None
    )
    charge_controller_amps = (pv_size_kwp * 1000) / req.system_voltage * 1.25

    return CalculationResponse(
        pv_size_kwp=round(pv_size_kwp, 2),
        battery_capacity_kwh=round(battery_capacity_kwh, 2),
        inverter_kw=round(inverter_kw, 2),
        generator_kw=generator_kw,
        charge_controller_amps=round(charge_controller_amps, 2),
        peak_sun_hours=round(peak_sun_hours, 2),
        temperature_derate_factor=round(temp_derate_factor, 3),
        confidence_score=round(confidence_score, 2),
        data_sources=data_sources,
        notes=notes,
    )
