import os
import logging
import dotenv

dotenv.load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Database configurations
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "attentions_ai")

DB_CONNECTION_STRING = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Neo4j configurations
NEO4J_URI = os.getenv("NEO4J_URI", "neo4j+s://613d545a.databases.neo4j.io:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "t67gF4MnYYEPbzaPWj-P4bG24D07EAG7sMsipH0enSs")

# API configurations
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "a839101859b65fdbf7868152539e207c")

# Constants
MAX_ITERATIONS = 5