from web3 import Web3
from dotenv import load_dotenv
import os
import json

# add your blockchain connection information
load_dotenv()
Provider_url = os.getenv('INFURA_URL')
web3 = Web3(Web3.HTTPProvider(Provider_url))
# Smart contract ERC20 ABI
with open('ERC20Abi.json', 'r') as abi_file:
    abi = json.load(abi_file)

if web3.is_connected():
    print("Connecté à Ethereum")


def main():
    latest_block_number = 0
    while True:
        block_number = web3.eth.block_number
        if block_number != latest_block_number:
            latest_block_number = block_number
            # Find transactions in this block
            block = web3.eth.get_block(latest_block_number, full_transactions=True)
            transactions = block['transactions']
            print("Nombre de transactions dans le bloc", latest_block_number, ":", len(transactions))
            # Process transaction data
            for tx in transactions:
                to_address = tx['to']
                # It's smart contract
                if to_address is None or to_address == "0x0":
                    info_transac = web3.eth.get_transaction_receipt(tx.hash.hex())
                    address = info_transac['contractAddress']
                    contract = web3.eth.contract(address=address, abi=abi)
                    try:
                        name = contract.functions.name().call()
                        symbol = contract.functions.symbol().call()
                        total_supply = contract.functions.totalSupply().call()
                        print(
                            f"{address} - Ce contract est ERC20\n"
                            f"Nom du contract: {name}\n"
                            f"Symbole: {symbol}\n"
                            f"Total Supply: {total_supply}"
                        )
                    except:
                        print(f"{address} - Ce contrat n'est pas un ERC20")
            latest_block_number = block_number


if __name__ == '__main__':
    main()
