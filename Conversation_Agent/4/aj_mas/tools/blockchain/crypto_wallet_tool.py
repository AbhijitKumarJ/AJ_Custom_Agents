from ..base_tool import BaseTool
from utils.logger import logger
from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes

class CryptoWalletTool(BaseTool):
    def __init__(self):
        super().__init__("Crypto Wallet", "Generate and manage cryptocurrency wallets")

    def execute(self, action: str, params: dict):
        logger.log(f"Executing Crypto Wallet Tool")
        try:
            if action == "generate_wallet":
                return self._generate_wallet(params.get('mnemonic'))
            elif action == "derive_address":
                return self._derive_address(params['mnemonic'], params['coin'], params['account'], params['address_index'])
            else:
                return f"Unsupported action: {action}"
        except Exception as e:
            return f"Error in crypto wallet operation: {str(e)}"

    def _generate_wallet(self, mnemonic=None):
        if mnemonic is None:
            mnemonic = Bip39SeedGenerator().Generate(12)
        seed_bytes = Bip39SeedGenerator(mnemonic).Generate()
        return {
            'mnemonic': mnemonic,
            'seed': seed_bytes.hex()
        }

    def _derive_address(self, mnemonic, coin, account, address_index):
        seed_bytes = Bip39SeedGenerator(mnemonic).Generate()
        if coin == "BTC":
            bip44_mst_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)
        elif coin == "ETH":
            bip44_mst_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.ETHEREUM)
        else:
            raise ValueError(f"Unsupported coin: {coin}")

        bip44_acc_ctx = bip44_mst_ctx.Purpose().Coin().Account(account)
        bip44_chg_ctx = bip44_acc_ctx.Change(Bip44Changes.CHAIN_EXT)
        bip44_addr_ctx = bip44_chg_ctx.AddressIndex(address_index)

        return {
            'address': bip44_addr_ctx.PublicKey().ToAddress(),
            'private_key': bip44_addr_ctx.PrivateKey().Raw().ToHex()
        }