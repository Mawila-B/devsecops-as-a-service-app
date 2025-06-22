from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    api_key = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="user")
    created_at = Column(DateTime, default=func.now())
    stripe_customer_id = Column(String)
    
    # Relationships
    subscription = relationship("Subscription", back_populates="user")
    payments = relationship("Payment", back_populates="user")
    scans = relationship("Scan", back_populates="user")

class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    tier = Column(String, default="free")
    status = Column(String, default="active")
    period_start = Column(DateTime, default=func.now())
    period_end = Column(DateTime)
    stripe_subscription_id = Column(String)
    
    # Relationships
    user = relationship("User", back_populates="subscription")

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Integer)  # In cents
    currency = Column(String, default="USD")
    provider = Column(String)
    payment_id = Column(String)
    status = Column(String, default="pending")
    completed_at = Column(DateTime)
    transaction_hash = Column(String)  # For crypto payments
    
    # Relationships
    user = relationship("User", back_populates="payments")

class Scan(Base):
    __tablename__ = "scans"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    target = Column(String)
    scan_type = Column(String)
    status = Column(String, default="queued")
    created_at = Column(DateTime, default=func.now())
    completed_at = Column(DateTime)
    report_path = Column(String)
    error = Column(String)
    
    # Relationships
    user = relationship("User", back_populates="scans")