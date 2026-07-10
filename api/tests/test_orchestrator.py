import json

import pytest

from src.agent.orchestrator import investigate_dispute
from src.enums import DisputeStatus
from src.models import Dispute


class MockPlanner:
    async def decide(self, prompt: str) -> str:
        return json.dumps(
            {
                "action": "approve_refund",
                "userId": "user_789",
                "amountCents": 22250,
                "reason": "Customer history and shipping status support the claim",
            }
        )


@pytest.mark.asyncio
async def test_investigates_dispute_executes_refund_when_planner_approves():
    # GIVEN
    dispute = Dispute(
        id="disp_1003",
        userId="user_789",
        amountCents=22250,
        merchant="Metropolitan Audio",
        reason="Fraudulent charge",
        trackingNumber="TRACK_IN_TRANSIT_1003",
        status=DisputeStatus.NEW,
    )
    planner = MockPlanner()

    # WHEN
    result = await investigate_dispute(dispute, planner)

    # THEN
    assert result["status"] == "approved"
    assert result["disputeId"] == "disp_1003"
    assert result["reason"] == "Customer history and shipping status support the claim"
    assert "refund_" in result["refundId"]
