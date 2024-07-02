from ..base_tool import BaseTool
from aj_mas.utils import logger
from web3 import Web3

class SmartContractInteractionTool(BaseTool):
    def __init__(self, provider_url):
        super().__init__("Smart Contract Interaction", "Interact with Ethereum smart contracts")
        self.w3 = Web3(Web3.HTTPProvider(provider_url))

    def execute(self, contract_address: str, contract_abi: list, function_name: str, function_params: list):
        logger.log(f"Executing Smart Contract Interaction Tool")
        try:
            contract = self.w3.eth.contract(address=contract_address, abi=contract_abi)
            function = getattr(contract.functions, function_name)
            result = function(*function_params).call()
            
            return {
                'contract_address': contract_address,
                'function_name': function_name,
                'result': result
            }
        except Exception as e:
            return f"Error in smart contract interaction: {str(e)}"