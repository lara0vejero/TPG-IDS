from flask import Blueprint, render_template, session, redirect, url_for, current_app, request
import requests

mis_libros_bp = Blueprint("mis_libros_bp", __name__)

# Mostrar todos los libros del usuario

@mis_libros_bp.route("/")
def mis_libros():

    # Validar sesion
    if "user_id" not in session:
        return redirect(url_for("iniciar_sesion_bp.iniciar_sesion"))

    BACK_URL = current_app.config["BACK_URL"]
    usuario_id = session["user_id"]

    # Pedir mis libros al backend
    response = requests.get(f"{BACK_URL}/libros/mis-libros/{usuario_id}")

    if response.status_code != 200:
        libros = []
    else:
        libros = response.json().get("libros", [])

    URL_BACK_IMAGEN = f"{BACK_URL}/images/"

    return render_template(
        "mis_libros.html",
        libros=libros,
        URL_BACK_IMAGEN=URL_BACK_IMAGEN,
        titulo="Mis Libros"
    )

# Cambiar estado del libro (disponible / pausa)

@mis_libros_bp.route("/cambiar-estado/<int:libro_id>", methods=["POST"])
def cambiar_estado(libro_id):

    if "user_id" not in session:
        return redirect(url_for("iniciar_sesion_bp.iniciar_sesion"))

    BACK_URL = current_app.config["BACK_URL"]
    usuario_id = session["user_id"]

    nuevo_estado = request.form.get("estado")

    if nuevo_estado not in ["disponible", "pausa"]:
        return "Estado inválido", 400

    data = {"usuario_id": usuario_id, "nuevo_estado": nuevo_estado}

    requests.put(f"{BACK_URL}/libros/cambiar-estado/{libro_id}", json=data)

    return redirect(url_for("mis_libros_bp.mis_libros"))


# Eliminar un libro (solo disponibles)

@mis_libros_bp.route("/eliminar/<int:libro_id>", methods=["POST"])
def eliminar(libro_id):

    if "user_id" not in session:
        return redirect(url_for("iniciar_sesion_bp.iniciar_sesion"))

    BACK_URL = current_app.config["BACK_URL"]
    usuario_id = session["user_id"]

    data = {"usuario_id": usuario_id}

    requests.delete(f"{BACK_URL}/libros/eliminar/{libro_id}", json=data)

    return redirect(url_for("mis_libros_bp.mis_libros"))
