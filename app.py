from flask import Flask
from app.docs import bp as docs, docs_url
from app.routes import bp as routes

def create_app():
    app = Flask(
        __name__,
        static_url_path='', 
        static_folder='public'
    )
    
    app.register_blueprint(routes)
    app.register_blueprint(docs, url_prefix=docs_url)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
