from typing import Literal

from pydantic import BaseModel, Field


PaymentMethod = Literal["razorpay", "cod"]


class CreatePaymentRequest(BaseModel):
    amount: int = Field(gt=0, description="Order amount in smallest currency unit")
    currency: str = Field(default="INR", min_length=3, max_length=3)
    method: PaymentMethod
    receipt: str | None = None


class PaymentOrderResponse(BaseModel):
    provider: PaymentMethod
    order_id: str
    amount: int
    currency: str
    key_id: str | None = None
    notes: dict[str, str] = Field(default_factory=dict)
