from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class InferenceRequest(BaseModel):
    data: dict


class InferenceResponse(BaseModel):
    robot_id: str
    result: dict


@router.post("/inference/{robot_id}", response_model=InferenceResponse)
async def run_inference(robot_id: str, request: InferenceRequest):
    # Step 5 (model registry) will load and run the appropriate model here
    raise HTTPException(status_code=501, detail="Model registry not yet implemented")
