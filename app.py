from flask import request, redirect, url_for, flash
from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from flask_mysqldb import MySQL
from validaciones import *

import requests

app = Flask(__name__)

app.secret_key = 'M0i1Xc$GfPw3Yz@2SbQ9lKpA5rJhDtE7'

app.config['MYSQL_HOST'] = 'sql3.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'sql3683290'
app.config['MYSQL_PASSWORD'] = 'XdlFaDGTnk'
app.config['MYSQL_DB'] = 'sql3683290'

conexion = MySQL(app)


@app.route('/plantas', methods=['GET'])
def listar_plantas():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT id_planta, nombre_comun, nombre_cientifico, region, propiedades FROM Plantas"
        cursor.execute(sql)
        datos = cursor.fetchall()
        plantas = []
        for fila in datos:
            planta = {'id_planta': fila[0], 'nombre_comun': fila[1],
                      'nombre_cientifico': fila[2], 'region': fila[3], 'propiedades': fila[4]}
            plantas.append(planta)
        return jsonify({'plantas': plantas, 'mensaje': "Plantas listadas."})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})


def buscar_planta_por_id(id_planta):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT id_planta, nombre_comun, nombre_cientifico, region, propiedades FROM Plantas WHERE id_planta = '{0}'".format(
            id_planta)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos != None:
            planta = {'id_planta': datos[0], 'nombre_comun': datos[1],
                      'nombre_cientifico': datos[2], 'region': datos[3], 'propiedades': datos[4]}
            return planta
        else:
            return None
    except Exception as ex:
        raise ex


def buscar_planta_por_region(region):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT id_planta, nombre_comun, nombre_cientifico, region, propiedades FROM Plantas WHERE region LIKE '%{0}%'".format(
            region)
        cursor.execute(sql)
        datos = cursor.fetchall()
        if datos:
            plantas = [{'id_planta': d[0], 'nombre_comun': d[1],
                        'nombre_cientifico': d[2], 'region': d[3], 'propiedades': d[4]} for d in datos]
            return plantas
        else:
            return None
    except Exception as ex:
        raise ex


