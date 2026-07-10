from typing import Optional
from pydantic import BaseModel
from src.enums import DisputeStatus


class Dispute(BaseModel):
    id: str
    userId: str
    amountCents: int
    merchant: str
    reason: str
    trackingNumber: Optional[str] = None
    note: Optional[str] = None
    status: DisputeStatus


class HealthResponse(BaseModel):
    ok: bool


class DisputesResponse(BaseModel):
    disputes: list[Dispute]


class ErrorResponse(BaseModel):
    status: str = "error"
    message: str
