# app/routes/__init__.py
def register_routes(app):
    from .main import main_bp
    from .auth import auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)