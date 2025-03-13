from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from .insurance_manager import InsuranceManager
from .blockchain_events import BlockchainEventManager

app = FastAPI()
insurance_manager = InsuranceManager(
    contract_address="YOUR_CONTRACT_ADDRESS",
    abi_path="path/to/contract_abi.json"
)

security = HTTPBearer()

class UserData(BaseModel):
    wallet_address: str
    age: int
    claim_history: int
    risk_factors: float
    requested_coverage: float
    duration: int

class ClaimData(BaseModel):
    claim_id: str
    amount: float
    evidence_hash: str
    policy_id: str

class PolicyQuery(BaseModel):
    policy_id: str
    user_address: str

class RiskAssessmentRequest(BaseModel):
    user_data: UserData
    additional_documents: list[str] = []

@app.post("/apply-insurance")
async def apply_insurance(user_data: UserData):
    try:
        result = insurance_manager.process_insurance_application(user_data.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/submit-claim")
async def submit_claim(claim_data: ClaimData):
    try:
        result = insurance_manager.submit_claim(claim_data.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/policy/{policy_id}")
async def get_policy(policy_id: str, credentials: HTTPAuthorizationCredentials = Security(security)):
    try:
        policy = insurance_manager.get_policy_details(policy_id)
        return policy
    except Exception as e:
        raise HTTPException(status_code=404, detail="Policy not found")

@app.get("/user-policies/{user_address}")
async def get_user_policies(user_address: str):
    try:
        policies = insurance_manager.get_user_policies(user_address)
        return policies
    except Exception as e:
        raise HTTPException(status_code=404, detail="No policies found")

@app.post("/risk-assessment")
async def assess_risk(request: RiskAssessmentRequest):
    try:
        risk_assessment = insurance_manager.risk_assessor.analyze_user_risk(request.user_data.dict())
        return risk_assessment
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/claim-status/{claim_id}")
async def get_claim_status(claim_id: str):
    try:
        status = insurance_manager.get_claim_status(claim_id)
        return status
    except Exception as e:
        raise HTTPException(status_code=404, detail="Claim not found") 