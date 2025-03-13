from web3 import Web3
import json

class SmartContract:
    def __init__(self, contract_address, abi_path):
        self.w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
        self.contract_address = contract_address
        with open(abi_path) as f:
            self.contract_abi = json.load(f)
        self.contract = self.w3.eth.contract(
            address=self.contract_address,
            abi=self.contract_abi
        )
    
    def create_insurance_contract(self, user_address, policy_details):
        """
        Create new insurance contract on blockchain
        """
        tx_hash = self.contract.functions.createPolicy(
            user_address,
            policy_details['coverage_amount'],
            policy_details['premium'],
            policy_details['duration']
        ).transact()
        return self.w3.eth.wait_for_transaction_receipt(tx_hash)
    
    def process_claim(self, claim_id, claim_data):
        """
        Process insurance claim through smart contract
        """
        tx_hash = self.contract.functions.processClaim(
            claim_id,
            claim_data['amount'],
            claim_data['evidence_hash']
        ).transact()
        return self.w3.eth.wait_for_transaction_receipt(tx_hash) 