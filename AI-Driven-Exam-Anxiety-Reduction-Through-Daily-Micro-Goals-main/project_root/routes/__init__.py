from routes.auth_routes import auth_bp
from routes.student_routes import student_bp
from routes.parent_routes import parent_bp

def register_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(parent_bp)
