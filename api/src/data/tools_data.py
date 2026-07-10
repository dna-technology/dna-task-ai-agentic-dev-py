"""
Static data used by the tools module.
"""
from typing import Any, Dict, List

# User balance data for ledger checks
USER_BALANCES: Dict[str, int] = {
    "user_123": 18000,
    "user_456": 9000,
    "user_789": 25000
}

# Customer history data
CUSTOMER_HISTORY: Dict[str, Dict[str, int]] = {
    "user_123": {"disputesLast90Days": 1, "accountAgeDays": 420},
    "user_456": {"disputesLast90Days": 3, "accountAgeDays": 38},
    "user_789": {"disputesLast90Days": 0, "accountAgeDays": 870},
}

# Default customer history for unknown users
DEFAULT_CUSTOMER_HISTORY: Dict[str, int] = {
    "disputesLast90Days": 0,
    "accountAgeDays": 1
}

# Global list to track refunded transactions
refunded_transactions: List[Dict[str, Any]] = []