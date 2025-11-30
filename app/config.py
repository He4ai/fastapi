import os
from dotenv import load_dotenv
load_dotenv()


POSTGRES_DB = os.getenv("POSTGRES_DB", 'app')
POSTGRES_USER = os.getenv("POSTGRES_USER", 'postgres')
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", 'root')
POSTGRES_HOST = os.getenv("POSTGRES_HOST", 'localhost')
POSTGRES_PORT = os.getenv("POSTGRES_PORT", '5431')
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE", 'avito')

PG_DSN = (f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@'
          f'{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}')
