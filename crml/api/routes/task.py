from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

router = APIRouter()


class TaskRequest(BaseModel):
    goal: str
    context: dict = {}


class TaskResponse(BaseModel):
    robot_id: str
    goal: str
    reasoning: str = ""
    action: str = ""
    parameters: dict = {}
    confidence: float = 0.0
    error: str = ""


@router.post("/task/{robot_id}", response_model=TaskResponse)
async def plan_task(robot_id: str, body: TaskRequest, request: Request):
    planner = request.app.state.planner
    if planner is None:
        raise HTTPException(status_code=503, detail="Task planner not available")

    result = await planner.plan(robot_id, body.goal, body.context)

    if "error" in result:
        return TaskResponse(robot_id=robot_id, goal=body.goal, error=result["error"])

    return TaskResponse(
        robot_id=robot_id,
        goal=body.goal,
        reasoning=result.get("reasoning", ""),
        action=result.get("action", ""),
        parameters=result.get("parameters", {}),
        confidence=result.get("confidence", 0.0),
    )
