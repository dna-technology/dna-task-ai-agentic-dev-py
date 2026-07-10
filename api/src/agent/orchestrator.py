import json
import time
from typing import Any, Dict

from src.agent.gemini_planner import GeminiPlanner
from src.agent.prompt import build_investigation_prompt
from src.enums import DisputeStatus
from src.logger import LOGGER
from src.models import Dispute
from src.tools import check_ledger_balance, execute_refund, get_customer_history, verify_shipping


async def investigate_dispute(dispute: Dispute, planner: GeminiPlanner) -> Dict[str, Any]:
    dispute["status"] = DisputeStatus.INVESTIGATING.value

    ledger = await check_ledger_balance(dispute["userId"])
    shipping = await verify_shipping(dispute.get("trackingNumber"))
    history = await get_customer_history(dispute["userId"])

    prompt = build_investigation_prompt({"dispute": dispute, "ledger": ledger, "shipping": shipping, "history": history})

    # big workload simulation
    time.sleep(15.0)
    decision_text = await planner.decide(prompt)
    decision = json.loads(decision_text)

    if decision.get("action") == "approve_refund":
        LOGGER.info("refunding")
        refund = await execute_refund(decision["userId"], decision["amountCents"])
        dispute["status"] = DisputeStatus.APPROVED.value

        return {
            "status": "approved",
            "disputeId": dispute["id"],
            "refundId": refund["refundId"],
            "reason": decision["reason"],
        }

    dispute["status"] = DisputeStatus.DENIED.value

    return {
        "status": dispute["status"],
        "disputeId": dispute["id"],
        "reason": decision["reason"],
    }
