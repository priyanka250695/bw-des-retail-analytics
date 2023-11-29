import requests

vault_url = "http://127.0.0.1:8200"
role_id = "e4a4a890-2207-16f5-835f-e8bbb020c4d1"
secret_id = "dda22be7-92d9-5788-715b-71d71f47b83e"
secret_path = "secret/data/aws"

class getVaultCred:

    def __init__(self, vault_url, role_id, secret_id, secret_path):
        self.vault_url = vault_url
        self.role_id = role_id
        self.secret_id = secret_id
        self.secret_path = secret_path
        self.token = None

    def authenticate_with_approle(self):
        auth_url = f"{self.vault_url}/v1/auth/approle/login"
        auth_data = {
            "role_id": self.role_id,
            "secret_id": self.secret_id
        }
        try:
            auth_response = requests.post(auth_url, json=auth_data)
            auth_response.raise_for_status()

            self.token = auth_response.json()["auth"]["client_token"]
            return self.token
        
        except requests.exceptions.RequestException as e:
            print(f"Authentication error: {e}")
            return None

    def get_secret(self, token):
        headers = {
            "X-Vault-Token": token,
        }
        url = f"{self.vault_url}/v1/{self.secret_path}"

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            secret_data = response.json()["data"]

            return secret_data

        except requests.exceptions.RequestException as e:
            print(f"Error retrieving secret: {e}")  
            return None  

# Create an instance of the getVaultCred class
vault_cred = getVaultCred(vault_url, role_id, secret_id, secret_path)

# Authenticate with AppRole and get token
token = vault_cred.authenticate_with_approle()

if token:
    # Retrieve the secret using the obtained token
    secret_data = vault_cred.get_secret(token)
    print(secret_data)
