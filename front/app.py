from flask import Flask, render_template

# IMPORTACIÓN DE BLUEPRINTS

# Front principal
from blueprints.index.routes_index import index_bp
from blueprints.sobre_nosotros.routes_sobre_nosotros import sobre_nosotros_bp
from blueprints.funcionamiento.routes_funcionamiento import funcionamiento_bp
from blueprints.contacto.routes_contacto import contacto_bp
from blueprints.registrarse.routes_registrarse import registrarse_bp
from blueprints.iniciar_sesion.routes_iniciar_sesion import iniciar_sesion_bp
from blueprints.perfil.routes_perfil import perfil_bp

# Biblioteca e intercambio
from blueprints.biblioteca.biblioteca import biblioteca_bp
from blueprints.cargar_libros.cargar_libros import cargar_libro_bp
from blueprints.mis_libros.mis_libros import mis_libros_bp
from blueprints.form_intercambio.form_intercambio import form_intercambio_bp

# CONFIGURACIÓN GENERAL

app = Flask(__name__)
app.secret_key = "super_secret_key"

# URL del Backend (ACÁ está el cambio que hizo tu amiga)
app.config["BACK_URL"] = "https://laru.pythonanywhere.com"

# VARIABLES GLOBALES

@app.context_processor
def inject_globals():
    return dict(BACK_URL=app.config["BACK_URL"])

# REGISTRO DE BLUEPRINTS

app.register_blueprint(index_bp, url_prefix="/")
app.register_blueprint(sobre_nosotros_bp, url_prefix="/sobre_nosotros")
app.register_blueprint(funcionamiento_bp, url_prefix="/funcionamiento")
app.register_blueprint(contacto_bp, url_prefix="/contacto")
app.register_blueprint(registrarse_bp, url_prefix="/registrarse")
app.register_blueprint(iniciar_sesion_bp, url_prefix="/iniciar_sesion")
app.register_blueprint(perfil_bp)

# Otros blueprints
app.register_blueprint(biblioteca_bp, url_prefix="/biblioteca")
app.register_blueprint(cargar_libro_bp, url_prefix="/cargar_libro")
app.register_blueprint(mis_libros_bp, url_prefix="/mis_libros")
app.register_blueprint(form_intercambio_bp, url_prefix="/intercambio")

# MANEJO DE ERRORES

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500

# EJECUCIÓN DEL SERVIDOR

if __name__ == "__main__":
    print("Flask corriendo en http://localhost:5000")
    app.run(host="localhost", port=5000, debug=True)
