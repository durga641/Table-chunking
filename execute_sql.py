import snowflake.connector
import os
import sys

# Snowflake connection details from environment variables
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PRIVATE_KEY_PATH = os.getenv("SNOWFLAKE_PRIVATE_KEY_PATH")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")

# Get the SQL file name from arguments
if len(sys.argv) < 2:
    print("No SQL file provided.")
    sys.exit(1)

sql_file = sys.argv[1]

# Read the private key
with open(SNOWFLAKE_PRIVATE_KEY_PATH, "rb") as keyfile:
    private_key = keyfile.read()

# Establish connection to Snowflake
try:
    conn = snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        account=SNOWFLAKE_ACCOUNT,
        private_key=private_key,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA,
    )
    print(f"Connected to Snowflake. Executing {sql_file}...")
except Exception as e:
    print(f"Failed to connect to Snowflake: {str(e)}")
    sys.exit(1)

# Read and execute the SQL file
try:
    with open(sql_file, "r") as file:
        sql_commands = file.read()

    with conn.cursor() as cur:
        cur.execute(sql_commands)

    print("✅ SQL Execution Completed Successfully!")

except Exception as e:
    print(f"Error executing SQL: {str(e)}")

finally:
    conn.close()
