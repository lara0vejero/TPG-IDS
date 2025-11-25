from flask import Blueprint, jsonify, request
from db import get_connection

cargar_libros_bp = Blueprint("cargar_libros", __name__)

@cargar_libros_bp.route('/cargar', methods=['POST'])
def cargar_libro_nuevo():
    data = request.get_json() or {}
    titulo = data.get('titulo')
    autor = data.get('autor')
    codigo_isbn = data.get('codigo_isbn')
    usuario_id = data.get('usuario_id')
    editorial = data.get('editorial')
    tematica = data.get('tematica')

    if not all([titulo, autor, editorial, codigo_isbn, tematica, usuario_id]):
        return jsonify({"error": "Faltan datos"}), 400
    
    coneccion = get_connection()
    cursor = coneccion.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            INSERT INTO libros
                (usuario_id, titulo, autor, editorial, codigo_isbn, tematica, estado_del_libro, imagen)
            VALUES (%s, %s, %s, %s, %s, %s, 'disponible', %s)
            """,
            (usuario_id, titulo, autor, editorial, codigo_isbn, tematica, "default.png"),
        )
        coneccion.commit()
        libro_id = cursor.lastrowid

        return jsonify({"libro_id": libro_id}), 201

    except Exception as e:
        coneccion.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        coneccion.close()




@cargar_libros_bp.route('/mis-libros/<int:usuario_id>', methods=['GET'])
def obtener_mis_libros(usuario_id):
    coneccion = get_connection()
    cursor = coneccion.cursor(dictionary=True)
    
    try:
        cursor.execute(
            """
            SELECT *
            FROM libros
            WHERE usuario_id = %s
            ORDER BY fecha_carga DESC
            """,
            (usuario_id,),
        )
        libros = cursor.fetchall()
        return jsonify({"libros": libros}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        coneccion.close()




@cargar_libros_bp.route("/eliminar/<int:libro_id>", methods=["DELETE"])
def eliminar_libro(libro_id):
    data = request.get_json() or {}
    usuario_id = data.get("usuario_id")

    if not usuario_id:
        return jsonify({"error": "Falta usuario_id"}), 400

    coneccion = get_connection()
    cursor = coneccion.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT usuario_id, estado_del_libro FROM libros WHERE id = %s",
            (libro_id,),
        )
        libro = cursor.fetchone()

        if not libro or libro["usuario_id"] != usuario_id:
            return jsonify(
                {"error": "Libro no encontrado o no te pertenece"}
            ), 404

        if libro["estado_del_libro"] != "disponible":
            return jsonify(
                {"error": "Solo se pueden eliminar libros disponibles"}
            ), 400

        cursor.execute("DELETE FROM libros WHERE id = %s", (libro_id,))
        coneccion.commit()

        return jsonify({"mensaje": "Libro eliminado"}), 200

    except Exception as e:
        coneccion.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        coneccion.close()
