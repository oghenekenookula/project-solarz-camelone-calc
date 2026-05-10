def apply_losses(energy_kwh: float, loss_factor: float, safety_factor: float) -> float:
    return energy_kwh * loss_factor * safety_factor
