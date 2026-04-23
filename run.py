from app import app
from app_blueprints import register_all_blueprints
from extensions.extensions import db

register_all_blueprints(app)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        
    print("running")
    app.run()