@app.route('/plantas/<identificador>', methods=['GET'])
def buscar_planta(identificador):
    try:
        if identificador.isdigit():
            # Si el identificador es un número, asumimos que es un ID de planta
            planta = buscar_planta_por_id(identificador)
            if planta:
                return jsonify({'planta': planta, 'mensaje': "Planta encontrada.", 'exito': True})
            else:
                return jsonify({'mensaje': "Planta no encontrada.", 'exito': False})
        else:
            # Si el identificador no es un número, asumimos que es el nombre de una región
            plantas_encontradas = buscar_planta_por_region(
                identificador)
            if plantas_encontradas:
                return jsonify({'plantas': plantas_encontradas, 'mensaje': "Plantas encontradas.", 'exito': True})
            else:
                return jsonify({'mensaje': "No se encontraron plantas para la región especificada.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})


@app.route('/plantas', methods=['POST'])
def agregar_planta():
    if (validar_nombre_comun(request.json['nombre_comun']) and validar_nombre_cientifico(request.json['nombre_cientifico']) and validar_region(request.json['region']) and validar_propiedades(request.json['propiedades'])):
        try:
            cursor = conexion.connection.cursor()
            sql = """INSERT INTO Plantas (nombre_comun, nombre_cientifico, region, propiedades) 
            VALUES ('{0}', '{1}', '{2}', '{3}')""".format(request.json['nombre_comun'],
                                                          request.json['nombre_cientifico'],
                                                          request.json['region'],
                                                          request.json['propiedades'])
            cursor.execute(sql)
            # Confirma la acción de inserción.
            conexion.connection.commit()
            return jsonify({'mensaje': "Planta registrada.", 'exito': True})
        except Exception as ex:
            return jsonify({'mensaje': "Error", 'exito': False})
    else:
        return jsonify({'mensaje': "Parámetros inválidos...", 'exito': False})


@app.route('/plantas/<id_planta>', methods=['PUT'])
def actualizar_planta(id_planta):
    if (validar_id(id_planta) and validar_nombre_comun(request.json['nombre_comun']) and validar_nombre_cientifico(request.json['nombre_cientifico']) and validar_region(request.json['region']) and validar_propiedades(request.json['propiedades'])):
        try:
            planta = buscar_planta_por_id(id_planta)
            if planta != None:
                cursor = conexion.connection.cursor()
                sql = """UPDATE Plantas SET nombre_comun = '{0}', nombre_cientifico = '{1}', region = '{2}', propiedades = '{3}'
                WHERE id_planta = '{4}'""".format(request.json['nombre_comun'],
                                                  request.json['nombre_cientifico'],
                                                  request.json['region'],
                                                  request.json['propiedades'], id_planta)
                cursor.execute(sql)
                # Confirma la acción de actualización.
                conexion.connection.commit()
                return jsonify({'mensaje': "Planta actualizada.", 'exito': True})
            else:
                return jsonify({'mensaje': "Planta no encontradab.", 'exito': False})
        except Exception as ex:
            return jsonify({'mensaje': "Error", 'exito': False})
    else:
        return jsonify({'mensaje': "Parámetros inválidos...", 'exito': False})


@app.route('/plantas/<id_planta>', methods=['DELETE'])
def eliminar_planta(id_planta):
    try:
        planta = buscar_planta_por_id(id_planta)
        if planta != None:
            cursor = conexion.connection.cursor()
            sql = "DELETE FROM Plantas WHERE id_planta = '{0}'".format(
                id_planta)
            cursor.execute(sql)
            # Confirma la acción de eliminación.
            conexion.connection.commit()
            return jsonify({'mensaje': "Planta eliminada.", 'exito': True})
        else:
            return jsonify({'mensaje': "Planta no encontrada.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})


# Creamos la ruta para visualizar la página de inicio

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# Creamos la ruta para visualizar los registros de la BD

@app.route('/bandeja', methods=['GET'])
def bandeja():
    cursor = conexion.connection.cursor()
    cursor.execute("SELECT * FROM Plantas")  # ORDER BY quejaID DESC
    datosDB = cursor.fetchall()
    total = cursor.rowcount
    # Convertir los datos a diccionario
    insertObjeto = []
    columnName = [column[0] for column in cursor.description]
    for registro in datosDB:
        insertObjeto.append(dict(zip(columnName, registro)))
    cursor.close()
    return render_template('plantas.html', data=insertObjeto, dataTotal=total)


# Creamos la ruta para visualizar un registro de la BD con el ID

@app.route('/bandeja/<string:id_planta>')
def ver_planta(id_planta):
    cursor = conexion.connection.cursor()
    # Utiliza parámetros seguros en la consulta para evitar SQL injection
    cursor.execute("SELECT * FROM Plantas WHERE id_planta = %s", (id_planta,))
    datosDB = cursor.fetchone()
    # Verifica si la planta existe
    if datosDB:
        # Convertir los datos a diccionario
        column_names = [column[0] for column in cursor.description]
        planta_dict = dict(zip(column_names, datosDB))
        cursor.close()
        return render_template('plantas.html', data=planta_dict)
    else:
        # Maneja el caso donde la planta no existe
        cursor.close()
        return render_template('planta_no_encontrada.html')


# Creamos la ruta para leer la documentacón

@app.route('/documentacion')
def documentacion():
    return render_template('documentacion.html')

# Creamos la ruta para enviar comentarios


@app.route('/comentarios')
def comentarios():
    return render_template('comentarios.html')


# Crear  la ruta para insertar los comentarios en la BD

@app.route('/agregarComentario', methods=['POST'])
def agregarComentario():
    # Obtener los datos del formulario
    nombre = request.form.get("nombre")
    comentario = request.form.get("comentario")

    # Verificar si se recibieron datos válidos
    if nombre and comentario:
        # URL del servicio web de análisis de sentimientos
        url = 'https://h-apiflask1-30f3f4171acf.herokuapp.com/analizar'

        # Datos a enviar en la solicitud POST
        datos = {'texto': comentario}

        # Realizar la solicitud POST al servicio web
        respuesta = requests.post(url, json=datos)

        # Verificar la respuesta del servicio web
        if respuesta.status_code == 200:
            # Obtener los sentimientos del comentario analizado
            sentimientos = respuesta.json()

            # Insertar los datos en la base de datos
            try:
                cursor = conexion.connection.cursor()
                sql = """INSERT INTO Comentarios (nombre, comentario, sentimiento)
                         VALUES (%s, %s, %s)"""
                datos_bd = (nombre, comentario, sentimientos)
                cursor.execute(sql, datos_bd)
                conexion.connection.commit()
                flash("Comentario agregado correctamente", "Exito")
            except Exception as e:
                flash(
                    "Error al agregar comentario a la base de datos: " + str(e), "Error")
                conexion.connection.rollback()
        else:
            flash("Error al analizar el comentario: " + respuesta.text, "Error")
    else:
        flash("Nombre y comentario son campos obligatorios", "Error")

    # Redirigir a la página de comentarios
    return redirect(url_for('comentarios'))


# Creamos una función para las paginas no encontradas

def pagina_no_encontrada(error):
    return "Error", 404


if __name__ == '__main__':
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()
