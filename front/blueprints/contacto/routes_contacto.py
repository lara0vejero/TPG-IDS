from flask import Blueprint, render_template, request

contacto_bp = Blueprint("contacto_bp", __name__)

@contacto_bp.route("/", methods=["GET", "POST"])
def contacto():

    titulo_pagina = "Contacto"

    horarios_biblioteca = {
        "Lunes": "08:30 - 22:00",
        "Martes": "08:30 - 22:00",
        "Miércoles": "08:30 - 22:00",
        "Jueves": "08:30 - 22:00",
        "Viernes": "08:30 - 22:00",
        "Sábado": "Cerrado",
        "Domingo": "Cerrado"
    }

    if request.method == "POST":
        datos_form = {
            "nombre": request.form.get("nombre_usuario"),
            "apellido": request.form.get("apellido_usuario"),
            "email": request.form.get("email_usuario"),
            "telefono": request.form.get("telefono_usuario"),
            "mensaje": request.form.get("mensaje_usuario")
        }

        return render_template(
            "formulario_enviado.html",
            titulo="Formulario enviado correctamente",
            info=datos_form
        )

    return render_template(
        "contacto.html",
        titulo=titulo_pagina,
        horarios=horarios_biblioteca
    )
