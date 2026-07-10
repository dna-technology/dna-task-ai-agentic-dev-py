from src.enums import DisputeStatus

disputes = {
    "disp_1001": {
        "id": "disp_1001",
        "userId": "user_123",
        "amountCents": 12999,
        "merchant": "Northstar Camera",
        "reason": "Item not received. Merchant says it shipped, but I never got it.",
        "trackingNumber": "TRACK-DELIVERED-1",
        "status": DisputeStatus.NEW
    },
    "disp_1002": {
        "id": "disp_1002",
        "userId": "user_456",
        "amountCents": 4590,
        "merchant": "Metro Coffee Supply",
        "reason": "Duplicate charge after checkout timed out.",
        "status": DisputeStatus.NEW
    },
    "disp_1003": {
        "id": "disp_1003",
        "userId": "user_789",
        "amountCents": 22250,
        "merchant": "Trailhead Gear",
        "reason": "Fraudulent charge. I do not recognize this merchant.",
        "trackingNumber": "TRACK-IN-TRANSIT-9",
        "status": DisputeStatus.NEW
    }
}