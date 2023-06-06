import os
import random

from xrpl.transaction import safe_sign_and_autofill_transaction, send_reliable_submission
from xrpl.models.transactions.nftoken_mint import NFTokenMint
from xrpl.utils import str_to_hex, hex_to_str
from xrpl.wallet import generate_faucet_wallet, Wallet
from xrpl.models.requests import AccountNFTs
from xrpl.clients import JsonRpcClient

TESTNET_RPC_URL = "https://s.altnet.rippletest.net:51234/"
xrp_client = JsonRpcClient(TESTNET_RPC_URL)
address = os.environ.get("XRPL_ADDRESS")
seed = os.environ.get("XRPL_SECRET")

issuer_wallet = Wallet(seed,address)

def mint_nft(uri):
    mint_tx = NFTokenMint(
        account=issuer_wallet.classic_address,
        nftoken_taxon=random.randint(1, 1000000000),
        uri=str_to_hex(uri)
    )

    mint_tx_signed = safe_sign_and_autofill_transaction(transaction=mint_tx, wallet=issuer_wallet, client=xrp_client)
    mint_tx_result = send_reliable_submission(transaction=mint_tx_signed, client=xrp_client).result

    return mint_tx_result

def get_owned_nfts(marker=None):
    # limit cannot be lower than 20.
    # marker is the last nft['NFTokenID'] from the previous request.
    get_account_nfts = xrp_client.request(AccountNFTs(account=issuer_wallet.classic_address, marker=marker))
    return get_account_nfts.result['account_nfts']

# Example usage
if __name__ == "__main__":
    pass
    # nft_uri = "https://example.com/nft"
    # mint_result = mint_nft(nft_uri)
    # nft_uri = "https://example.com/nfts/1"
    # mint_result = mint_nft(nft_uri)
    # print(f"Minted NFT: {mint_result['hash']}")
    # mint_result = mint_nft(nft_uri)
    # print(f"Minted NFT: {mint_result['hash']}")
    # nft_uri = "https://example.com/nft"
    # mint_result = mint_nft(nft_uri)
    # nft_uri = "https://example.com/nfts/1"
    # mint_result = mint_nft(nft_uri)
    # print(f"Minted NFT: {mint_result['hash']}")
    # mint_result = mint_nft(nft_uri)
    # print(f"Minted NFT: {mint_result['hash']}")
    # # Get the owned NFTs
