from flask_swagger_ui import get_swaggerui_blueprint

docs_url = '/api-docs'
docs_file = '/swagger.json'

bp = get_swaggerui_blueprint(
    docs_url,
    docs_file,
    config={
        'app_name': "Email Scheduler App | API Documentation"
    }
)