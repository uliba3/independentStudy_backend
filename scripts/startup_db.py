import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import engine
from app.db.schema import Base

print("Script started")
print(f"Engine URL: {engine.url}")


if __name__ == "__main__":
    print("Attempting to create tables...")
    try:
        Base.metadata.create_all(engine)
        print("Tables created successfully")
    except Exception as e:
        print(f"An error occurred: {e}")


print("Script finished")
