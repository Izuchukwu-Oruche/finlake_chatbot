from typing import Dict, Any, Tuple
from config import PROMPTS

def fulfill_balance(user_id: str, slots: Dict[str,Any]) -> Tuple[bool, str]:
    # TODO: call your internal balance API using user_id/phone mapping
    # Return English text; we'll localize for the user
    mock_amount = "50,000"
    return True, PROMPTS["en"]["balance"].format(amount=mock_amount)

def fulfill_transfer(user_id: str, slots: Dict[str,Any]) -> Tuple[bool, str]:
    # TODO: call your internal transfer API with {amount, account_number}
    # Here we simulate success
    return True, "Transfer successful."