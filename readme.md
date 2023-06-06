# API Documentation

The API provides two endpoints for interacting with the NFT system.

## Upload a PDF file and mint an NFT

- Endpoint: `/api/upload-pdf/`
- Method: `POST`
- Request Payload: The request should include a PDF file in the `pdf_file` field of the multipart/form-data.
- Response: Upon successful upload and NFT minting, the response will include the following fields:
  - `message`: A success message indicating the PDF upload was successful.
  - `sha256_checksum`: The SHA256 checksum of the uploaded PDF file.
  - `metadata`: The metadata extracted from the PDF file.

## Get a list of owned NFTs

- Endpoint: `/api/list-nfts/`
- Method: `GET`
- Query Parameters:
  - `marker` (optional): The last NFT ID from the previous request. Used for pagination.
- Response: The response will include a list of owned NFTs.

# Credentials Instructions

To use the NFT system, you need to set up the following credentials and environment variables:

## NFT Storage Token

- Generate a token from [https://nft.storage/manage/](https://nft.storage/manage/).
- Set the environment variable `NFT_STORAGE_TOKEN` in your command-line interface:
  - Windows Command Prompt: `set NFT_STORAGE_TOKEN={Authorization: Bearer Token}`

## Ripple Credentials

- Get the credentials from [https://xrpl.org/xrp-testnet-faucet.html](https://xrpl.org/xrp-testnet-faucet.html).
- Set the following environment variables in your command-line interface:
  - Windows Command Prompt: `set XRPL_SECRET={Your Ripple secret key}`
  - Windows Command Prompt: `set XRPL_ADDRESS={Your Ripple addresy}`

# Running the Server and Unit Tests

To test the Django Rest Framework, follow these steps:

1. Change the directory to `deep_ink\deep_ink` in your command-line interface.
2. Run the following command to start the server: `python manage.py runserver`.
3. To run the unit tests, use the following command: `python manage.py test`.

Please make sure to set the environment variables and credentials correctly before running the server or the tests.
