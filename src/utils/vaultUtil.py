import requests

vault_url = "http://127.0.0.1:8200"
role_id = "259ac15c-cb2b-6f65-c02c-892fafa57e34"
secret_id = "042053f0-7eb7-f6c6-cdbc-e6a91271edad"
secret_path = "secret/data/aws"

def authenticate_with_approle():
    auth_url = f"{vault_url}/v1/auth/approle/login"
    auth_data = {
        "role_id": role_id,
        "secret_id": secret_id
    }
    try:
        auth_response = requests.post(auth_url, json=auth_data)
        auth_response.raise_for_status()

        token = auth_response.json()["auth"]["client_token"]
        print("token===========",)
        return token
    
    except requests.exceptions.RequestException as e:
        print(f"Authentication error : {e}")
        return None

def get_secret(token):
    
    headers = {
        "X-Vault-Token": token,
    }
    url = f"{vault_url}/v1/{secret_path}"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        secret_data = response.json()["data"]

        return secret_data

    except requests.exceptions.RequestException as e:
        print(f"Error retrieving secret: {e}")  
        return None  


token = authenticate_with_approle()
secret_data = get_secret(token)

print(secret_data)


