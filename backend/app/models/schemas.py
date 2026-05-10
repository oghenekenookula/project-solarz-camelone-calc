from pydantic import BaseModel, Field


class CalculationRequest(BaseModel):
    country: str = Field(..., description="Target country")
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    daily_energy_kwh: float = Field(..., gt=0)
    autonomy_days: int = Field(3, ge=1, le=14)
    depth_of_discharge: float = Field(0.8, gt=0, le=1)
    peak_load_kw: float = Field(1.0, gt=0)
    system_voltage: int = Field(48, ge=12, le=120)
    panel_efficiency: float = Field(0.18, gt=0, le=1)
    loss_factor: float = Field(1.3, gt=1)
    safety_factor: float = Field(1.1, gt=1)
    tilt_deg: float = Field(10, ge=0, le=90)
    azimuth_deg: float = Field(180, ge=0, le=360)
    ambient_temp_c: float = Field(35, ge=-20, le=60)
    temp_coeff_per_c: float = Field(-0.004, ge=-0.01, le=0)
    enable_hybrid_generator: bool = Field(False)
    use_mock: bool = Field(True, description="Use mock solar data for offline runs")


class DataSourceInfo(BaseModel):
    name: str
    url: str
    retrieved_at: str
    notes: str | None = None


class CalculationResponse(BaseModel):
    pv_size_kwp: float
    battery_capacity_kwh: float
    inverter_kw: float
    generator_kw: float | None
    charge_controller_amps: float
    peak_sun_hours: float
    temperature_derate_factor: float
    confidence_score: float
    data_sources: list[DataSourceInfo]
    notes: list[str]
