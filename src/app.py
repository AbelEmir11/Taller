"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, send_from_directory
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_jwt_extended import JWTManager
from api.utils import APIException, generate_sitemap
from api.models import db, TokenBlockList
from api.routes import api
from api.admin import setup_admin
from datetime import timedelta
from api.commands import setup_commands # Nuevo comando para importación
from flask_mail import Mail, Message
from api.notifications_routes import notifications_bp
from api.success_stories_routes import success_stories_bp  # Rutas de casos de éxito


ENV = "development" if os.getenv("FLASK_DEBUG") == "1" else "production"
static_file_dir = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), '../public/')
app = Flask(__name__)
app.url_map.strict_slashes = False

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET")
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=3)
# Agregar configuración de correo (leer de env en producción)
app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER", app.config.get('MAIL_SERVER'))
app.config['MAIL_PORT'] = int(os.getenv("MAIL_PORT", app.config.get('MAIL_PORT', 587)))
app.config['MAIL_USE_TLS'] = os.getenv("MAIL_USE_TLS", "True") == "True"
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME", 'autoagendanotificaciones@example.com')
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD", '123456')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_DEFAULT_SENDER", 'AutoAgenda <autoagendanotificaciones@example.com>')

jwt = JWTManager(app)

# Manejo de errores JWT para retornar JSON en lugar de HTML
@jwt.unauthorized_loader
def custom_unauthorized_response(err_msg):
    return jsonify({"error": "Missing or malformed Authorization header", "details": err_msg}), 401

@jwt.invalid_token_loader
def custom_invalid_token_response(err_msg):
    return jsonify({"error": "Invalid token", "details": err_msg}), 422

@jwt.expired_token_loader
def custom_expired_token_response(jwt_header, jwt_payload):
    return jsonify({"error": "Token expired"}), 401

@jwt.revoked_token_loader
def custom_revoked_token_response(jwt_header, jwt_payload):
    return jsonify({"error": "Token has been revoked"}), 401

# database condiguration
db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db, compare_type=True)
db.init_app(app)

# add the admin
setup_admin(app)

# add the admin
setup_commands(app)

# Add all endpoints form the API with a "api" prefix
app.register_blueprint(api, url_prefix='/api')

# Handle/serialize errors like a JSON object

# Inicializar Mail usando la instancia definida en api package (api.__init__.py)
#from api import mail as mail_ext
#mail_ext.init_app(app)
# Evitar importar mail desde el paquete 'api' (posible conflicto en deploy).
# Inicializamos Mail localmente y lo registramos en la app.
mail = Mail()
mail.init_app(app)

# Registrar blueprint de notificaciones (queda bajo /api/...)
app.register_blueprint(notifications_bp, url_prefix="/api")

# Registrar blueprint de casos de éxito (queda bajo /api/...)
app.register_blueprint(success_stories_bp, url_prefix="/api")

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    if ENV == "development":
        return generate_sitemap(app)
    return send_from_directory(static_file_dir, 'index.html')

# any other endpoint will try to serve it like a static file


@app.route('/<path:path>', methods=['GET'])
def serve_any_other_file(path):
    if not os.path.isfile(os.path.join(static_file_dir, path)):
        path = 'index.html'
    response = send_from_directory(static_file_dir, path)
    response.cache_control.max_age = 0  # avoid cache memory
    return response
#pruebas de envio de email
@app.route('/test_mail')
def test_mail():
    from api.utils import send_email
    result = send_email("tu_correo@gmail.com", "Prueba desde Render", "Este es un correo de prueba")
    print("Resultado envío de prueba:", result)
    return jsonify({"sent": result})


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=PORT, debug=True)

