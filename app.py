from flask import Flask, jsonify,render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import pymysql
import hashlib
import filetype
import os
import re
import math

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/img'
app.secret_key = 'nicoLASs'

def Connect():
    connection = pymysql.Connection(
        host='localhost',
        user='cc5002',
        password='programacionweb',
        database='tarea2',
        port=3306,
        charset='utf8'
    )
    return connection

def validar_Email(email):
    email_regEx =  r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    return re.fullmatch(email_regEx, email)

def validar_artesano(region, comuna, tipo, nombre, email, celular):
    errors = []
    if not region:
        errors.append("Seleccione una región válida.")
    if not comuna:
        errors.append("Seleccione una comuna válida.")
    if not tipo or len(tipo) > 3 :
        errors.append("Seleccione entre uno o tres tipos de artesania.")
    if not nombre or len(nombre) < 3 or len(nombre) > 80 or type(nombre) != str:
        errors.append("Nombre inválido.")
    if not email or not validar_Email(email):
        errors.append("E-mail inválido.")
    if celular and len(celular) != 9:
        errors.append("Número de celular inválido.")

    return errors

def validar_hincha(deporte, region, comuna, tipo, nombre, email, celular):
    errors = []
    if not deporte or len(deporte) > 3 :
        errors.append("Seleccione entre uno o tres tipos de deporte.")
    if not region:
        errors.append("Seleccione una región válida.")
    if not comuna:
        errors.append("Seleccione una comuna válida.")
    if not tipo :
        errors.append("Seleccione un tipo válido.")
    if not nombre or len(nombre) < 3 or len(nombre) > 80 or type(nombre) != str:
        errors.append("Nombre inválido.")
    if not email or not validar_Email(email):
        errors.append("E-mail inválido.")
    if celular and len(celular) != 9:
        errors.append("Número de celular inválido.")

    return errors

def validate_image(image):
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
    ALLOWED_MIMETYPES = {"image/jpeg", "image/png", "image/gif"}
    MAX_SIZE = 5 * 1024 * 1024 # 5 mb max.

    # check if a file was submitted
    if image is None:
        return False

    # check if the browser submitted an empty file
    if image.filename == "":
        return False
    
    # check file extension
    ftype_guess = filetype.guess(image)
    if ftype_guess.extension not in ALLOWED_EXTENSIONS:
        return False
    # check mimetype
    if ftype_guess.mime not in ALLOWED_MIMETYPES:
        return False
    
    # check image size
    if image.content_length > MAX_SIZE:
        return False

    return True
    
@app.route("/", methods = ['GET'])
@app.route("/index.html", methods = ['GET'])
def index():
    return render_template("index.html")

@app.route("/agregar-hincha",  methods = ['POST', 'GET'])
def agregarHincha():
    if request.method == 'POST':
        deporte = request.form.getlist("sport")
        region = request.form['region']
        comuna = request.form['comuna']
        tipo = request.form['tipo']
        nombre = request.form['nombre']
        email = request.form['email']
        celular = request.form['celular']
        descripcion = request.form['descripcion']

        errors = validar_hincha(deporte, region, comuna, tipo ,nombre, email, celular)

        if errors:
            redirect(url_for('agregarHincha'))
        
        else:
            connection = Connect()
            cur = connection.cursor()
            cur.execute(
                'INSERT INTO hincha (comuna_id, modo_transporte, nombre, email, celular, comentarios) VALUES (%s, %s, %s, %s, %s, %s);', 
                (comuna, tipo, nombre, email, celular, descripcion)
            )
            connection.commit()
            hincha_id = cur.lastrowid
            for t in deporte:
                n = cur.execute('SELECT id FROM deporte WHERE nombre = %s;', (t,))
                result = cur.fetchone()
                if result is not None:
                    deporte_id = result[0]  
                    cur.execute(
                        'INSERT INTO hincha_deporte (hincha_id, deporte_id) VALUES (%s, %s);', 
                        (hincha_id, deporte_id))
                    connection.commit()
            return redirect(url_for('verHinchas'))
    
    elif request.method == 'GET':
        return render_template("agregar-hincha.html")

