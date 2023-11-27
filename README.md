# Generate eth validator keys and store them in Vault

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