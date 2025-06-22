from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..core.payment_service import PaymentService
from ..utils.auth import get_current_user

router = APIRouter()

class VerifyPaymentRequest(BaseModel):
    provider: str
    payment_id: str

@router.post("/payment/verify")
async def verify_payment(
    request: VerifyPaymentRequest,
    user: User = Depends(get_current_user)
):
    try:
        payment_service = PaymentService()
        
        # Handle payment verification based on provider
        if request.provider == "stripe":
            payment_service.verify_stripe_payment(request.payment_id)
        elif request.provider == "paystack":
            payment_service.verify_paystack_payment(request.payment_id)
        elif request.provider == "paypal":
            payment_service.verify_paypal_payment(request.payment_id)
        elif request.provider == "crypto":
            payment_service.verify_crypto_payment(request.payment_id)
        else:
            raise HTTPException(status_code=400, detail="Invalid payment provider")
        
        return {"status": "success", "message": "Payment verified"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))