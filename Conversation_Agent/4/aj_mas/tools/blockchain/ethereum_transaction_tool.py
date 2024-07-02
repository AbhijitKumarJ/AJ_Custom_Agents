from ..base_tool import BaseTool
from aj_mas.utils import logger
from web3 import Web3

class EthereumTransactionTool(BaseTool):
    def __init__(self, provider_url):
        super().__init__("Ethereum Transaction", "Send Ethereum transactions")
        self.w3 = Web3(Web3.HTTPProvider(provider_url))

    def execute(self, from_address: str, to_address: str, amount: float, private_key: str):
        logger.log(f"Executing Ethereum Transaction Tool")
        try:
            nonce = self.w3.eth.get_transaction_count(from_address)
            gas_price = self.w3.eth.gas_price
            value = self.w3.to_wei(amount, 'ether')
            
            transaction = {
                'nonce': nonce,
                'to': to_address,
                'value': value,
                'gas': 21000,
                'gasPrice': gas_price
            }
            
            signed_txn = self.w3.eth.account.sign_transaction(transaction, private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            return {
                'transaction_hash': tx_hash.hex(),
                'from': from_address,
                'to': to_address,
                'amount': amount
            }
        except Exception as e:
            return f"Error in Ethereum transaction: {str(e)}"