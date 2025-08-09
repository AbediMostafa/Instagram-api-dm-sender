from peewee import *
from playhouse.pool import PooledPostgresqlDatabase

from dotenv import load_dotenv
import os

load_dotenv()

# Get the values from environment variables
user = os.getenv("POSTGRES_USER", "postgres")
password = os.getenv("POSTGRES_PASSWORD", "arka")
host = os.getenv("POSTGRES_HOST", "localhost")
port = int(os.getenv("POSTGRES_PORT", "5434"))
database_name = os.getenv("POSTGRES_DB", "instagram_dm_sender")

# Set up the database connection
# database = PostgresqlDatabase(
#     database_name,
#     user=user,
#     host=host,
#     port=port,
# )

database = PooledPostgresqlDatabase(
    database_name,
    user=user,
    host=host,
    port=port,
    max_connections=200,  # pool size, adjust as needed
    stale_timeout=100,
)
database.connect()


class BaseModel(Model):
    class Meta:
        database = database
