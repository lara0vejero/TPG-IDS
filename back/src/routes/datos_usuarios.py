from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_connection

datos_usuarios_bp = Blueprint("datos_usuarios", __name__)

@datos_usuarios_bp.route("/registrar", methods=["POST"])
def registrar_usuario():
    data = request.get_json(silent=True) or request.form.to_dict()

    nombre = data.get("nombre_usuario")
    email = data.get("email_usuario")
    contraseña = data.get("contraseña_usuario")
    telefono = data.get("telefono_usuario")
    direccion = data.get("direccion_usuario")
    dni = data.get("dni_usuario")


    if not all([nombre, email, contraseña, telefono, direccion]):
        return jsonify({"error": "Faltan datos"}), 400
    coneccion = get_connection()
    cursor = coneccion.cursor(dictionary=True)
    try:
        # Verificar duplicado por email o nombre
        cursor.execute(
            """
            SELECT id 
            FROM datos_usuario 
            WHERE email_usuario = %s OR nombre_usuario = %s
            """,
            (email, nombre),
        )
        mail_existente = cursor.fetchone()
        if mail_existente:
            return jsonify({"error": "Usuario o email ya registrado"}), 400
        contraseña_hash = generate_password_hash(contraseña)

        cursor.execute(
            """
            INSERT INTO datos_usuario
                (nombre_usuario, email_usuario, contraseña_usuario,
                 telefono_usuario, direccion_usuario, dni_usuario)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (nombre, email, contraseña_hash, telefono, direccion, dni),
        )
        coneccion.commit()
        user_id = cursor.lastrowid

        return jsonify({"user_id": user_id}), 201
    except Exception as e:
        coneccion.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        coneccion.close()

@datos_usuarios_bp.route("/login", methods=["POST"])
def login_usuario():
    data = request.get_json() or {}
    identificador = data.get("identificador")  # puede ser email o nombre
    contraseña = data.get("contraseña")

    if not identificador or not contraseña:
        return jsonify({"error": "Faltan datos"}), 400

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT * 
            FROM datos_usuario
            WHERE email_usuario = %s OR nombre_usuario = %s
            """,
            (identificador, identificador),
        )
        usuario = cursor.fetchone()

        if not usuario or not check_password_hash(
            usuario["contraseña_usuario"], contraseña
        ):
            return jsonify({"error": "Credenciales inválidas"}), 401
        return jsonify(
            {
                "id": usuario["id"],
                "nombre": usuario["nombre_usuario"],
                "email": usuario["email_usuario"],
            }
        ), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()


# GET /datos/<id>
@datos_usuarios_bp.route("/<int:usuario_id>", methods=["GET"])
def obtener_usuario(usuario_id):
    coneccion = get_connection()
    cursor = coneccion.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT id, nombre_usuario, email_usuario,
                   telefono_usuario, direccion_usuario, dni_usuario
            FROM datos_usuario
            WHERE id = %s
            """,
            (usuario_id,),
        )
        usuario = cursor.fetchone()
        if not usuario:
            return jsonify({"error": "Usuario no encontrado"}), 404
        return jsonify(usuario), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        coneccion.close()
