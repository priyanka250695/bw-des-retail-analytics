import boto3
from vaultUtil import getVaultCred

vault_url = "http://127.0.0.1:8200"
role_id = "e4a4a890-2207-16f5-835f-e8bbb020c4d1"
secret_id = "dda22be7-92d9-5788-715b-71d71f47b83e"
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



class AWSConnector:
    def __init__(self, aws_access_key, aws_secret_key, aws_region='us-east-1', client='s3'):
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key
        self.aws_region = aws_region
        self.aws_client = client
        self.session = self.create_session()
        self.s3_client_conn = self.create_aws_client()

    def create_session(self):
        session = boto3.Session(
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_key,
            region_name = self.aws_region
        )
        return session

    def create_aws_client(self):
        aws_client_conn = self.session.client(self.aws_client)
        return aws_client_conn

# Create an instance of the AWSConnector class with the default region (us-east-1)
client = "s3"
aws_region = "us-east-1"
aws_connector = AWSConnector(aws_access_key, aws_secret_key, aws_region, client)

# Create S3 client
s3_client = aws_connector.s3_client_conn

response = s3_client.list_buckets()
print("s3_buckets")
for bucket in response['Buckets']:
    print(f"{bucket['Name']}")
