from uuid import uuid4


class PaymentService:
    @staticmethod
    def create_provider_order(provider: str, amount_paise: int) -> dict:
        provider = provider.lower()
        if provider not in {'razorpay', 'paytm'}:
            raise ValueError('Unsupported payment provider')
        return {
            'provider': provider,
            'order_id': f'{provider}_order_{uuid4().hex[:12]}',
            'amount_paise': amount_paise,
            'currency': 'INR',
        }

    @staticmethod
    def verify_signature(provider: str, payload: dict, signature: str | None) -> bool:
        # Replace with actual HMAC signature validation for production provider SDKs
        return bool(signature and payload and provider)
