import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from crml.llm.client import OllamaClient
from crml.llm.planner import TaskPlanner
from crml.llm.prompts import build_user_prompt, SYSTEM_PROMPT


def test_build_user_prompt():
    prompt = build_user_prompt("rover", "find the cup", {"objects": ["cup"]})
    assert "rover" in prompt
    assert "find the cup" in prompt
    assert "cup" in prompt


def test_system_prompt_contains_actions():
    for action in ("move", "rotate", "stop", "wait"):
        assert action in SYSTEM_PROMPT


@pytest.mark.asyncio
async def test_planner_returns_action():
    mock_client = AsyncMock(spec=OllamaClient)
    mock_client.chat.return_value = json.dumps({
        "reasoning": "move toward the cup",
        "action": "move",
        "parameters": {"direction": "forward", "distance": 0.5},
        "confidence": 0.9,
    })
    planner = TaskPlanner(mock_client)
    result = await planner.plan("rover", "find the cup", {"objects": ["cup"]})
    assert result["action"] == "move"
    assert result["confidence"] == 0.9


@pytest.mark.asyncio
async def test_planner_handles_invalid_json():
    mock_client = AsyncMock(spec=OllamaClient)
    mock_client.chat.return_value = "Sorry, I cannot help with that."
    planner = TaskPlanner(mock_client)
    result = await planner.plan("rover", "find the cup", {})
    assert result["error"] == "invalid_response"
    assert "raw" in result


@pytest.mark.asyncio
async def test_ollama_client_availability_check():
    client = OllamaClient("localhost", 11434, "llama3.1:8b")
    with patch("httpx.AsyncClient") as mock_http:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_http.return_value.__aenter__.return_value.get = AsyncMock(return_value=mock_response)
        assert await client.is_available() is True


@pytest.mark.asyncio
async def test_ollama_client_unavailable():
    import httpx
    client = OllamaClient("nonexistent-host", 11434, "llama3.1:8b")
    result = await client.is_available()
    assert result is False


def test_task_endpoint_no_planner(client):
    # Simulate planner being None (Ollama unavailable)
    from crml.api.app import app
    app.state.planner = None
    r = client.post("/task/rover", json={"goal": "find the cup", "context": {}})
    assert r.status_code == 503


@pytest.mark.asyncio
async def test_task_endpoint_with_planner(client):
    mock_planner = AsyncMock()
    mock_planner.plan.return_value = {
        "reasoning": "move forward",
        "action": "move",
        "parameters": {"direction": "forward", "distance": 1.0},
        "confidence": 0.85,
    }
    from crml.api.app import app
    app.state.planner = mock_planner
    r = client.post("/task/rover", json={"goal": "go forward", "context": {"battery": 90}})
    assert r.status_code == 200
    data = r.json()
    assert data["action"] == "move"
    assert data["robot_id"] == "rover"
    assert data["confidence"] == 0.85
