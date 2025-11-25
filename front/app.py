from flask import Flask
from blueprints.biblioteca.biblioteca import biblioteca_bp
from blueprints.cargar_libros.cargar_libros import cargar_libro_bp
from blueprints.mis_libros.mis_libros import mis_libros_bp
from blueprints.form_intercambio.form_intercambio import form_intercambio_bp

app = Flask(__name__)

# Clave para manejar sesiones de usuarios
app.secret_key = "super_secret_key"

# URL DEL BACKEND
app.config["BACK_URL"] = "http://127.0.0.1:5002"

# permite usar BACK_URL en templates

@app.context_processor
def inject_globals():
    return {
        "BACK_URL": app.config["BACK_URL"]
    }

app.register_blueprint(biblioteca_bp, url_prefix="/biblioteca")
app.register_blueprint(cargar_libro_bp, url_prefix="/cargar_libro")
app.register_blueprint(mis_libros_bp, url_prefix="/mis_libros")
app.register_blueprint(form_intercambio_bp, url_prefix="/intercambio")

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
