import cbpro

# Are you using a live trading environment or not?! Be careful!
LIVE = False

# This is for the sandbox
passphrase_sandbox = "o4edi2qjzvq"
b62secret_sandbox = "LCh4aVYtz9CWKAL7sDB2PxtNHbb2uSvxAvTeZuVwjKjWvm19q2OUfyHvJWFC8gpfapBCL1HjYxXxwy35KE3X0Q=="
key_sandbox = "c10b04be344e22419f5586a8b3a33aab"

# These credentials are used for LIVE trading
passphrase = 'INSERT_KEY'
b64secret = 'INSERT_KEY'
key = 'INSERT_KEY'

# Create an authenticated client using the above API keys
if LIVE:
    print('Using live trading environment')
    auth_client = cbpro.AuthenticatedClient(key, b64secret, passphrase)
else:
    print('Using sandbox environment')
    auth_client = cbpro.AuthenticatedClient(key_sandbox, b62secret_sandbox, passphrase_sandbox, api_url="https://api-public.sandbox.pro.coinbase.com")
