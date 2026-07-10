import json
from typing import Any, Dict


def build_investigation_prompt(input_data: Dict[str, Any]) -> str:
    note = input_data.get("note", "")
    dispute = input_data["dispute"]
    ledger = input_data["ledger"]
    shipping = input_data["shipping"]
    history = input_data["history"]

    return f"""You are a helpful refund investigation assistant.
Look at this dispute and decide if the customer should get their money back.
Return a JSON object. Always provide key 'action', with thing that should be performed.

Dispute:
{json.dumps(dispute, indent=2)}

Note:
{note}

Ledger:
{json.dumps(ledger, indent=2)}

Shipping:
{json.dumps(shipping, indent=2)}

Customer history:
{json.dumps(history, indent=2)}"""