@app.route("/ver-hinchas", methods=['GET'])
def verHinchas():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    conn = Connect()
    cur = conn.cursor()

    cur.execute('SELECT COUNT(*) FROM hincha')
    total_rows = cur.fetchone()[0]

    num_pages = math.ceil(total_rows / per_page)

    start_idx = (page - 1) * per_page

    cur.execute(
        'SELECT id, comuna_id, modo_transporte, nombre, email, celular, comentarios FROM hincha ORDER BY id DESC LIMIT %s, %s',
        (start_idx, per_page))
    data = cur.fetchall()
    tipo_names = []
    comuna_names = []
    for hincha in data:
        cur.execute('SELECT nombre FROM comuna WHERE id = %s', (hincha[1],))
        comuna_name = cur.fetchone()[0]
        comuna_names.append(comuna_name)

        cur.execute('SELECT deporte_id FROM hincha_deporte WHERE hincha_id=%s', (hincha[0],))
        tipo_ids = cur.fetchall() 

        tipo_names_hinchas = []  
        for tipo_id in tipo_ids:
            cur.execute('SELECT nombre FROM deporte WHERE id = %s', (tipo_id,))
            tipo_name = cur.fetchone()[0]
            tipo_names_hinchas.append(tipo_name)

        tipo_names.append(tipo_names_hinchas)

    return render_template("ver-hinchas.html", hinchas=data, tipo_names=tipo_names,comunas=comuna_names, lenHinchas=len(data),  page=page, per_page=per_page, num_pages=num_pages)

@app.route("/agregar-artesano", methods = ['POST', 'GET'])
def agregarArtesano():
    if request.method == 'POST':
        region = request.form['region']
        comuna = request.form['comuna']
        tipo = request.form.getlist("tipo")
        descripcion = request.form['descripcion']
        nombre = request.form['nombre']
        email = request.form['email']
        celular = request.form['celular']

        errors = validar_artesano(region, comuna, tipo ,nombre, email, celular)

        if errors:
            redirect(url_for('agregarArtesano'))
        
        else:
            connection = Connect()
            cur = connection.cursor()
            cur.execute(
                'INSERT INTO artesano (comuna_id, descripcion_artesania, nombre, email, celular) VALUES (%s, %s, %s, %s, %s);', 
                (comuna, descripcion, nombre, email, celular)
            )
            connection.commit()
            
            artesano_id = cur.lastrowid  
            for t in tipo:
                n = cur.execute('SELECT id FROM tipo_artesania WHERE nombre = %s;', (t,))
                result = cur.fetchone()
                if result is not None:
                    tipo_artesania_id = result[0]  
                    cur.execute('INSERT INTO artesano_tipo (artesano_id, tipo_artesania_id) VALUES (%s, %s);', (artesano_id, tipo_artesania_id))
                    connection.commit()
            print(request.files.getlist("foto"))
            if len(request.files.getlist("foto")) > 0 and len(request.files.getlist("foto")) <= 3:
                for new_img in request.files.getlist("foto"):
                    if validate_image(new_img):
                        _filename = hashlib.sha256(
                            secure_filename(new_img.filename).encode("utf-8")
                        ).hexdigest()
                        _extension = filetype.guess(new_img).extension
                        img_filename = f"{_filename}.{_extension}"

                        new_img.save(os.path.join(app.config["UPLOAD_FOLDER"], img_filename))
                        cur.execute(
                            'INSERT INTO foto (ruta_archivo, nombre_archivo, artesano_id) VALUES (%s, %s, %s);',
                            (os.path.join(app.config["UPLOAD_FOLDER"], img_filename), img_filename, artesano_id)
                        )
                        connection.commit()
            else:
                print("no entró") 
                errors.append("Fotos inválidas.")
                return redirect(url_for('agregarArtesano'))
            return redirect(url_for('verArtesanos'))
    
    elif request.method == 'GET': 
        return render_template("agregar-artesano.html")

@app.route("/ver-artesanos", methods=['GET'])
def verArtesanos():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    conn = Connect()
    cur = conn.cursor()

    cur.execute('SELECT COUNT(*) FROM artesano')
    total_rows = cur.fetchone()[0]

    num_pages = math.ceil(total_rows / per_page)

    start_idx = (page - 1) * per_page

    cur.execute(
        'SELECT id, comuna_id, descripcion_artesania, nombre, email, celular FROM artesano ORDER BY id DESC LIMIT %s, %s',
        (start_idx, per_page))
    data = cur.fetchall()
    tipo_names = []
    comuna_names = []
    images_arr = []
    for artesano in data:
        cur.execute('SELECT nombre FROM comuna WHERE id = %s', (artesano[1],))
        comuna_name = cur.fetchone()[0]
        comuna_names.append(comuna_name)

        cur.execute('SELECT tipo_artesania_id FROM artesano_tipo WHERE artesano_id=%s', (artesano[0],))
        tipo_ids = cur.fetchall() 

        tipo_names_artesano = []  
        for tipo_id in tipo_ids:
            cur.execute('SELECT nombre FROM tipo_artesania WHERE id = %s', (tipo_id,))
            tipo_name = cur.fetchone()[0]
            tipo_names_artesano.append(tipo_name)

        tipo_names.append(tipo_names_artesano)

        cur.execute('SELECT nombre_archivo FROM foto WHERE artesano_id=%s', (artesano[0],))
        image_names = cur.fetchall()
        if image_names is not None:
            images_arr.append([x[0] for x in image_names])
    return render_template('ver-artesanos.html', artesanos=data, tipo_names=tipo_names,comunas=comuna_names, lenArtesanos=len(data), IMAGES=images_arr, page=page, per_page=per_page, num_pages=num_pages)

