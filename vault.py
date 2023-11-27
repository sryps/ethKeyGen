import logging
import os
import requests
import time
import subprocess
import json

def vaultInit(resp, password, chain):
    logging.info( "Adding values to vault...")
    id = "%s-%s" % (resp["withdrawal_address"], int(time.time()))
    vaultToken = os.environ['VAULT_TOKEN']
    vaultAddr = os.environ['VAULT_ADDR']
    vaultBaseURL = "%s/v1/ethereum/data/%s" % (vaultAddr,id)

    keystore = getPrysmKeystore(resp["data"],password, chain)

    data = {
        "deposit_data": {"deposit_data": resp["data"]["deposit_data"]},
        "mnemonic": resp["data"]["mnemonic"]["seed"],
        "withdrawal_address": resp["withdrawal_address"],
        "password": password,
        "keystore": str(keystore)
    }

    headers = {
    "X-Vault-Token": vaultToken,
    "Content-Type": "application/json",
    }

    payload = {
        "data": data,
    }

    try:
        response = requests.post(vaultBaseURL, headers=headers, json=payload, timeout=8)
        if response.status_code == 200:
            return {"response": "Secrets successfully added to HashiCorp Vault!"}
        else:
            print(f"Failed to add secret. Status code: {response.status_code}")
            return {"error": response.text }
    except requests.exceptions.Timeout:
        print(f"Request timed out after 8 seconds.")
        return { "error": "Request timed out after 8 seconds."}
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return { "error": e}

    
def getPrysmKeystore(dpData, password, chain):

    home = os.environ['HOME']

    passwordPath = "%s/pwd" % (home)
    if os.path.exists(passwordPath):
        os.remove(passwordPath)

    checkPath = "%s/.eth2validators/prysm-wallet-v2/direct/accounts/all-accounts.keystore.json" % (home)
    if os.path.exists(checkPath):
        os.remove(checkPath)
 
    rm_path = "%s/keys/validator_keys" % (home)
    file_list = os.listdir(rm_path)

    for file_name in file_list:
        file_path = os.path.join(rm_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)

    with open(passwordPath, 'w') as file:
        file.write(password)
    
    keystorePath = "%s/keys/validator_keys" % (home)
    i = 0
    for key in dpData["keystores"]:
        newPath = "%s/%s%s%s%s.json" % (keystorePath, "keystore-m_12381_3600_",i,"_0_0-",int(time.time()))
        i += 1
        with open(newPath, 'w') as file:
            keyMod = str(key).replace("'","\"")
            keyMod2 = keyMod.replace("None","\"\"")
            file.write(keyMod2)

    cmd = "validator accounts import --accept-terms-of-use --keys-dir %s/keys/validator_keys --wallet-password-file %s/pwd --account-password-file %s/pwd --%s" % (home,home,home,chain)
    resp = subprocess.run(
        cmd,
        shell=True,
        check=True)
    
    checkPath = "%s/.eth2validators/prysm-wallet-v2/direct/accounts/all-accounts.keystore.json" % (home)
    if os.path.exists(checkPath):
        with open(checkPath, 'r') as file:
            file_contents = json.load(file)
            return file_contents
    else:
        return "keystore import failed"

  