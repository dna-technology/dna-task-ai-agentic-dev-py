import pytest
from src.tools import check_ledger_balance, get_customer_history, verify_shipping


@pytest.mark.asyncio
async def test_returns_ledger_shipping_and_customer_history_data():

    ledger_result = await check_ledger_balance("user_123")
    assert ledger_result == {
        "userId": "user_123",
        "availableCents": 18000
    }

    shipping_result = await verify_shipping("TRACK-DELIVERED-1")
    assert shipping_result == {
        "trackingNumber": "TRACK-DELIVERED-1",
        "delivered": True,
        "carrierStatus": "DELIVERED"
    }

    history_result = await get_customer_history("user_123")
    assert history_result == {
        "userId": "user_123",
        "disputesLast90Days": 1,
        "accountAgeDays": 420
    }
