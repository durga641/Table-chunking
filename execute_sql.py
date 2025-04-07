{
    "dev": {
        "SNOWFLAKE_ACCOUNT": "xyz123.us-east-1",
        "SNOWFLAKE_USER": "your_dev_user",
        "SNOWFLAKE_DATABASE": "dev_db",
        "SNOWFLAKE_SCHEMA": "public",
        "SNOWFLAKE_WAREHOUSE": "dev_warehouse"
    },
    "prod": {
        "SNOWFLAKE_ACCOUNT": "xyz123.us-east-1",
        "SNOWFLAKE_USER": "your_prod_user",
        "SNOWFLAKE_DATABASE": "prod_db",
        "SNOWFLAKE_SCHEMA": "public",
        "SNOWFLAKE_WAREHOUSE": "prod_warehouse"
    }
}


import snowflake.connector
import os
import sys
import json

# Get the environment (default to "dev" if not set)
ENV = os.getenv("ENVIRONMENT", "dev")


# Simple Python program to read and print a file's content

def read_file(file_path):
    try:
        # Open the file in read mode
        with open(file_path, 'r') as file:
            # Read and print the content of the file
            content = file.read()
            print(content)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Specify the path to your file
file_path = 'example.txt'  # Replace with your file path

# Call the function to read and print the file
read_file(file_path)


# Load JSON config
config_path = "config/config.json"
if not os.path.exists(config_path):
    print(f"Config file not found: {config_path}")
    sys.exit(1)

with open(config_path, "r") as config_file:
    config = json.load(config_file)

# Validate environment key
if ENV not in config:
    print(f"Environment '{ENV}' not found in config.json")
    sys.exit(1)

# Extract Snowflake connection details for the selected environment
env_config = config[ENV]
SNOWFLAKE_ACCOUNT = env_config["SNOWFLAKE_ACCOUNT"]
SNOWFLAKE_USER = env_config["SNOWFLAKE_USER"]
SNOWFLAKE_DATABASE = env_config["SNOWFLAKE_DATABASE"]
SNOWFLAKE_SCHEMA = env_config["SNOWFLAKE_SCHEMA"]
SNOWFLAKE_WAREHOUSE = env_config["SNOWFLAKE_WAREHOUSE"]

# Get the SQL file name from arguments
if len(sys.argv) < 2:
    print("No SQL file provided.")
    sys.exit(1)

sql_file = sys.argv[1]

# Read the private key from the environment variable
SNOWFLAKE_PRIVATE_KEY_PATH = os.getenv("SNOWFLAKE_PRIVATE_KEY_PATH")
if not SNOWFLAKE_PRIVATE_KEY_PATH:
    print("Private key path not set.")
    sys.exit(1)

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
    print(f"Connected to Snowflake ({ENV} environment). Executing {sql_file}...")
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
