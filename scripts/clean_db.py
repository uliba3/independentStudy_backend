import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import engine
from app.db.schema import Base

def clean_all_tables():
    Base.metadata.drop_all(engine)

if __name__ == "__main__":
    clean_all_tables()
