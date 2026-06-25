from fastapi import APIRouter
from pydantic import BaseModel
from crml import __version__

router = APIRouter()


class HealthResponse(BaseModel):
    status: str
    version: str
    mqtt_connected: bool


@router.get("/health", response_model=HealthResponse)
async def health(mqtt_connected: bool = False):
    return HealthResponse(
        status="ok",
        version=__version__,
        mqtt_connected=mqtt_connected,
    )
