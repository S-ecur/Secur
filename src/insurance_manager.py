from .risk_assessment import RiskAssessment
from .blockchain_contract import SmartContract
from .models import User, Policy, Claim, PolicyStatus, ClaimStatus, RiskAssessment as RiskAssessmentModel
from .database import get_db_session
from .exceptions import PolicyError, ClaimError, ValidationError
from .logger import setup_logger
from datetime import datetime, timedelta
import json

logger = setup_logger("insurance_manager")

class InsuranceManager:
    def __init__(self, contract_address, abi_path):
        self.risk_assessor = RiskAssessment()
        self.smart_contract = SmartContract(contract_address, abi_path)
        
    def process_insurance_application(self, user_data):
        try:
            logger.info(f"Processing insurance application for user: {user_data['wallet_address']}")
            
            with get_db_session() as db:
                # Create or get user
                user = self._get_or_create_user(db, user_data)
                
                # Perform risk assessment
                risk_result = self.risk_assessor.analyze_user_risk(user_data)
                premium = self._calculate_premium(risk_result['risk_score'], user_data)
                
                # Store risk assessment
                risk_assessment = RiskAssessmentModel(
                    user_id=user.id,
                    risk_score=risk_result['risk_score'],
                    risk_factors=json.dumps(risk_result['risk_factors'])
                )
                db.add(risk_assessment)
                
                # Create blockchain contract
                policy_details = self._create_policy_details(user_data, premium)
                contract_result = self.smart_contract.create_insurance_contract(
                    user_data['wallet_address'],
                    policy_details
                )
                
                # Store policy
                policy = self._create_policy(db, user, contract_result, user_data, premium)
                
                logger.info(f"Successfully created policy {policy.policy_id}")
                return self._format_policy_response(policy, risk_result)
                
        except Exception as e:
            logger.error(f"Error processing insurance application: {str(e)}")
            raise PolicyError(f"Failed to process insurance application: {str(e)}")
    
    def submit_claim(self, claim_data):
        try:
            logger.info(f"Processing claim for policy: {claim_data['policy_id']}")
            
            with get_db_session() as db:
                # Validate policy
                policy = self._validate_policy_for_claim(db, claim_data)
                
                # Process claim on blockchain
                claim_result = self.smart_contract.process_claim(
                    claim_data['claim_id'],
                    claim_data
                )
                
                # Store claim
                claim = Claim(
                    claim_id=claim_data['claim_id'],
                    policy_id=policy.id,
                    amount=claim_data['amount'],
                    status=ClaimStatus.PROCESSING,
                    evidence_hash=claim_data['evidence_hash'],
                    created_at=datetime.utcnow()
                )
                db.add(claim)
                db.commit()
                
                logger.info(f"Successfully submitted claim {claim.claim_id}")
                return self._format_claim_response(claim, claim_result)
                
        except Exception as e:
            logger.error(f"Error processing claim: {str(e)}")
            raise ClaimError(f"Failed to process claim: {str(e)}")
    
    def get_policy_details(self, policy_id: str):
        try:
            with get_db_session() as db:
                policy = db.query(Policy).filter_by(policy_id=policy_id).first()
                if not policy:
                    raise PolicyError("Policy not found")
                return self._format_policy_response(policy)
        except Exception as e:
            logger.error(f"Error fetching policy details: {str(e)}")
            raise PolicyError(f"Failed to fetch policy details: {str(e)}")
    
    def get_user_policies(self, wallet_address: str):
        try:
            with get_db_session() as db:
                user = db.query(User).filter_by(wallet_address=wallet_address).first()
                if not user:
                    return []
                return [self._format_policy_response(policy) for policy in user.policies]
        except Exception as e:
            logger.error(f"Error fetching user policies: {str(e)}")
            raise PolicyError(f"Failed to fetch user policies: {str(e)}")
    
    def get_claim_status(self, claim_id: str):
        try:
            with get_db_session() as db:
                claim = db.query(Claim).filter_by(claim_id=claim_id).first()
                if not claim:
                    raise ClaimError("Claim not found")
                return self._format_claim_response(claim)
        except Exception as e:
            logger.error(f"Error fetching claim status: {str(e)}")
            raise ClaimError(f"Failed to fetch claim status: {str(e)}")
    
    # Helper methods
    def _get_or_create_user(self, db, user_data):
        user = db.query(User).filter_by(wallet_address=user_data['wallet_address']).first()
        if not user:
            user = User(
                wallet_address=user_data['wallet_address'],
                age=user_data['age'],
                credit_score=user_data.get('credit_score'),
                occupation=user_data.get('occupation')
            )
            db.add(user)
            db.commit()
        return user
    
    def _create_policy_details(self, user_data, premium):
        return {
            'coverage_amount': user_data['requested_coverage'],
            'premium': premium,
            'duration': user_data['duration']
        }
    
    def _create_policy(self, db, user, contract_result, user_data, premium):
        policy = Policy(
            policy_id=contract_result['policy_id'],
            user_id=user.id,
            coverage_amount=user_data['requested_coverage'],
            premium=premium,
            status=PolicyStatus.ACTIVE,
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow() + timedelta(days=user_data['duration']),
            contract_address=contract_result['contract_address']
        )
        db.add(policy)
        db.commit()
        return policy
    
    def _calculate_premium(self, risk_score, user_data):
        """
        Calculate insurance premium based on risk score and coverage
        """
        base_premium = user_data['requested_coverage'] * 0.01
        risk_multiplier = 1 + risk_score
        return base_premium * risk_multiplier
    
    def _validate_policy_for_claim(self, db, claim_data):
        policy = db.query(Policy).filter_by(policy_id=claim_data['policy_id']).first()
        if not policy:
            raise PolicyError("Policy not found")
        return policy
    
    def _format_policy_response(self, policy, risk_result):
        return {
            'policy_id': policy.policy_id,
            'risk_score': risk_result['risk_score'],
            'premium': policy.premium,
            'contract_address': policy.contract_address
        }
    
    def _format_claim_response(self, claim, claim_result):
        return {
            'claim_id': claim.claim_id,
            'policy_id': claim.policy_id,
            'amount': claim.amount,
            'status': claim.status,
            'evidence_hash': claim.evidence_hash,
            'created_at': claim.created_at,
            'result': claim_result
        } 