from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

router = APIRouter()


class InferenceRequest(BaseModel):
    task: str
    data: dict


class InferenceResponse(BaseModel):
    robot_id: str
    task: str
    result: dict


@router.post("/inference/{robot_id}", response_model=InferenceResponse)
async def run_inference(robot_id: str, request_body: InferenceRequest, request: Request):
    registry = request.app.state.registry
    model = registry.load(request_body.task)
    if model is None:
        raise HTTPException(status_code=404, detail=f"No model found for task '{request_body.task}'")

    # Real model forward pass will replace this when models exist
    result = {"status": "ok", "model": request_body.task, "input_keys": list(request_body.data.keys())}
    return InferenceResponse(robot_id=robot_id, task=request_body.task, result=result)
