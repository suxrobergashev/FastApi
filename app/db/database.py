from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import dotenv

dotenv.load_dotenv()
ENV_VALUES = dotenv.dotenv_values()
DB_URL = (f"{ENV_VALUES.get('DB_ENGINE')}://{ENV_VALUES.get('DB_USER')}:{ENV_VALUES.get('DB_PASSWORD')}"
          f"@{ENV_VALUES.get('DB_SERVER')}:{ENV_VALUES.get('DB_PORT')}/{ENV_VALUES.get('DB_NAME')}")

engine = create_engine(DB_URL, echo=True if ENV_VALUES.get("SQLALCHEMY_ECHO") == '1' else False)

Base = declarative_base()
session = sessionmaker()
