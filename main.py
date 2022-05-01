from flask import Flask, jsonify,request
from conexion import crear_usuario, get_contactos, iniciar_sesion, insertar_contacto

from conexion import insertar_contacto, get_contacto, get_contacto

from conexion import modificar_contacto, eliminar_contacto

from conexion import get_contacto_usuario

app = Flask(__name__)

@app.route("/api/v1/usuarios", methods = ["POST", "GET"])
@app.route("/api/v1/usuarios/<int:usuarioId>/contacto", methods = ["GET"])
@app.route("/api/v1/usuarios/<intd:usuarioId>/contacto/<int:id>", methods =["GET"])

def usuario(usuarioId = None,id = None):
    if request.method == "POST" and request.is_json:
        try:
            data = request.get_json()
            print(data)

            if crear_usuario(data["correo_usuario"], data["contrasena"]):
                return jsonify({"code": "ok"})
            else:
                return jsonify({"code": "existe"})
        except:
            return jsonify({"code": "error"})

    elif request.method == "GET" and id is not None:
        return jsonify(get_contacto_usuario(id))

@app.route("/api/v1/sesiones", methods = ["POST"])

def sesion():
    if request.method == "POST" and request.is_json:
        try:
            data = request.get_json()
            correo_usuario = data["correo_usuario"]
            contrasena = data["contrasena"]
            print(correo_usuario, contrasena)
            id, ok = iniciar_sesion(correo_usuario, contrasena)
            if ok:
                return jsonify({"code": "ok", "id": id})
            else:
                return jsonify({"code": "noexiste"})
        except:
            return jsonify({"code": "error"})

@app.route("/api/v1/contactos", methods = ["GET","POST"])
# @app.route("/api/v1/contactos/<int:usuarioId>", methods = ["GET", "PATCH", "DELETE"])
@app.route("/api/v1/contactos/<int:usuarioId>/<int:id>", methods = ["GET", "PATCH", "DELETE"])


def contacto(usuarioId=None, id=None):
    
    if request.method == "POST" and request.is_json:
        try: 
            data = request.get_json()
            print(data)
            if insertar_contacto(data):
                return jsonify({"code": "ok"})
            else: 
                return jsonify({"code": "no"})
        except:
            return jsonify({"code": "error"})

    elif request.method == "GET" and usuarioId is None and id is None:
        return jsonify(get_contactos())

    elif request.method == "GET" and usuarioId is not None and id is None:
        return jsonify(get_contacto(usuarioId))


    elif request.method == "GET" and usuarioId is not None and id is not None:
        return jsonify(get_contacto_usuario(usuarioId, id))

  

    elif request.method == "PATCH" and usuarioId is not None and request.is_json:
        data = request.get_json()
        columna = data['columna']
        valor = data['valor']

        if modificar_contacto(usuarioId, columna, valor):
            return jsonify(code='ok')
        else:
            return jsonify(code='error')

    elif request.method == "DELETE" and usuarioId is not None:
        if eliminar_contacto(usuarioId):
            return jsonify(code='ok')
        else:
            return jsonify(code='ok')


# @app.route("/api/v1/contactos/<int:id>/<int:id>", methods = ["GET"])
# def usuario_contacto(usuarioId=None, id=None):
#     if request.method == "POST" and request.is_json:
#         try: 
#             data = request.get_json()
#             print(data)
#             if insertar_contacto(data):
#                 return jsonify({"code": "ok"})
#             else: 
#                 return jsonify({"code": "no"})
#         except:
#             return jsonify({"code": "error"})
#     if request.method == "GET" and usuarioId and id is not None:
#         return jsonify(get_contacto(usuarioId,id))


app.run(debug = True)