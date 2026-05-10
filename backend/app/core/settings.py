from dataclasses import dataclass
import os


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y"}


@dataclass(frozen=True)
class Settings:
    solar_use_mock: bool
    pvgis_base_url: str
    nrel_base_url: str
    nrel_api_key: str | None


def get_settings() -> Settings:
    return Settings(
        solar_use_mock=_env_bool("SOLAR_USE_MOCK", True),
        pvgis_base_url=os.getenv("PVGIS_BASE_URL", "https://re.jrc.ec.europa.eu/api/v5_2"),
        nrel_base_url=os.getenv("NREL_BASE_URL", "https://developer.nrel.gov"),
        nrel_api_key=os.getenv("NREL_API_KEY") or None,
    )
