import sys
import os
from sqlalchemy import create_engine, MetaData

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))

from config import Config

def clean_db():
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    metadata = MetaData()
    metadata.reflect(bind=engine)

    metadata.drop_all(bind=engine)
    print("All tables have been deleted.")

if __name__ == "__main__":
    clean_db()
