import os
from astrapy import DataAPIClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

token  = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
endpoint  = os.getenv("ASTRA_DB_API_ENDPOINTS")
namespace = os.getenv("ASTRA_DB_NAMESPACE")
collection = os.getenv("ASTRA_DB_COLLECTION")

if not token or not endpoint or not collection:
    raise RuntimeError(
        "Environment variables ASTRA_DB_API_ENDPOINT, ASTRA_DB_COLLECTION ASTRA_DB_APPLICATION_TOKEN must be defined"
    )

client = DataAPIClient(token)
database = client.get_database(endpoint)
collection = database.get_collection(collection)  