from web3 import Web3
import asyncio
from datetime import datetime

class BlockchainEventManager:
    def __init__(self, smart_contract):
        self.contract = smart_contract.contract
        self.w3 = smart_contract.w3
        
    async def monitor_events(self):
        """
        Monitor blockchain events
        """
        policy_filter = self.contract.events.PolicyCreated.create_filter(fromBlock='latest')
        claim_filter = self.contract.events.ClaimProcessed.create_filter(fromBlock='latest')
        
        while True:
            for event in policy_filter.get_new_entries():
                await self._handle_policy_event(event)
            
            for event in claim_filter.get_new_entries():
                await self._handle_claim_event(event)
                
            await asyncio.sleep(10)
    
    async def _handle_policy_event(self, event):
        """
        Handle new policy creation events
        """
        event_data = {
            'policy_id': event.args.policyId,
            'user_address': event.args.userAddress,
            'coverage_amount': event.args.coverageAmount,
            'timestamp': datetime.fromtimestamp(event.args.timestamp),
            'transaction_hash': event.transactionHash.hex()
        }
        # Process event data (e.g., store in database)
        return event_data
    
    async def _handle_claim_event(self, event):
        """
        Handle claim processing events
        """
        event_data = {
            'claim_id': event.args.claimId,
            'policy_id': event.args.policyId,
            'amount': event.args.amount,
            'status': event.args.status,
            'timestamp': datetime.fromtimestamp(event.args.timestamp)
        }
        # Process event data (e.g., store in database)
        return event_data 