import requests

vault_url = "http://127.0.0.1:8200"
<<<<<<< HEAD
role_id = "1e490c5c-467b-02dd-ea11-bbf9229446dc"
secret_id = "daa278f2-3d73-19e1-7961-314be82ccf70"
secret_path = "secret/data/aws"
=======
role_id = "259ac15c-cb2b-6f65-c02c-892fafa57e34"
secret_id = "042053f0-7eb7-f6c6-cdbc-e6a91271edad"
secret_path = "secret/data/snow"
>>>>>>> 8c9b8899ec27a980a4109d21ddf48fb38ad07655

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
