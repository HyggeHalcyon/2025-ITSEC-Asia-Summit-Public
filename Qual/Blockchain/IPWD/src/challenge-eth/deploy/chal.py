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


def deploy(web3: Web3, deployer_address: str, deployer_privateKey: str, player_address: str) -> str:
    uri = web3.provider.endpoint_uri
    contract_info = json.loads(Path("compiled/Setup.sol/Setup.json").read_text())
    abi = contract_info["abi"]
    bytecode = contract_info["bytecode"]["object"]


    contract = web3.eth.contract(abi=abi, bytecode=bytecode)

    referralCodes = [
        "0x9a3f688fd6543508be48a13660f2d780f2601f617a3b44ef402f5b56eee7dd08",
        "0x06006085f233f903b528878a17f958db2bfba88148b76f5ae5abd6edbd4ddf41",
        "0x777ecc3d54067d660257e75b66dbba2845f25d57bf67ac9bc0b1c18f0376bf05",
        "0x1d51d1d58bd7ad06a12b7994e6b60261c9da16cb00a859f02b253a5a800e5c7f",
        "0xde6d5fbe8c4a4e5f054d5add98ce90adee46f41824c79e2e3f8245c6f6d342f1"
    ]

    construct_txn = contract.constructor(referralCodes).build_transaction(
        {
            "from": deployer_address,
            "value": Web3.to_wei(2500, 'ether'), #Give Ether to Setup.sol (if Required, else just comment this line)
            "nonce": web3.eth.get_transaction_count(deployer_address),
        }
    )

    tx_create = web3.eth.account.sign_transaction(construct_txn, deployer_privateKey)
    tx_hash = web3.eth.send_raw_transaction(tx_create.raw_transaction)

    rcpt = web3.eth.wait_for_transaction_receipt(tx_hash)

    set_balance(web3, player_address, Web3.to_wei(2.3, 'ether'))

    return rcpt.contractAddress

app = sandbox.run_launcher(deploy)
