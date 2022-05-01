import mysql.connector
import hashlib


bd = mysql.connector.connect(
    user='edgar',password='12345678',
    database='agenda_prueba')

cursor = bd.cursor()

def get_usuario():
    consulta = "SELECT * FROM usuario"

    cursor.execute(consulta)
    usuarios = []
    for row in cursor.fetchall():
        usuario = {
            'id': row[0],
            'correo_usuario': row[1],
            'contrasena': row[2]
        }
        usuarios.append(usuario)
    return usuarios

def existe_usuario(correo_usuario):
    query = "SELECT COUNT(*) FROM usuario WHERE correo_usuario =%s"
    cursor.execute(query,(correo_usuario,))

    if cursor.fetchone()[0] == 1:
        return True
    else:
        return False


def crear_usuario(correo_usuario, contrasena):
    if existe_usuario(correo_usuario):
        return False
    else:
        h = hashlib.new("sha256", bytes(contrasena, "utf-8")) 
        h = h.hexdigest() 
        insertar = "INSERT INTO usuario(correo_usuario, contrasena) VALUES(%s, %s)"
        cursor.execute(insertar, (correo_usuario, h))

        bd.commit()
        return True

def iniciar_sesion(correo_usuario, contrasena):
    h = hashlib.new("sha256", bytes(contrasena, "utf-8")) 
    h = h.hexdigest()
    query = "SELECT id FROM usuario WHERE correo_usuario = %s AND contrasena = %s"
    cursor.execute(query, (correo_usuario, h))
    identificacion = cursor.fetchone()
    if identificacion:
        return identificacion[0], True
    else:
        return None, False

def insertar_contacto(contacto):
    nombre = contacto['nombre']
    telefono = contacto['telefono']
    correo_contacto  = contacto['correo_contacto']
    facebook = contacto['facebook']
    linkedin = contacto['linkedin']
    twitter = contacto['twitter']
    foto = contacto['foto']
    usuarioId = contacto['usuarioId']

    insertar = "INSERT INTO contacto \
        (nombre, telefono, correo_contacto, facebook, linkedin, twitter,foto, usuarioId) \
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(insertar,(nombre, telefono, correo_contacto, facebook, linkedin, twitter, foto, usuarioId))
    bd.commit()

    if cursor.rowcount:
        return True
    else:
        return False

def get_contactos():
    query = "SELECT id, nombre, telefono, correo_contacto, facebook, linkedin, twitter, foto FROM contacto"
    cursor.execute(query)
    contactos = []
    for row in cursor.fetchall():
        contacto = {
            'id': row[0],
            'nombre': row[1],
            'telefono': row[2],
            'correo_contacto': row[3],
            'facebook' : row[4],
            'linkedin': row[5],
            'twitter': row[6],
            'foto': row[7],
        }
        contactos.append(contacto)

    return contactos

def get_contacto(usuarioId,):
    query = "SELECT * FROM contacto WHERE usuarioId =%s "
    cursor.execute(query, (usuarioId,))
    contacto = {}
    row = cursor.fetchone()
    if row: 
        contacto['id'] = row[0]
        contacto['nombre'] = row[1]
        contacto['telefono'] = row[2]
        contacto['correo_contacto'] = row[3]
        contacto['facebook'] = row[4]
        contacto['linkedin'] = row[5]
        contacto['twitter'] = row[6]
        contacto['foto'] = row[7]
    return contacto

def get_contacto_usuario(usuarioId, id):
    query = "SELECT * FROM contacto WHERE usuarioId =%s and id = %s"
    cursor.execute(query, (usuarioId,id,))
    contacto = {}
    row = cursor.fetchone()
    if row: 
        contacto['id'] = row[0]
        contacto['nombre'] = row[1]
        contacto['telefono'] = row[2]
        contacto['correo_contacto'] = row[3]
        contacto['facebook'] = row[4]
        contacto['linkedin'] = row[5]
        contacto['twitter'] = row[6]
        contacto['foto'] = row[7]
    return contacto

def modificar_contacto(usuarioId,id, columna, valor):
    update = f"UPDATE contacto SET {columna} = %s WHERE id = %s"
    cursor.execute(update, (valor, id))
    bd.commit()

    if cursor.rowcount:
        return True
    else:
        return False

def eliminar_contacto(usuarioId,id):
    eliminar = "DELETE from contacto WHERE id = %s"
    cursor.execute(eliminar, (id,))
    bd.commit()

    if cursor.rowcount:
        return True
    else:
        return False

def get_contacto_usuario(usuarioId, id):
    query = "SELECT * FROM contacto WHERE usuarioId = %s"
    cursor.execute(query, (id,))
    contactos = []
    for row in cursor.fetchall():
        contacto = {
            'id': row[0],
            'nombre': row[1],
            'telefono': row[2],
            'correo_contacto': row[3],
            'facebook' : row[4],
            'linkedin': row[5],
            'twitter': row[6],
            'foto': row[7],
        }
        contactos.append(contacto)
    return contactos