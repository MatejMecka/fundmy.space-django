from stellar_sdk import Server, Keypair, TransactionBuilder, Network, FeeBumpTransaction, ClaimPredicate, Claimant, Asset, exceptions
import os
import json
server = Server("https://horizon-testnet.stellar.org")

def getAssets(public_key: str) -> list:
    """
    Get all the balances an account has.
    """
    balances = server.accounts().account_id(public_key).call()['balances'] # Call API
    # Parse Data
    balances_to_return = [ {"asset_code": elem.get("asset_code"), "issuer": elem.get("asset_issuer"), "balance": int(float(elem.get("balance")))} for elem in balances ]
    balances_to_return[-1]["asset_code"] = "Stellar Lumens (XLM)"
    balances_to_return.reverse()
    return balances_to_return

def getOperations(public_key: str) -> list:
    """
    Get all the claimable_balance operations a user executed.
    """
    operations = server.operations().for_account(public_key).limit(200).order(desc=True).include_failed(False).call()['_embedded']['records']
    data = []
    for operation in operations:
        if operation['type'] == "claim_claimable_balance":
            data.append({"created_at": operation.get("created_at"), "url": f"https://stellar.expert/explorer/testnet/tx/{operation.get('transaction_hash')}"})
            print(operation.get("transaction_hash"))
    return data

def getClaimableBalances(public_key: str) -> list:
    """
    Get all the claimable balances an account has to claim.
    """
    balances = server.claimable_balances().for_claimant(public_key).call()['_embedded']['records']
    return [ {"sponsor": elem.get("sponsor"), "id": elem.get("id"), "asset": elem.get("asset").replace('native', 'XLM').split(':')[0], "amount": round(int(float(elem.get("amount"))))} for elem in balances ]

def checkTrustline(asset :str, issuer:str, available_assets: list) -> bool:
    """
    Check if in the balances of the account an asset like that alredy exists to establish a trustline
    """
    for elem in available_assets:
        if elem["sponsor"] == asset:
            return True
    return False

def XDRForClaimableBalance(public_key: str, balance_id: str, asset=None, asset_issuer=None):
    """
    Generate an XDR to Claim a Balance using Albedo or web+stellar
    """
    base_fee = server.fetch_base_fee()
    if(getAssets(public_key)[0] == 0):
        # 3. User does not have enough XLM to pay fees
        account = server.load_account(public_key)
        transaction = TransactionBuilder(
            source_account=account,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=base_fee,
        ).append_claim_claimable_balance_op(
            balance_id=balance_id,
            source=public_key
        ).build()

        return transaction.to_xdr()

        # 4. User does not have enough XLM to pay fees or establish trustline

        transaction = TransactionBuilder(
            source_account=account,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=base_fee,
        ).append_begin_sponsoring_future_reserves_op(
            sponsored_id=other_account_pub_key,
            source=quest_account_pub_key
        ).append_create_account_op(
            destination=other_account_pub_key,
            starting_balance="0",
            source=quest_account_pub_key
        ).append_end_sponsoring_future_reserves_op(
            source=other_account_pub_key
        ).build()

        return transaction.to_xdr()
       
    else:
        account = server.load_account(public_key)
        if (asset == None and asset_issuer == None) or checkTrustline(asset, getAssets(public_key)):
            # 1. User has enough XLM to pay fees for claimable balances
            transaction = TransactionBuilder(
                source_account=account,
                network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
                base_fee=base_fee,
            ).append_claim_claimable_balance_op(
                balance_id=balance_id,
                source=public_key
            ).build()

            return transaction.to_xdr()
        
        # 2. User has enough XLM to pay fees but needs to establish Trustline
        transaction = TransactionBuilder(
            source_account=account,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=base_fee,
        ).append_change_trust_op(
            asset_code=asset, 
            asset_issuer=asset_issuer
        ).append_claim_claimable_balance_op(
            balance_id=balance_id,
            source=public_key
        ).build()

        return transaction.to_xdr()

def createAccount(public_key: str):
    """
    Create a Stellar Account with 0 Balance
    """
    base_fee = server.fetch_base_fee()
    account = server.load_account(os.environ["STELLAR_PRIVATE_KEY"])

    transaction = TransactionBuilder(
        source_account=account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=base_fee,
    ).append_begin_sponsoring_future_reserves_op(
        sponsored_id=public_key,
        source=account.public_key
    ).append_create_account_op(
        destination=public_key,
        starting_balance="0",
        source=account.public_key
    ).append_end_sponsoring_future_reserves_op(
        source=public_key
    ).build()

    transaction.sign(account.secret)

    return transaction.to_xdr()
