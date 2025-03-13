from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()

class PolicyStatus(enum.Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    CANCELLED = "cancelled"

class ClaimStatus(enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    PROCESSING = "processing"

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    wallet_address = Column(String(42), unique=True, nullable=False)
    age = Column(Integer)
    credit_score = Column(Integer)
    occupation = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    policies = relationship("Policy", back_populates="user")
    risk_assessments = relationship("RiskAssessment", back_populates="user")

class Policy(Base):
    __tablename__ = 'policies'
    
    id = Column(Integer, primary_key=True)
    policy_id = Column(String(100), unique=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    coverage_amount = Column(Float)
    premium = Column(Float)
    status = Column(Enum(PolicyStatus))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    contract_address = Column(String(42))
    
    user = relationship("User", back_populates="policies")
    claims = relationship("Claim", back_populates="policy")

class Claim(Base):
    __tablename__ = 'claims'
    
    id = Column(Integer, primary_key=True)
    claim_id = Column(String(100), unique=True)
    policy_id = Column(Integer, ForeignKey('policies.id'))
    amount = Column(Float)
    status = Column(Enum(ClaimStatus))
    evidence_hash = Column(String(66))  # IPFS hash
    created_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime)
    
    policy = relationship("Policy", back_populates="claims")

class RiskAssessment(Base):
    __tablename__ = 'risk_assessments'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    risk_score = Column(Float)
    risk_factors = Column(String(500))  # JSON string
    assessment_date = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="risk_assessments") 