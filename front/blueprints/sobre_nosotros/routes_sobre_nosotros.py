from flask import Blueprint, render_template

sobre_nosotros_bp = Blueprint("sobre_nosotros_bp", __name__)

@sobre_nosotros_bp.route("/sobre_nosotros")
def sobre_nosotros():
    titulo = "Sobre Nosotros"
    return render_template("sobre_nosotros.html", titulo=titulo)
