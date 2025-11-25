from flask import Blueprint, render_template, request

contacto_bp = Blueprint("contacto_bp", __name__)

@contacto_bp.route("/contacto", methods=["GET", "POST"])
def contacto():

    titulo_pagina = "Contacto"

    # Horarios predefinidos (mismo contenido, diferente estilo)
    horarios_biblioteca = {
        "Lunes": "08:30 - 22:00",
        "Martes": "08:30 - 22:00",
        "Miércoles": "08:30 - 22:00",
        "Jueves": "08:30 - 22:00",
        "Viernes": "08:30 - 22:00",
        "Sábado": "Cerrado",
        "Domingo": "Cerrado"
    }

    # ----- POST: procesar formulario -----
    if request.method == "POST":
        datos_form = {
            "nombre": request.form.get("nombre_usuario"),
            "apellido": request.form.get("apellido_usuario"),
            "email": request.form.get("email_usuario"),
            "telefono": request.form.get("telefono_usuario"),
            "mensaje": request.form.get("mensaje_usuario")
        }

        # Renderiza otra plantilla con los datos enviados
        return render_template(
            "formulario_enviado.html",
            titulo="Formulario enviado correctamente",
            info=datos_form
        )

    # ----- GET: mostrar formulario -----
    return render_template(
        "contacto.html",
        titulo=titulo_pagina,
        horarios=horarios_biblioteca
    )
