class InsuranceError(Exception):
    """Base exception for insurance system"""
    pass

class RiskAssessmentError(InsuranceError):
    """Raised when risk assessment fails"""
    pass

class BlockchainError(InsuranceError):
    """Raised when blockchain operations fail"""
    pass

class PolicyError(InsuranceError):
    """Raised when policy operations fail"""
    pass

class ClaimError(InsuranceError):
    """Raised when claim operations fail"""
    pass

class ValidationError(InsuranceError):
    """Raised when data validation fails"""
    pass

class DatabaseError(InsuranceError):
    """Raised when database operations fail"""
    pass 