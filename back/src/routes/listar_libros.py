from flask import Blueprint, jsonify, request
from db import get_connection

listar_libros_bp = Blueprint("listar_libros", __name__)

@listar_libros_bp.route("/libros", methods=["GET"])
def listar_libros():
    usuario_id = request.args.get("usuario_id", type=int)
    coneccion = get_connection()
    cursor = coneccion.cursor(dictionary=True)
    try:
        sql = """
            SELECT *
            FROM libros
            WHERE estado_del_libro = 'disponible'
        """
        params = []
        if usuario_id:
            sql += " AND usuario_id <> %s"
            params.append(usuario_id)

        sql += " ORDER BY fecha_carga DESC"

        cursor.execute(sql, params)
        libros = cursor.fetchall()

        # agregar URL de imagen si hay
        for libro in libros:
            if libro.get("imagen"):
                libro["imagen_url"] = f"/static/images/{libro['imagen']}"

        return jsonify({"libros": libros}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        coneccion.close()

# GET /libros/libros/<libro_id>
@listar_libros_bp.route("/libros/<int:libro_id>", methods=["GET"])
def obtener_libro(libro_id):
    coneccion = get_connection()
    cursor = coneccion.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM libros WHERE id = %s", (libro_id,))
        libro = cursor.fetchone()
        if not libro:
            return jsonify({"error": "Libro no encontrado"}), 404

        if libro.get("imagen"):
            libro["imagen_url"] = f"/static/images/{libro['imagen']}"

        return jsonify(libro), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        coneccion.close()


# GET /libros/buscar?q=...
@listar_libros_bp.route("/buscar", methods=["GET"])
def buscar_libros():
    q = request.args.get("q", "").strip()
    if not q:
        return jsonify({"libros": []}), 200

    coneccion = get_connection()
    cursor = coneccion.cursor(dictionary=True)

    try:
        like = f"%{q}%"
        cursor.execute(
            """
            SELECT *
            FROM libros
            WHERE estado_del_libro = 'disponible'
              AND (
                    titulo LIKE %s OR
                    autor LIKE %s OR
                    editorial LIKE %s OR
                    codigo_isbn LIKE %s OR
                    tematica LIKE %s
                  )
            ORDER BY fecha_carga DESC
            """,
            (like, like, like, like, like),
        )
        libros = cursor.fetchall()
        for libro in libros:
            if libro.get("imagen"):
                libro["imagen_url"] = f"/static/images/{libro['imagen']}"

        return jsonify({"libros": libros}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        coneccion.close()
