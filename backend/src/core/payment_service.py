# Add to PaymentService class
def verify_stripe_payment(self, payment_id: str):
    payment_intent = stripe.PaymentIntent.retrieve(payment_id)
    
    if payment_intent.status != 'succeeded':
        raise ValueError("Payment not succeeded")
    
    # Update database
    db = SessionLocal()
    try:
        payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()
        if payment:
            payment.status = "completed"
            payment.completed_at = datetime.utcnow()
            db.commit()
            
            # Activate subscription
            subscription = payment.subscription
            subscription.status = "active"
            db.commit()
    finally:
        db.close()

def verify_paystack_payment(self, payment_id: str):
    url = f"https://api.paystack.co/transaction/verify/{payment_id}"
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    
    if data['data']['status'] != 'success':
        raise ValueError("Payment not successful")
    
    # Update database (similar to stripe method)

def verify_paypal_payment(self, payment_id: str):
    url = f"{settings.PAYPAL_BASE_URL}/v2/checkout/orders/{payment_id}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {self._get_paypal_access_token()}"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    order = response.json()
    
    if order['status'] != 'COMPLETED':
        raise ValueError("Payment not completed")
    
    # Update database (similar to stripe method)