# This auth procedure for the StackOverflow API is mildly annoying.
# Will probably need to find a better way to make it less painful.
#
# To perform authentication via OAuth2 for StackApps:
# 1. Use the following url with your input parameters to get the access code:
#       https://stackoverflow.com/oauth?client_id=[CLIENT_ID]&scopeno_expiry&redirect_uri=[REDIRECT_URI]
# 2. Accept the application permissions.
# 3. Copy and ave the code given in the url and run this authentication script.
# 4. Copy and save the access token from the response.
import requests

client_id = input("Enter StackApps ClientID: ")
consumer_secret = input("Enter Consumer Secret: ")
redir_uri = input("Enter StackApps redirect_uri: ")
auth_code = input("Enter StackApps Code: ")

access_token_url = "https://stackoverflow.com/oauth/access_token/json"

r = requests.post(access_token_url,
        data={'client_id': client_id,
            'client_secret': consumer_secret,
            'code': auth_code,
            'redirect_uri': redir_uri})
print(r.text)