@app.route("/ver-artesanos/<id>", methods=['GET'])
def informacionArtesano(id):
    connection = Connect()
    cur = connection.cursor()
    cur.execute('SELECT * FROM artesano WHERE id=%s', (id))
    data = cur.fetchall()
    if not data:
        return redirect(url_for('verArtesanos'))
    
    data = data[0]
    comunaID = data[1]

    cur.execute('SELECT nombre, region_id FROM comuna WHERE id=%s', (comunaID))
    comunaYRegion = cur.fetchall()[0]
    comuna = comunaYRegion[0]

    regionID = comunaYRegion[1]
    cur.execute('SELECT nombre FROM region WHERE id=%s', (regionID))
    region = cur.fetchone()[0]

    cur.execute('SELECT tipo_artesania_id FROM artesano_tipo WHERE artesano_id=%s', (id))
    tipo_ids = cur.fetchall()
    tipo_names = []
    for tipo_id in tipo_ids:
        cur.execute('SELECT nombre FROM tipo_artesania WHERE id = %s', (tipo_id,))
        tipo_name = cur.fetchone()[0]
        tipo_names.append(tipo_name)
    
    images_arr = []
    cur.execute('SELECT nombre_archivo FROM foto WHERE artesano_id=%s', (id,))
    image_names = cur.fetchall()
    if image_names:
        images_arr = [x[0] for x in image_names]
    lenImages = len(images_arr)
    return render_template('informacion-artesano.html', tipo=tipo_names ,artesanos=data, region=region, comuna=comuna, IMAGES=images_arr, lenImages=lenImages)

@app.route("/ver-hinchas/<id>", methods=['GET'])
def informacionHincha(id):
    connection = Connect()
    cur = connection.cursor()
    cur.execute('SELECT * FROM hincha WHERE id=%s', (id))
    data = cur.fetchall()
    if not data:
        return redirect(url_for('verHinchas'))
    
    data = data[0]
    comunaID = data[1]

    cur.execute('SELECT nombre, region_id FROM comuna WHERE id=%s', (comunaID))
    comunaYRegion = cur.fetchall()[0]
    comuna = comunaYRegion[0]

    regionID = comunaYRegion[1]
    cur.execute('SELECT nombre FROM region WHERE id=%s', (regionID))
    region = cur.fetchone()[0]

    cur.execute('SELECT deporte_id FROM hincha_deporte WHERE hincha_id=%s', (id))
    tipo_ids = cur.fetchall()
    tipo_names = []
    for tipo_id in tipo_ids:
        cur.execute('SELECT nombre FROM deporte WHERE id = %s', (tipo_id,))
        tipo_name = cur.fetchone()[0]
        tipo_names.append(tipo_name)
    
    return render_template('informacion-hincha.html', tipo=tipo_names ,hinchas=data, region=region, comuna=comuna)

# Obtener los tipos de hinchas y la cantidad de cada uno
@app.route("/get-hinchas-tipo")
def get_hinchas_data_all():
    conn = Connect()
    cur = conn.cursor()
    cur.execute('SELECT d.nombre as nombre_deporte, COUNT(*) as total FROM hincha_deporte hd JOIN deporte d ON hd.deporte_id = d.id GROUP BY hd.deporte_id;')
    deportes_hinchas = cur.fetchall()
    markers = []
    for deportes_hincha, total in deportes_hinchas:
        markers.append({
            "tipo_hincha": deportes_hincha,
            "total": total
        })
    
    return jsonify(markers)

# Obtener los tipos de artesanos y la cantidad de cada uno
@app.route("/get-artesanos-tipo")
def get_artesanos_data_all():
    conn = Connect()
    cur = conn.cursor()
    cur.execute('SELECT ta.nombre as nombre_tipo_artesania, COUNT(*) as total FROM artesano_tipo at JOIN tipo_artesania ta ON at.tipo_artesania_id = ta.id GROUP BY at.tipo_artesania_id;')
    tipos_artesanos = cur.fetchall()
    markers = []
    for tipo_artesano, total in tipos_artesanos:
        markers.append({
            "tipo_artesano": tipo_artesano,
            "total": total
        })
    
    return jsonify(markers)

# Ruta para mostrar los graficos
@app.route("/graficos", methods = ['GET'])
def graficos():
    return render_template('graficos.html')

if __name__ == '__main__':
    app.run(debug = True)