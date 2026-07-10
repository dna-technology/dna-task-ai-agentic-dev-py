import time
from typing import Any, Dict, Optional

from src.data.tools_data import CUSTOMER_HISTORY, DEFAULT_CUSTOMER_HISTORY, USER_BALANCES, refunded_transactions
from src.enums import ShippingStatus


async def check_ledger_balance(user_id: str) -> Dict[str, Any]:
    time.sleep(0.4)
    return {"userId": user_id, "availableCents": USER_BALANCES.get(user_id, 0)}


async def verify_shipping(tracking_number: Optional[str]) -> Dict[str, Any]:
    time.sleep(0.5)

    if not tracking_number:
        return {"delivered": False, "carrierStatus": ShippingStatus.NO_TRACKING_NUMBER}

    if "DELIVERED" in tracking_number:
        return {"trackingNumber": tracking_number, "delivered": True, "carrierStatus": ShippingStatus.DELIVERED}

    return {"trackingNumber": tracking_number, "delivered": False, "carrierStatus": ShippingStatus.IN_TRANSIT}


async def get_customer_history(user_id: str) -> Dict[str, Any]:
    time.sleep(0.3)

    user_history = CUSTOMER_HISTORY.get(user_id, DEFAULT_CUSTOMER_HISTORY)

    return {"userId": user_id, **user_history}


async def execute_refund(user_id: str, amount_cents: int) -> Dict[str, Any]:
    time.sleep(0.5)

    refund = {"refundId": f"refund_{int(time.time() * 1000)}", "userId": user_id, "amountCents": amount_cents}

    refunded_transactions.append(refund)

    return refund
