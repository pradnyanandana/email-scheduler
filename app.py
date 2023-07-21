from flask import Flask
from flask_migrate import Migrate
from app.routes import bp as app_bp
from database import db
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api-docs'
API_URL = '/swagger.json'

def create_app():
    app = Flask(
        __name__,
        static_url_path='', 
        static_folder='public'
    )

    app.config.from_object('config.Config')
    app.register_blueprint(app_bp)

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Email Scheduler App | API Documentation"
        }
    )

    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    
    db.init_app(app)
    migrate = Migrate(app, db)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
