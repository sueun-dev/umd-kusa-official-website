# run.py
from app import create_app, db

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensure tables are created before starting the app
    app.run(port=8080)
