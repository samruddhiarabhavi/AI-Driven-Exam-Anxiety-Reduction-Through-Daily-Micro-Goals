from flask import Flask
from config import Config
from models import db
from routes import register_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ---------- DATABASE ----------
    db.init_app(app)

    with app.app_context():
        from models.student import Student
        from models.goal import DailyGoal
        from models.session import StudySession
        from models.message import EncouragementMessage
        db.create_all()

    # ---------- ROUTES ----------
    register_routes(app)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
