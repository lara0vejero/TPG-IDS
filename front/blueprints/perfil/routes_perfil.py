from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, current_app
import requests

perfil_bp = Blueprint("perfil_bp", __name__)

@perfil_bp.route("/perfil/<int:id_usuario>", methods=["GET", "POST"])
def perfil(id_usuario):

    # -------- PROTECCIÓN --------
    if "user_id" not in session:
        return redirect(url_for("iniciar_sesion_bp.iniciar_sesion"))

    if session["user_id"] != id_usuario:
        return jsonify({"error": "Acceso no autorizado"}), 403

    BACK_URL = current_app.config["BACK_URL"]
    id_usuario = session["user_id"]

    # -------- FORMULARIOS (ACEPTAR / CANCELAR) --------
    if request.method == "POST":
        accion = request.form.get("accion")
        codigo = request.form.get("codigo_intercambio")

        if accion == "aceptar":
            requests.post(
                f"{BACK_URL}/libros/aceptar_intercambio",
                json={"codigo_intercambio": codigo}
            )

        elif accion == "cancelar":
            requests.post(
                f"{BACK_URL}/libros/cancelar_intercambio",
                json={"codigo_intercambio": codigo, "usuario_id": id_usuario}
            )

        return redirect(url_for("perfil_bp.perfil", id_usuario=id_usuario))

    # -------- OBTENER HISTORIAL DEL BACK --------
    r = requests.get(f"{BACK_URL}/libros/intercambios/historial/{id_usuario}")

    if r.status_code == 200:
        historial = r.json()
    else:
        historial = {"pendientes": [], "completados": [], "cancelados": []}

    # -------- ENVIAR DATOS A TU TEMPLATE --------
    return render_template(
        "perfil.html",
        titulo="Mi Perfil",
        nombre_usuario=session.get("nombre"),
        email_usuario=session.get("email"),
        id_usuario=id_usuario,
        historial=historial
    )
