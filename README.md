# Generate eth validator keys and store them in Vault

This creates a web API to hit for creating ETH validator keys and importing them to a Prysm keystore (max 100 validators). This prototype is for demonstrative purposes only.

<hr>
hit end point `/createkey` with the following GET requests:

`address=<eth_withdrawal_wallet_address>`

`chain=<goerli / mainnet>`

`number_of_validators=<int>`

`token=<auth_token>`

## How to run

Build docker image:

`docker build -t <name>/ethkey:latest -f ethkey.dockerfile .`

Run your docker image:

`docker run -p 5000:5000 -e API_TOKEN="asdf" -e VAULT_TOKEN="asdfasdf" -e VAULT_ADDR="http://1.2.3.4:8200" <name>/ethkey:latest`

<hr>

TODO:
- improve better error handling
- look into generating and signing exit msg (validator accounts voluntary-exit --exit-json-output-dir `The output directory to write voluntary exits as individual unencrypted JSON files. If this flag is provided, voluntary exits will be written to the provided directory and will not be broadcasted.` )
- parameterize vault path
- improve sanity checks && confirm data is stored in vault before moving on
- improve logs
- add zabbix_sender for reporting
