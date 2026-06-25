from fastapi import FastAPI, Request
from pydantic import BaseModel
from crml import __version__
from crml.api.routes import inference, models

app = FastAPI(title="CRML", version=__version__, docs_url="/docs")

app.include_router(inference.router)
app.include_router(models.router)


class HealthResponse(BaseModel):
    status: str
    version: str
    mqtt_connected: bool


@app.get("/health", response_model=HealthResponse)
async def health(request: Request):
    bridge = request.app.state.bridge
    return HealthResponse(
        status="ok",
        version=__version__,
        mqtt_connected=bridge.is_connected,
    )
