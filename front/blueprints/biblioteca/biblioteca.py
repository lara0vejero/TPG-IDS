from flask import Blueprint, render_template, session, redirect, url_for, current_app
import requests

biblioteca_bp = Blueprint("biblioteca_bp", __name__)

@biblioteca_bp.route("/")
def biblioteca():
    # Asegurarse de que el usuario esté logueado
    if "user_id" not in session:
        return redirect(url_for("iniciar_sesion_bp.iniciar_sesion"))

    BACK_URL = current_app.config["BACK_URL"]
    usuario_id = session["user_id"]

    # Llamar al backend para obtener libros disponibles de otros usuarios
    response = requests.get(
        f"{BACK_URL}/libros/disponibles",
        params={"excluir_usuario": usuario_id}
    )

    if response.status_code != 200:
        libros = []
    else:
        data = response.json()
        libros = data.get("libros", [])

    # Ruta donde se guardan las imágenes en el backend
    URL_BACK_IMAGEN = f"{BACK_URL}/static/images/"

    return render_template(
        "biblioteca.html",
        libros=libros,
        URL_BACK_IMAGEN=URL_BACK_IMAGEN,
        titulo="Biblioteca"
    )
