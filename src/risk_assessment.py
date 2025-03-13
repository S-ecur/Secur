from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import numpy as np
import joblib

class RiskAssessment:
    def __init__(self):
        self.model = RandomForestClassifier()
        self.scaler = StandardScaler()
        
    def train_model(self, training_data, labels):
        """
        Train the risk assessment model
        """
        features = np.array([self._extract_features(data) for data in training_data])
        features_scaled = self.scaler.fit_transform(features)
        self.model.fit(features_scaled, labels)
        
    def analyze_user_risk(self, user_data):
        """
        Analyze user risk based on provided data
        """
        features = self._extract_features(user_data)
        features_scaled = self.scaler.transform([features])
        risk_score = self.model.predict_proba(features_scaled)[0][1]
        
        risk_factors = self._analyze_risk_factors(user_data)
        return {
            'risk_score': risk_score,
            'risk_factors': risk_factors
        }
    
    def _extract_features(self, user_data):
        """
        Extract relevant features from user data
        """
        features = [
            user_data.get('age', 0),
            user_data.get('claim_history', 0),
            user_data.get('risk_factors', 0),
            user_data.get('coverage_amount', 0),
            user_data.get('income', 0),
            user_data.get('credit_score', 0),
            user_data.get('occupation_risk', 0),
            user_data.get('health_score', 0)
        ]
        return features
        
    def _analyze_risk_factors(self, user_data):
        """
        Analyze specific risk factors
        """
        risk_factors = []
        
        if user_data.get('age', 0) > 60:
            risk_factors.append('Age Risk')
        if user_data.get('claim_history', 0) > 2:
            risk_factors.append('High Claim History')
        if user_data.get('credit_score', 0) < 650:
            risk_factors.append('Low Credit Score')
            
        return risk_factors
        
    def save_model(self, path):
        """
        Save trained model to file
        """
        joblib.dump({
            'model': self.model,
            'scaler': self.scaler
        }, path)
        
    def load_model(self, path):
        """
        Load trained model from file
        """
        saved_model = joblib.load(path)
        self.model = saved_model['model']
        self.scaler = saved_model['scaler'] 