# from app import create_app, db
# import os

# def init_db():
#     # Get the current directory path
#     base_dir = os.path.abspath(os.path.dirname(__file__))

#     # Create the app with the database path
#     app = create_app()

#     # Print where the database will be created
#     db_path = os.path.join(base_dir, 'app.db')
#     print(f"Database will be created at: {db_path}")

#     with app.app_context():
#         # Drop all tables if they exist
#         db.drop_all()
#         # Create new tables
#         db.create_all()
#         print("Database created successfully!")

# if __name__ == "__main__":
#     init_db()


from app import create_app, db
from app.models import User, Availability, Appointment, Chat
import os


def init_db():
    app = create_app()

    # Print the actual database path
    print(f"Database path: {app.config['SQLALCHEMY_DATABASE_URI']}")

    with app.app_context():
        print("Starting database creation...")
        db.drop_all()
        db.create_all()

        # Verify tables
        inspector = db.inspect(db.engine)
        created_tables = inspector.get_table_names()
        print(f"Created tables: {created_tables}")

        # Print the actual file location
        db_path = app.config["SQLALCHEMY_DATABASE_URI"].replace("sqlite:///", "")
        print(f"Database file should be at: {db_path}")
        print(f"Database file exists: {os.path.exists(db_path)}")


if __name__ == "__main__":
    init_db()
