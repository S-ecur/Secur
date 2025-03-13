from pydantic import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = "postgresql://user:password@localhost/insurance_db"
    
    # Blockchain settings
    BLOCKCHAIN_NODE_URL: str = "http://localhost:8545"
    CONTRACT_ADDRESS: str = ""
    CONTRACT_ABI_PATH: str = "contracts/Insurance.json"
    
    # AI Model settings
    MODEL_PATH: str = "models/risk_assessment_model.joblib"
    MODEL_VERSION: str = "1.0.0"
    
    # API settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = False
    
    # Security settings
    SECRET_KEY: str = "your-secret-key"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # IPFS settings
    IPFS_HOST: str = "localhost"
    IPFS_PORT: int = 5001
    
    class Config:
        env_file = ".env"

settings = Settings() 