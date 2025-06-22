from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from ..core.payment_service import CryptoPaymentService
from ..utils.auth import get_current_user
from ..core.database import get_db
from ..core.models import User

router = APIRouter()

class CreateCryptoPaymentRequest(BaseModel):
    amount_usd: float

class VerifyCryptoPaymentRequest(BaseModel):
    payment_id: str
    tx_hash: str

@router.post("/crypto/create-payment")
async def create_crypto_payment(
    request: CreateCryptoPaymentRequest,
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    crypto_service = CryptoPaymentService()
    eth_price = crypto_service.get_eth_usd_price()
    amount_eth = request.amount_usd / eth_price
    
    payment_request = crypto_service.create_payment_request(
        current_user.id,
        round(amount_eth, 6)  # Round to 6 decimal places
    )
    
    return {
        **payment_request,
        "eth_usd_price": eth_price,
        "amount_usd": request.amount_usd
    }

@router.post("/crypto/verify-payment")
async def verify_crypto_payment(
    request: VerifyCryptoPaymentRequest,
    current_user: User = Depends(get_current_user)
):
    crypto_service = CryptoPaymentService()
    result = crypto_service.verify_payment(request.payment_id, request.tx_hash)
    
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    
    return {"status": "success", "message": "Payment verified successfully"}