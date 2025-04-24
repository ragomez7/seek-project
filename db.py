from dotenv import load_dotenv
import os 
from pymongo import MongoClient

load_dotenv(dotenv_path=".env.local", override=True)
load_dotenv(override=True)

MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = int(os.getenv("MONGO_PORT", "27017"))
CA_FILE_PATH = os.getenv("CA_FILE_PATH")

print(
    f"[DEBUG] MONGO_HOST={MONGO_HOST}, MONGO_PORT={MONGO_PORT}, CA_FILE_PATH={CA_FILE_PATH}")

try:
    client = MongoClient(
        host=MONGO_HOST,
        port=MONGO_PORT,
        username="master",
        password=MONGO_PASSWORD,
        tls=True,
        tlsCAFile=CA_FILE_PATH,
        tlsAllowInvalidHostnames=True,
        serverSelectionTimeoutMS=5000,
        retryWrites=False,
        directConnection=True,
    )
except Exception as e:
    print(f"[ERROR] Failed to create MongoClient: {e}")
    raise