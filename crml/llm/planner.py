import json
from loguru import logger
from crml.llm.client import OllamaClient
from crml.llm.prompts import SYSTEM_PROMPT, build_user_prompt


class TaskPlanner:
    def __init__(self, client: OllamaClient):
        self._client = client

    async def plan(self, robot_id: str, goal: str, context: dict) -> dict:
        user_prompt = build_user_prompt(robot_id, goal, context)
        logger.info("Planning task for robot={} goal='{}'", robot_id, goal)

        raw = await self._client.chat(SYSTEM_PROMPT, user_prompt)

        try:
            result = json.loads(raw)
            logger.info("Plan for robot={}: action={} confidence={}",
                        robot_id, result.get("action"), result.get("confidence"))
            return result
        except json.JSONDecodeError:
            logger.warning("LLM returned non-JSON response: {}", raw[:200])
            return {"error": "invalid_response", "raw": raw}
