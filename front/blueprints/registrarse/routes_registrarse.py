from flask import Blueprint, render_template, request, redirect, url_for, current_app, jsonify
import requests

registrarse_bp = Blueprint("registrarse_bp", __name__)

@registrarse_bp.route("/registrarse", methods=["GET", "POST"])
def registrarse():

    titulo = "Registrarse"
    BACK_URL = current_app.config.get("BACK_URL")

    # ---------- GET: mostrar formulario ----------
    if request.method == "GET":
        return render_template("registrarse.html", titulo=titulo)

    # ---------- POST: procesar registro ----------
    usuario = request.form.get("nombre_usuario")
    mail = request.form.get("email_registro")
    mail_conf = request.form.get("email_confirmacion")
    contrasena = request.form.get("contrasena_registro")
    telefono = request.form.get("telefono_usuario")
    direccion = request.form.get("direccion_usuario")
    dni = request.form.get("dni_usuario")

    # ------- Validaciones básicas -------
    if not all([usuario, mail, mail_conf, contrasena]):
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    if mail != mail_conf:
        return jsonify({"error": "Los mails no coinciden"}), 400

    # ------- Datos listos para enviar al backend -------
    data = {
        "nombre": usuario,
        "email": mail,
        "contrasena": contrasena,
        "telefono": telefono,
        "direccion": direccion,
        "dni": dni
    }

    # ------- Enviar al backend -------
    if BACK_URL:
        requests.post(f"{BACK_URL}/datos/registrar", json=data)

    # ------- Redirigir al login -------
    return redirect(url_for("iniciar_sesion_bp.iniciar_sesion"))
