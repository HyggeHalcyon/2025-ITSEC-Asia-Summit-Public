import json
from pathlib import Path

import sandbox
from web3 import Web3

def set_balance(web3: Web3, account_address: str, amount: int):
    res = web3.provider.make_request(
        "anvil_setBalance",
        [account_address, amount]
    )
    print(res)

def deploy_currency_library(web3: Web3, deployer_address: str, deployer_privateKey: str) -> str:
    """Deploy a library and return its address"""
    contract_info = json.loads(Path(f"compiled/Currency.sol/CurrencyLibrary.json").read_text())
    abi = contract_info["abi"]
    bytecode = contract_info["bytecode"]["object"]
    
    contract = web3.eth.contract(abi=abi, bytecode=bytecode)
    
    construct_txn = contract.constructor().build_transaction(
        {
            "from": deployer_address,
            "value": Web3.to_wei(0, 'ether'),
            "nonce": web3.eth.get_transaction_count(deployer_address),
            "gas": 10_000_000,
        }
    )
    
    tx_create = web3.eth.account.sign_transaction(construct_txn, deployer_privateKey)
    tx_hash = web3.eth.send_raw_transaction(tx_create.raw_transaction)
    rcpt = web3.eth.wait_for_transaction_receipt(tx_hash)
    
    return rcpt.contractAddress

def deploy(web3: Web3, deployer_address: str, deployer_privateKey: str, player_address: str) -> str:
    uri = web3.provider.endpoint_uri
    
    lib_address = deploy_currency_library(web3, deployer_address, deployer_privateKey)
    print(f"Deployed CurrencyLibrary at {lib_address}")
    
    # Load the main contract
    contract_info = json.loads(Path("compiled/Setup.sol/Setup.json").read_text())
    abi = contract_info["abi"]
    bytecode = contract_info["bytecode"]["object"]
    
    # Link the libraries in the bytecode
    linked_bytecode = bytecode
    placeholder = f"__$3f635709e851129283446a6d08ad5262c7$__"
    linked_bytecode = linked_bytecode.replace(placeholder, lib_address[2:])  # Remove '0x' prefix
    
    contract = web3.eth.contract(abi=abi, bytecode=linked_bytecode)

    construct_txn = contract.constructor().build_transaction(
        {
            "from": deployer_address,
            "value": Web3.to_wei(0, 'ether'),
            "nonce": web3.eth.get_transaction_count(deployer_address),
            "gas": 10_000_000,
        }
    )

    tx_create = web3.eth.account.sign_transaction(construct_txn, deployer_privateKey)
    tx_hash = web3.eth.send_raw_transaction(tx_create.raw_transaction)

    rcpt = web3.eth.wait_for_transaction_receipt(tx_hash)

    set_balance(web3, player_address, Web3.to_wei(1, 'ether'))

    return rcpt.contractAddress

app = sandbox.run_launcher(deploy)