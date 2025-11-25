from flask import Blueprint, render_template

index_bp = Blueprint("index_bp", __name__)

@index_bp.route("/")
def index():
    titulo = "El Portal Literario"
    return render_template("index.html", titulo=titulo)
