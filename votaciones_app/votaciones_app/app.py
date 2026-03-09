from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'clave_secreta_sena' 

# --- FUNCIÓN PARA CONECTAR A LA BASE DE DATOS ---
def conectar_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="", 
        database="votaciones_db"
    )

# --- RUTA 1: PÁGINA PRINCIPAL ---
@app.route('/')
def index():
    return render_template('index.html')


# --- RUTA 2: REGISTRO DE CIUDADANOS Y PUESTOS (NUEVA) ---
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        # 1. Capturamos los datos del Ciudadano
        documento = request.form['documento']
        nombre = request.form['nombre']
        ciudad = request.form['ciudad']
        telefono = request.form['telefono']
        
        # 2. Capturamos los datos del Puesto de Votación
        lugar_votacion = request.form['lugar_votacion']
        direccion = request.form['direccion']
        mesa = request.form['mesa']
        zona = request.form['zona']
        
        conexion = conectar_db()
        cursor = conexion.cursor()
        
        try:
            # PRIMER PASO: Crear al ciudadano
            sql_ciudadano = "INSERT INTO ciudadanos (documento, nombre, ciudad, telefono) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql_ciudadano, (documento, nombre, ciudad, telefono))
            
            # SEGUNDO PASO: Asignar su puesto de votación
            sql_puesto = "INSERT INTO puestos_votacion (documento, lugar_votacion, direccion, mesa, zona) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql_puesto, (documento, lugar_votacion, direccion, mesa, zona))
            
            # Confirmamos
            conexion.commit()
            flash('¡Registro completado con éxito! Ciudadano y Puesto guardados.')
            
        except Exception as e:
            conexion.rollback() # Deshace si hay error
            flash(f'Error al registrar: {e}')
        finally:
            cursor.close()
            conexion.close()
            
        return redirect(url_for('registro'))
    
    return render_template('registro.html')


# --- RUTA 3: CONSULTA DE PUESTO DE VOTACIÓN ---
@app.route('/consulta', methods=['GET', 'POST'])
def consulta():
    if request.method == 'POST':
        documento = request.form['documento']
        
        conexion = conectar_db()
        cursor = conexion.cursor(dictionary=True) 
        
        try:
            sql = "SELECT documento, lugar_votacion, direccion, mesa, zona FROM puestos_votacion WHERE documento = %s"
            cursor.execute(sql, (documento,))
            resultado = cursor.fetchone()
            
            if resultado:
                return render_template('resultado.html', datos=resultado)
            else:
                flash('No hay información asociada a este documento.')
                
        except Exception as e:
            flash(f'Error al consultar: {e}')
        finally:
            cursor.close()
            conexion.close()
            
    return render_template('consulta.html')


# --- ARRANQUE DE LA APLICACIÓN ---
if __name__ == '__main__':
    app.run(debug=True, port=5001)