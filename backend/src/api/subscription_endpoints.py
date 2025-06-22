from fastapi import APIRouter, Depends
from ..utils.auth import get_current_user
from ..core.subscription_service import get_subscription_details

router = APIRouter()

@router.get("/subscription")
async def get_subscription(user: User = Depends(get_current_user)):
    return get_subscription_details(user.id)

@router.post("/subscription/upgrade")
async def upgrade_subscription(
    tier: str,
    user: User = Depends(get_current_user)
):
    # Implementation of upgrade logic
    return {"status": "success", "message": f"Upgraded to {tier} tier"}

@router.post("/subscription/cancel")
async def cancel_subscription(user: User = Depends(get_current_user)):
    # Implementation of cancellation logic
    return {"status": "success", "message": "Subscription cancelled"}