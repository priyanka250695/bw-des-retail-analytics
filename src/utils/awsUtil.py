import boto3
from vaultUtil import getVaultCred

vault_url = "http://127.0.0.1:8200"
role_id = "1e490c5c-467b-02dd-ea11-bbf9229446dc"
secret_id = "daa278f2-3d73-19e1-7961-314be82ccf70"
secret_path = "secret/data/aws"

# Create an instance of the getVaultCred class
vault_cred = getVaultCred(vault_url, role_id, secret_id, secret_path)

# Authenticate with AppRole and get token
token = vault_cred.authenticate_with_approle()



# Retrieve the secret using the obtained token
if token:
    # Retrieve the secret using the obtained token
    secret_data = vault_cred.get_secret(token)
    print(secret_data)

    # Extract AWS access key and secret key
    aws_access_key = secret_data['data']['bw-aws-accesskey-dev']
    aws_secret_key = secret_data['data']['bw-aws-secretkey-dev']   
    aws_region = "us-east-1"

    session = boto3.Session(aws_access_key_id=aws_access_key,
                            aws_secret_access_key=aws_secret_key,
                            region_name=aws_region)

    # Connect to AWS
    # aws_session = connect_to_aws(aws_access_key, aws_secret_key, aws_region)

    # Example: List all S3 buckets in the account
    s3_client = session.client("s3")
    response = s3_client.list_buckets()

    print("S3 Buckets:")
    for bucket in response["Buckets"]:
        print(f"- {bucket['Name']}")

    

