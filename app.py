from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db
from routes import page_routes
from routes.page_routes import bp as page_routes_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(page_routes.bp)

    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)