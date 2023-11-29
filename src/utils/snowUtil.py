import snowflake.connector
import boto3
from vaultUtil import getVaultCred

vault_url = "http://127.0.0.1:8200"
role_id = "06cafffa-f09a-b908-a1ef-a5947cae3bac"
secret_id = "a529b4da-9a62-90c8-1395-2453906d2ad7"
secret_path = "secret/data/snow"

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
# username = secret_data['data']['bw-snow-username-dev']
# username = secret_data['data']['bw-snow-userpass-dev']  

class SnowflakeConnector:
    def __init__(self, account, warehouse, database, schema, username, password):
        self.account = account
        self.warehouse = warehouse
        self.database = database
        self.schema = schema
        self.username = username
        self.password = password
        self.conn = None
        self.cursor = None

    def connect(self):
        """Establish a connection to Snowflake."""
        try:
            self.conn = snowflake.connector.connect(
                account=self.account,
                warehouse=self.warehouse,
                database=self.database,
                schema=self.schema,
                user=self.username,
                password=self.password
            )
            self.cursor = self.conn.cursor()
            print("Connected to Snowflake successfully.")
        except Exception as e:
            print(f"Error connecting to Snowflake: {str(e)}")

    def execute_query(self, query):
        """Execute a SQL query and fetch the results."""
        try:
            if self.cursor:
                self.cursor.execute(query)
                results = self.cursor.fetchall()
                return results
            else:
                print("Error: Cursor is not initialized.")
                return None
        except Exception as e:
            print(f"Error executing query: {str(e)}")
            return None

    def close_connection(self):
        """Close the Snowflake connection."""
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
            print("Snowflake connection closed.")
        except Exception as e:
            print(f"Error closing Snowflake connection: {str(e)}")

# Example Usage:
# Replace the placeholders with your Snowflake account information
snowflake_conn = SnowflakeConnector(
    account='dqb00356.us-east-1',
    warehouse='COMPUTE_WH',
    database='SNOWFLAKE_SAMPLE_DATA',
    schema='TPCH_SF1',
    username=secret_data['data']['bw-snow-username-dev'],
    password=secret_data['data']['bw-snow-userpass-dev']
)

try:
    snowflake_conn.connect()

    # Example Query
    query = "SELECT * FROM CUSTOMER"
    results = snowflake_conn.execute_query(query)

    if results:
        print("Query Results:")
        for row in results:
            print(row)

finally:
    snowflake_conn.close_connection()
