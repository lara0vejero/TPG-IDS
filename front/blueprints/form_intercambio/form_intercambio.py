from flask import Blueprint, render_template, session, redirect, url_for, current_app, request
import requests

form_intercambio_bp = Blueprint("intercambio_bp", __name__)

@form_intercambio_bp.route("/", methods=["GET", "POST"])
def intercambio():

    #Validar sesion activa
    if "user_id" not in session:
        return redirect(url_for("iniciar_sesion_bp.iniciar_sesion"))

    BACK_URL = current_app.config["BACK_URL"]
    usuario_ofreciente = session["user_id"]


    # Mostramos formulario para elegir libro a ofrecer

    if request.method == "GET":
        libro_solicitado = request.args.get("libro_solicitado", type=int)

        if not libro_solicitado:
            return "Error: no seleccionaste ningún libro para solicitar", 400

        # Obtenemos mis libros disponibles
        resp_mis_libros = requests.get(f"{BACK_URL}/libros/mis-libros/{usuario_ofreciente}")

        if resp_mis_libros.status_code != 200:
            return "Error al obtener tus libros", 500

        mis_libros = resp_mis_libros.json().get("libros", [])

        # Validar que tenga al menos un libro disponible
        libros_disponibles = [l for l in mis_libros if l["estado_del_libro"] == "disponible"]

        if not libros_disponibles:
            # Si no tiene libros, lo llevo a cargar uno
            return redirect(url_for("cargar_libro_bp.cargar_libro"))

        # Obtener info del libro solicitado
        resp_libro_solicitado = requests.get(f"{BACK_URL}/libros/{libro_solicitado}")

        if resp_libro_solicitado.status_code != 200:
            return "El libro solicitado no existe", 404

        libro_info = resp_libro_solicitado.json()

        return render_template(
            "intercambio.html",
            libros_usuario=libros_disponibles,
            libro_solicitado=libro_info,
            titulo="Intercambiar Libro"
        )

    # Enviar solicitud de intercambio al backend
    libro_solicitado = request.form.get("libro_solicitado", type=int)
    libro_ofrecido = request.form.get("libro_ofrecido", type=int)

    if not libro_solicitado or not libro_ofrecido:
        return "Datos incompletos para solicitar intercambio", 400

    # Obtener el dueño del libro solicitado
    resp_libro = requests.get(f"{BACK_URL}/libros/{libro_solicitado}")

    if resp_libro.status_code != 200:
        return "No se encontró el libro solicitado", 404

    usuario_solicitado = resp_libro.json().get("usuario_id")

    # Construir JSON del intercambio
    data = {
        "id_libro_solicitado": libro_solicitado,
        "id_libro_ofrecido": libro_ofrecido,
        "id_usuario_ofrecido": usuario_ofreciente,
        "id_usuario_solicitado": usuario_solicitado
    }

    requests.post(f"{BACK_URL}/intercambios/solicitar", json=data)

    # Volver al perfil del usuario
    return redirect(url_for("perfil_bp.perfil", id_usuario=usuario_ofreciente))
