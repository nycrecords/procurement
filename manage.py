from app import create_app, db
from sqlalchemy import text

app = create_app()

# Test the database connection
with app.app_context():
    try:
        db.session.execute(text('SELECT 1'))
        print("Database connection successful")
    except Exception as e:
        print("Error: ", e)

if __name__ == '__main__':
    app.run(debug=True)
