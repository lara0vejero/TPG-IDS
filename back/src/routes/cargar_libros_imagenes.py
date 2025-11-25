import os
from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename
from db import get_connection

carga_libros_imagenes_bp = Blueprint("carga_libros_imagenes", __name__)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "images")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# POST /libros/<libro_id>/subir_imagen
@carga_libros_imagenes_bp.route("/<int:libro_id>/subir_imagen", methods=["POST"])
def subir_imagen(libro_id):
    if "imagen" not in request.files:
        return jsonify({"error": "No se envió archivo"}), 400

    file = request.files["imagen"]
    if file.filename == "":
        return jsonify({"error": "Nombre de archivo vacío"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Extensión no permitida"}), 400

    filename = secure_filename(file.filename)
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)

    coneccion = get_connection()
    cursor = coneccion.cursor()

    try:
        cursor.execute(
            "UPDATE libros SET imagen = %s WHERE id = %s",
            (filename, libro_id),
        )
        coneccion.commit()
        return jsonify(
            {
                "mensaje": "Imagen subida",
                "imagen_url": f"static/images/{filename}",
            }
        ), 200

    except Exception as e:
        coneccion.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        coneccion.close()
