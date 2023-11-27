from flask import Flask, request, jsonify
from vault import *

import subprocess
import json
import string
import random
import os
import requests
import logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

def generator(length=24):
    characters = string.ascii_letters + string.digits + "!"
    random_id = ''.join(random.choice(characters) for _ in range(length))
    return random_id

def deposit(chain,password,numVal,withdrawalAddr):
    cmd = "eth-staking-smith new-mnemonic --chain=%s --keystore_password='%s' --num_validators=%s --withdrawal_credentials=%s" % (chain,password,numVal,withdrawalAddr)
    seed = subprocess.check_output(
        cmd,
        shell=True)

    return json.loads(seed)

def checkVar(variableValue):
    if variableValue == None:
        return "ERROR: not included in GET request"
    else:
        return variableValue
        

@app.route("/createkey")
def createkey():

    token = request.args.get("token")
    apiToken = os.environ['API_TOKEN']
    if apiToken == None or token != apiToken:
        return {"error": "Invalid Token"}
    
    withdrawalAddr = request.args.get("address")
    isWithdrawalAddress = checkVar(withdrawalAddr)
    
    chain = request.args.get("chain")
    isChain = checkVar(chain)
    if chain != 'goerli' and chain != 'mainnet':
        msg = "unknow chain - %s" % (chain)
        return {"error": msg}
    
    numVal = request.args.get("number_of_validators")
    isNumVal = checkVar(numVal)
    if int(numVal) > 100:
        return {"error": "can not create more than 100 validators"}

    password = generator()
    
    if None not in (withdrawalAddr,chain,numVal):
        depositData = deposit(chain,password,numVal,withdrawalAddr)
        resp =  {
            "success": True,
            "withdrawal_address": withdrawalAddr,
            "data": depositData
        }
        msg = "%s - succesful key initialization" % (withdrawalAddr)
        logging.info(msg)

        userResponse = vaultInit(resp, password, chain)
        return userResponse, 200
    else:
        resp =  {
            "success": False,
            "withdrawalAddr": isWithdrawalAddress,
            "chain": isChain,
            "number_of_validators": isNumVal
        }
        return jsonify(resp), 200

if __name__ == "__main__":
    logging.info("Starting API server...")
    app.run("0.0.0.0", 5000, debug=True,ssl_context='adhoc')