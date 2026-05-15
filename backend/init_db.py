"""Initialize the database schema."""
from app.database import engine, Base
from app.models import User, Recipe

def init_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")

if __name__ == "__main__":
    init_db()
