from flask import Blueprint, render_template, request, redirect, url_for, current_app, flash
import requests

registrarse_bp = Blueprint("registrarse_bp", __name__)

@registrarse_bp.route("/registrarse", methods=["GET", "POST"])
def registrarse():

    titulo = "Registrarse"
    BACK_URL = current_app.config.get("BACK_URL")

    if request.method == "GET":
        return render_template("registrarse.html", titulo=titulo)

    # ---------- POST ----------
    usuario = request.form.get("nombre_usuario")
    mail = request.form.get("email_usuario")
    mail_conf = request.form.get("email_confirmacion")
    contrasena = request.form.get("contraseña_usuario")
    telefono = request.form.get("telefono_usuario")
    direccion = request.form.get("direccion_usuario")
    dni = request.form.get("dni_usuario")

    # Validación de campos obligatorios
    if not all([usuario, mail, mail_conf, contrasena, telefono, direccion, dni]):
        flash("Faltan campos obligatorios", "error")
        return redirect(url_for("registrarse_bp.registrarse"))

    if mail != mail_conf:
        flash("Los correos no coinciden", "error")
        return redirect(url_for("registrarse_bp.registrarse"))

    # Datos a enviar al backend
    data = {
        "nombre_usuario": usuario,
        "email_usuario": mail,
        "contraseña_usuario": contrasena,
        "telefono_usuario": telefono,
        "direccion_usuario": direccion,
        "dni_usuario": dni
    }

    # Enviar datos al backend
    try:
        response = requests.post(f"{BACK_URL}/datos/registrar", data=data)

        if response.status_code == 201:
            return redirect(url_for("iniciar_sesion_bp.iniciar_sesion"))
        else:
            flash("Hubo un error al registrarte: " + response.text, "error")
            return redirect(url_for("registrarse_bp.registrarse"))

    except Exception as e:
        flash(f"Error de conexión con el servidor: {e}", "error")
        return redirect(url_for("registrarse_bp.registrarse"))
