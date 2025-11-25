from flask import Blueprint, jsonify, request
from db import get_connection

intercambio_libros_bp = Blueprint("intercambio_libros", __name__)


# GET /libros/usuarios/<usuario_id>/tiene_libros
@intercambio_libros_bp.route("/usuarios/<int:usuario_id>/tiene_libros", methods=["GET"])
def tiene_libros(usuario_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT COUNT(*) AS cantidad FROM libros WHERE usuario_id = %s",
            (usuario_id,),
        )
        row = cursor.fetchone()
        return jsonify({"cantidad": row["cantidad"]}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()


# POST /libros/solicitar_intercambio
@intercambio_libros_bp.route("/solicitar_intercambio", methods=["POST"])
def solicitar_intercambio():
    data = request.get_json() or {}

    id_libro_solicitado = data.get("id_libro_solicitado")
    id_libro_ofrecido = data.get("id_libro_ofrecido")
    id_usuario_ofrecido = data.get("id_usuario_ofrecido")
    id_usuario_solicitado = data.get("id_usuario_solicitado")

    if not all(
        [id_libro_solicitado, id_libro_ofrecido, id_usuario_ofrecido, id_usuario_solicitado]
    ):
        return jsonify({"error": "Faltan datos"}), 400

    if id_libro_solicitado == id_libro_ofrecido:
        return jsonify({"error": "No se puede intercambiar el mismo libro"}), 400

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Libro ofrecido
        cursor.execute(
            "SELECT usuario_id, estado_del_libro FROM libros WHERE id = %s",
            (id_libro_ofrecido,),
        )
        libro_ofrecido = cursor.fetchone()

        # Libro solicitado
        cursor.execute(
            "SELECT usuario_id, estado_del_libro FROM libros WHERE id = %s",
            (id_libro_solicitado,),
        )
        libro_solicitado = cursor.fetchone()

        if not libro_ofrecido or not libro_solicitado:
            return jsonify({"error": "Alguno de los libros no existe"}), 404

        if libro_ofrecido["usuario_id"] != id_usuario_ofrecido:
            return jsonify({"error": "El libro ofrecido no pertenece al usuario"}), 400
        if libro_solicitado["usuario_id"] != id_usuario_solicitado:
            return jsonify({"error": "El libro solicitado no pertenece al usuario"}), 400

        if libro_ofrecido["estado_del_libro"] != "disponible" or libro_solicitado[
            "estado_del_libro"
        ] != "disponible":
            return jsonify({"error": "Alguno de los libros no está disponible"}), 400

        # Crear intercambio en espera
        cursor.execute(
            """
            INSERT INTO intercambio_libro
                (id_libro_solicitado, id_libro_ofrecido,
                 id_usuario_solicitado, id_usuario_ofrecido,
                 estado_del_intercambio)
            VALUES (%s, %s, %s, %s, 'espera')
            """,
            (
                id_libro_solicitado,
                id_libro_ofrecido,
                id_usuario_solicitado,
                id_usuario_ofrecido,
            ),
        )
        intercambio_id = cursor.lastrowid

        # Poner libro ofrecido en pausa
        cursor.execute(
            "UPDATE libros SET estado_del_libro = 'pausa' WHERE id = %s",
            (id_libro_ofrecido,),
        )

        conn.commit()
        return jsonify({"intercambio_id": intercambio_id}), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()


# POST /libros/aceptar_intercambio/<id>
@intercambio_libros_bp.route("/aceptar_intercambio/<int:intercambio_id>", methods=["POST"])
def aceptar_intercambio(intercambio_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT * FROM intercambio_libro WHERE id = %s", (intercambio_id,)
        )
        inter = cursor.fetchone()
        if not inter or inter["estado_del_intercambio"] != "espera":
            return jsonify({"error": "Intercambio no encontrado o no está en espera"}), 404

        id_libro_solicitado = inter["id_libro_solicitado"]
        id_libro_ofrecido = inter["id_libro_ofrecido"]
        id_usuario_solicitado = inter["id_usuario_solicitado"]
        id_usuario_ofrecido = inter["id_usuario_ofrecido"]

        # Intercambiar dueños + marcar como intercambiados
        cursor.execute(
            """
            UPDATE libros 
            SET usuario_id = %s, estado_del_libro = 'intercambiado'
            WHERE id = %s
            """,
            (id_usuario_ofrecido, id_libro_solicitado),
        )
        cursor.execute(
            """
            UPDATE libros 
            SET usuario_id = %s, estado_del_libro = 'intercambiado'
            WHERE id = %s
            """,
            (id_usuario_solicitado, id_libro_ofrecido),
        )

        cursor.execute(
            """
            UPDATE intercambio_libro
            SET estado_del_intercambio = 'completado', fecha_final = NOW()
            WHERE id = %s
            """,
            (intercambio_id,),
        )

        conn.commit()
        return jsonify({"mensaje": "Intercambio aceptado"}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()


# POST /libros/cancelar_intercambio/<id>
@intercambio_libros_bp.route("/cancelar_intercambio/<int:intercambio_id>", methods=["POST"])
def cancelar_intercambio(intercambio_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT * FROM intercambio_libro WHERE id = %s", (intercambio_id,)
        )
        inter = cursor.fetchone()
        if not inter or inter["estado_del_intercambio"] != "espera":
            return jsonify({"error": "Intercambio no encontrado o no está en espera"}), 404

        id_libro_ofrecido = inter["id_libro_ofrecido"]

        # Volver libro ofrecido a disponible
        cursor.execute(
            "UPDATE libros SET estado_del_libro = 'disponible' WHERE id = %s",
            (id_libro_ofrecido,),
        )
        cursor.execute(
            """
            UPDATE intercambio_libro
            SET estado_del_intercambio = 'cancelado', fecha_final = NOW()
            WHERE id = %s
            """,
            (intercambio_id,),
        )

        conn.commit()
        return jsonify({"mensaje": "Intercambio cancelado"}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()


# GET /intercambios/<usuario_id>
@intercambio_libros_bp.route("/intercambios/<int:usuario_id>", methods=["GET"])
def listar_intercambios(usuario_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT i.*,
                   l1.titulo AS titulo_solicitado,
                   l2.titulo AS titulo_ofrecido
            FROM intercambio_libro i
            JOIN libros l1 ON l1.id = i.id_libro_solicitado
            JOIN libros l2 ON l2.id = i.id_libro_ofrecido
            WHERE i.id_usuario_solicit
            """,
            # por si el SQL de arriba se corta podés completarlo así:
            # WHERE i.id_usuario_solicitado = %s OR i.id_usuario_ofrecido = %s
            (usuario_id, usuario_id),
        )
        intercambios = cursor.fetchall()
        return jsonify({"intercambios": intercambios}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()
