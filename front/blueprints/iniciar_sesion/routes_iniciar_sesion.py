from flask import Blueprint, render_template, request, redirect, url_for, current_app, session, jsonify
import requests

iniciar_sesion_bp = Blueprint("iniciar_sesion_bp", __name__)

@iniciar_sesion_bp.route("/iniciar_sesion", methods=["GET", "POST"])
def iniciar_sesion():
    titulo_pagina = "Iniciar sesión"

    # Mostrar el formulario si es GET
    if request.method == "GET":
        return render_template("iniciar_sesion.html", titulo=titulo_pagina)

    # --- POST: procesar datos enviados desde el formulario ---
    usuario_input = request.form.get("usuario_o_mail")
    clave_input = request.form.get("contrasena_usuario")

    # Validación mínima
    if not usuario_input or not clave_input:
        return jsonify({"error": "Por favor completá todos los campos"}), 400

    # Datos que se envían al backend
    payload = {
        "identificador": usuario_input,
        "contraseña": clave_input
    }

    backend_url = current_app.config.get("BACK_URL")
    login_response = requests.post(f"{backend_url}/datos/login", json=payload)

    # Si el backend confirma el usuario
    if login_response.status_code == 200:
        usuario_data = login_response.json().get("usuario", {})

        # Guardar info en sesión
        session["user_id"] = usuario_data.get("id")
        session["nombre"] = usuario_data.get("nombre")
        session["email"] = usuario_data.get("email")

        # Redirigir a perfil
        return redirect(url_for("perfil_bp.perfil", id_usuario=session["user_id"]))

    # Si el backend devuelve error
    return jsonify({"error": "Credenciales incorrectas"}), 401
