# database/connect_database.py
# Purpose: Provides database connection parameters. Centralizes database configuration to make it
# easy to modify connection settings in one place.

# Function: Return database connection parameters as a dictionary
def get_connection_params():
    return {
        "host": "localhost",
        "user": "root",
        "password": "",
        "database": "shs_registration_system"
    }
