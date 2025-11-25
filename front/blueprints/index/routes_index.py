from flask import Blueprint, render_template, current_app
import requests

index_bp = Blueprint("index_bp", __name__)

@index_bp.route("/")
def index():
    back = current_app.config["BACK_URL"]

    try:
        tematicas = requests.get(f"{back}/tematicas").json()
    except:
        tematicas = []

    titulo = "El Portal Literario"

    return render_template("index.html", titulo=titulo, tematicas=tematicas)
