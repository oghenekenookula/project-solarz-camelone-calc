from fastapi import FastAPI, HTTPException

from app.models.schemas import CalculationRequest, CalculationResponse
from app.services.calculation import run_sizing
from app.services.solar_data import get_solar_inputs

app = FastAPI(title="Solarz Off-Grid Calculator API", version="0.1.0")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/calculate", response_model=CalculationResponse)
def calculate(req: CalculationRequest) -> CalculationResponse:
    try:
        solar_inputs = get_solar_inputs(req.latitude, req.longitude, req.use_mock)
        return run_sizing(
            req,
            peak_sun_hours=solar_inputs.peak_sun_hours,
            data_sources=solar_inputs.data_sources,
            notes=solar_inputs.notes,
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))
