import json

from fastapi.testclient import TestClient

from src.app import app, get_planner


class MockPlanner:
    def __init__(self, decision: dict) -> None:
        self.decision = decision

    async def decide(self, prompt: str) -> str:
        return json.dumps(self.decision)


def test_returns_the_starter_disputes():
    # GIVEN
    mock_planner = MockPlanner({"action": "deny_refund", "reason": "not used"})
    app.dependency_overrides[get_planner] = lambda: mock_planner
    client = TestClient(app)

    # WHEN
    response = client.get("/api/disputes")
    app.dependency_overrides = {}

    # THEN
    disputes = response.json()["disputes"]

    assert response.status_code == 200
    assert len(disputes) == 3
    assert disputes["disp_1001"]["id"] == "disp_1001"
    assert disputes["disp_1001"]["merchant"] == "Northstar Camera"


def test_runs_investigation_endpoint_with_mocked_planner():
    # GIVEN
    mock_planner = MockPlanner({"action": "deny_refund", "reason": "Carrier shows delivered"})
    app.dependency_overrides[get_planner] = lambda: mock_planner
    client = TestClient(app)

    # WHEN
    response = client.post("/api/disputes/disp_1001/investigate")
    app.dependency_overrides = {}

    # THEN
    result = response.json()

    assert response.status_code == 200
    assert result == {"status": "denied", "disputeId": "disp_1001", "reason": "Carrier shows delivered"}


def test_investigation_endpoint_returns_404_for_nonexistent_dispute():
    # GIVEN
    mock_planner = MockPlanner({"action": "deny_refund", "reason": "not used"})
    app.dependency_overrides[get_planner] = lambda: mock_planner
    client = TestClient(app)

    # WHEN
    response = client.post("/api/disputes/nonexistent/investigate")
    app.dependency_overrides = {}

    # THEN
    result = response.json()

    assert response.status_code == 404
    assert result["message"] == "Dispute ID nonexistent not found"
