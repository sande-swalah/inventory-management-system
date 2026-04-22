from app import app
from extensions.extensions import db
from user_handling import create_app_for_user_handling

app = create_app_for_user_handling(app)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        
    print("running")
    app.run()