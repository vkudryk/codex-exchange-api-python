from codex.api import CodexExchangeAPI
import json

try:
    with open('credentials.json', 'r') as creds_file:
        credentials = json.load(creds_file)
except FileNotFoundError:
    exit('credentials.json not found.')

codex = CodexExchangeAPI(
    public_key=credentials.get('public_key'),
    secret_key=credentials.get('secret_key')
)

print(codex.get_balances())
