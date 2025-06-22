from web3 import Web3
import json
from datetime import datetime
from ..config import settings
from ..core.database import SessionLocal
from ..core.models import Payment, Subscription
from ..utils.logging import logger
import time

class CryptoPaymentService:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(settings.ETHEREUM_NODE_URL))
        self.contract = self.w3.eth.contract(
            address=settings.ETH_CONTRACT_ADDRESS,
            abi=self._load_contract_abi()
        )
        
    def _load_contract_abi(self):
        with open("crypto_payment_abi.json") as f:
            return json.load(f)
    
    def create_payment_request(self, user_id: int, amount_eth: float):
        """Create a unique payment request for MetaMask"""
        payment_id = f"crypto_{int(time.time())}_{user_id}"
        
        db = SessionLocal()
        try:
            # Create pending payment record
            payment = Payment(
                user_id=user_id,
                amount=amount_eth,
                currency="ETH",
                provider="metamask",
                payment_id=payment_id,
                status="pending"
            )
            db.add(payment)
            db.commit()
            
            return {
                "payment_id": payment_id,
                "amount_eth": amount_eth,
                "wallet_address": settings.ETH_RECEIVING_ADDRESS
            }
        finally:
            db.close()
    
    def verify_payment(self, payment_id: str, tx_hash: str):
        """Verify blockchain transaction"""
        db = SessionLocal()
        try:
            payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()
            if not payment:
                return {"status": "error", "message": "Payment not found"}
            
            if payment.status == "completed":
                return {"status": "success", "message": "Payment already verified"}
            
            # Get transaction receipt
            tx_receipt = self.w3.eth.get_transaction_receipt(tx_hash)
            if not tx_receipt or tx_receipt.status != 1:
                return {"status": "error", "message": "Transaction failed"}
            
            # Get transaction details
            tx = self.w3.eth.get_transaction(tx_hash)
            
            # Verify payment details
            amount_wei = self.w3.toWei(payment.amount, 'ether')
            if tx.value != amount_wei:
                return {"status": "error", "message": "Amount mismatch"}
            
            if tx.to.lower() != settings.ETH_RECEIVING_ADDRESS.lower():
                return {"status": "error", "message": "Recipient mismatch"}
            
            # Update payment status
            payment.status = "completed"
            payment.transaction_hash = tx_hash
            payment.completed_at = datetime.utcnow()
            db.commit()
            
            # Activate subscription
            subscription = db.query(Subscription).filter(
                Subscription.user_id == payment.user_id
            ).first()
            if subscription:
                subscription.status = "active"
                subscription.period_end = datetime.utcnow() + timedelta(days=30)
                db.commit()
            
            return {"status": "success", "message": "Payment verified"}
        except Exception as e:
            logger.error(f"Payment verification failed: {str(e)}")
            return {"status": "error", "message": str(e)}
        finally:
            db.close()
    
    def get_eth_usd_price(self):
        """Get current ETH/USD price from CoinGecko"""
        try:
            response = requests.get(
                "https://api.coingecko.com/api/v3/simple/price",
                params={"ids": "ethereum", "vs_currencies": "usd"}
            )
            return response.json()["ethereum"]["usd"]
        except Exception as e:
            logger.error(f"Failed to get ETH price: {str(e)}")
            return 3000  # Fallback price
