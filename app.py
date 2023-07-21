# app.py
from flask import Flask
from app.routes import bp as app_bp
from database import db

app = Flask(__name__)

# Load configuration settings from config.py
app.config.from_object('config.Config')

# Register the app's blueprints
app.register_blueprint(app_bp)

if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
