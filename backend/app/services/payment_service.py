import time
from dataclasses import dataclass

from app.core.config import settings
from app.schemas.payment import CreatePaymentRequest, PaymentOrderResponse


@dataclass
class PaymentService:
    """Business logic for payment orchestration."""

    def create_order(self, payload: CreatePaymentRequest) -> PaymentOrderResponse:
        if payload.method == "cod":
            return self._build_cod_order(payload.amount, payload.currency)
        return self._build_razorpay_order(payload.amount, payload.currency, payload.receipt)

    def _build_razorpay_order(self, amount: int, currency: str, receipt: str | None) -> PaymentOrderResponse:
        # Placeholder for Razorpay test-mode integration.
        # In the next step, replace synthetic id creation with Razorpay API call.
        generated_order_id = f"order_test_{int(time.time())}"

        return PaymentOrderResponse(
            provider="razorpay",
            order_id=generated_order_id,
            amount=amount,
            currency=currency.upper(),
            key_id=settings.razorpay_key_id,
            notes={"receipt": receipt or "bds-receipt"},
        )

    def _build_cod_order(self, amount: int, currency: str) -> PaymentOrderResponse:
        generated_order_id = f"cod_{int(time.time())}"
        return PaymentOrderResponse(
            provider="cod",
            order_id=generated_order_id,
            amount=amount,
            currency=currency.upper(),
            key_id=None,
            notes={"instruction": "Collect payment on delivery"},
        )
