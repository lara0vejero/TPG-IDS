from flask import Blueprint, render_template, request, session, redirect, url_for, current_app
import requests

cargar_libro_bp = Blueprint("cargar_libro_bp", __name__)

@cargar_libro_bp.route("/", methods=["GET", "POST"])
def cargar_libro():

    #  Validar que haya sesion activa
    if "user_id" not in session:
        return redirect(url_for("iniciar_sesion_bp.iniciar_sesion"))

    # Si entra por GET (mostrar formulario)
    if request.method == "GET":
        return render_template("cargar_libro.html", titulo="Cargar Libro")

    # 2) Obtener los datos del formulario
    titulo = request.form.get("titulo")
    autor = request.form.get("autor")
    editorial = request.form.get("editorial")
    isbn = request.form.get("codigo_isbn")
    tematica = request.form.get("tematica")
    imagen = request.files.get("imagen")

    # Validacion minima
    if not titulo or not editorial or not isbn or not tematica:
        return render_template(
            "cargar_libro.html",
            error="Faltan datos obligatorios.",
            titulo="Cargar Libro"
        )

    BACK_URL = current_app.config["BACK_URL"]

    # JSON para crear el libro
    data_json = {
        "titulo": titulo,
        "autor": autor,
        "editorial": editorial,
        "codigo_isbn": isbn,
        "tematica": tematica,
        "usuario_id": session["user_id"]
    }

    # Enviar JSON (crear el libro)
    respuesta = requests.post(f"{BACK_URL}/libros/cargar", json=data_json)

    if respuesta.status_code != 201:
        return render_template(
            "cargar_libro.html",
            error="No se pudo cargar el libro.",
            titulo="Cargar Libro"
        )

    libro_id = respuesta.json()["libro_id"]

    # Subir imagen (si el usuario selecciono una)
    if imagen and imagen.filename:
        files = {
            "imagen": (imagen.filename, imagen.stream, imagen.mimetype)
        }

        resp_img = requests.post(
            f"{BACK_URL}/libros/{libro_id}/subir_imagen",
            files=files
        )

        # No frenar la lógica si la imagen falla
        if resp_img.status_code != 200:
            print("⚠️ Error al subir imagen, uso imagen por defecto")

    # 6) Redirigir al perfil del usuario
    return redirect(url_for("perfil_bp.perfil", id_usuario=session["user_id"]))
