from flask import Flask
from controller.docs import bp as docs, docs_url
from controller.routes import bp as routes

app = Flask(
    __name__,
    static_url_path='', 
    static_folder='public'
)

app.register_blueprint(routes)
app.register_blueprint(docs, url_prefix=docs_url)

if __name__ == '__main__':
    app.run(debug=True)
