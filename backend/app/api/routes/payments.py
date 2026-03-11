from fastapi import APIRouter

from app.schemas.payment import CreatePaymentRequest, PaymentOrderResponse
from app.services.payment_service import PaymentService

router = APIRouter(prefix="/payments", tags=["payments"])
service = PaymentService()


@router.post("/order", response_model=PaymentOrderResponse)
def create_payment_order(payload: CreatePaymentRequest) -> PaymentOrderResponse:
    return service.create_order(payload)
