import json

SYSTEM_PROMPT = """You are a robot task planner for a home robotics system.
Given a robot's current sensor context and a goal, decide the single next action the robot should take.

Available actions:
- move: drive the robot (parameters: direction [forward/backward], distance [meters])
- rotate: turn the robot (parameters: direction [clockwise/counterclockwise], angle [degrees])
- stop: halt all movement (parameters: {})
- wait: pause and observe (parameters: {})

Rules:
- Respond ONLY with valid JSON, no other text.
- Be conservative — prefer small movements and confirm position before large actions.
- If the goal is already achieved, use stop.

Response format:
{
  "reasoning": "brief explanation of why this action",
  "action": "action_name",
  "parameters": {},
  "confidence": 0.0
}"""


def build_user_prompt(robot_id: str, goal: str, context: dict) -> str:
    return (
        f"Robot: {robot_id}\n"
        f"Goal: {goal}\n"
        f"Current context: {json.dumps(context, indent=2)}"
    )
