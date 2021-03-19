from flask import Flask, render_template, request, flash, url_for, session
from werkzeug.utils import redirect
from flask_mysqldb import MySQL
import pymysql
import bcrypt

# conexion a la base de datos

db = pymysql.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    db = 'agenda'
)

app = Flask(__name__)
api = MySQL(app)

app.secret_key = 'darwin_y_monica'

#Generamos el encriptado
encriptado = bcrypt.gensalt()


def main():
    if 'name' in session:
        #se carga el main del html
        return render_template('page.html')
    else:
        return render_template('index.html')

#definimos la ruta del index
@app.route('/')
def index():
    #verificamos que exista la seccion del usuario
    if 'name' in session:
        return render_template('page.html')
        #cargamos la pagina page
    else:
        return render_template('index.html')

@app.route('/index.html', methods=['GET','POST'])
def register():
    if request.method == 'GET':

        if 'name' in session:
            return render_template('page.html')
        else:        #Acceso no permitido para este usuario
            return render_template('index.html')
    else:
        #obtenemos los datos
        name = request.form['name_register']
        password = request.form['password_register']
        email = request.form['email_register']
        password_encode = password.encode("utf-8")
        password_encript = bcrypt.hashpw(password_encode, encriptado)

        '''print('Agregando datos')
        print('password_encode: ', password_encode)
        print('password_encript', password_encript)'''

        sQuery = "INSER INTO login (name, password, email) VALUES (%s, %s, %s)"

        cursor = db.cursor()
        cursor.execute(sQuery,(name, password_encript, email))
        cursor.connection.commit()

        #procedemos a registrar la sesion
        session['name'] = name
        session['email'] = email

        #redirigimos a index
        return redirect(url_for('page'))

@app.route('/page', methods = ['GET', 'POST'])

def  page():
    if request.method == 'GET':

        if 'name' in session:
            return render_template('page.html')
        else:
            return render_template('index.html')
    else:

        #obtengamos los datos
        email = request.form['name']
        password = request.form['password']
        password_encode = password.encode("utf-8")

        #preparamos el cursor para la ejecucion

        cursor = pymysql.connections.cursor()

        sQuery = "SELECT email, password, name FROM login WHERE email = %s"

        #ejecutamos la sentencia

        cursor.execute(sQuery,[email])

        #obtenemos el dato
        user = cursor.fetchone()

        # cerramos la consulta
        cursor.close()

        #vericamos si se obtuvieron datos
        if (user != None):
            password_encript_encode = user[1].encode()


            print('password_encode', password_encode)
            print('password_encript_encode', password_encript_encode)
             #procedemos a verificar el password del usuario
            if(bcrypt.checkpw(password_encode, password_encript_encode)):

                session['name'] = user[2]
                session['email'] = email

                #redirigimos al page
                return redirect(url_for('page'))
            else:
                flash("Password incorrect, please try other password", "alert-warning")

                #lo redirigimos al index

                return render_template('index.html')
        else:

            flash("The email don't exist, please try with othe email", "alert-warning")

            return render_template('index.html')


#definimos la ruta de salida o logout

@app.route('/logout')
def logout():
    #limpiamos la sesion
    session.clear()

    #redirigimos al index
    return redirect(url_for('index'))

#estos parametros los vamos a utilizaar para editar el contenido de la agenda de ser necesario

@app.route('/edit/<id>')
def get_contact(id):
    cursor = db.cursor()
    cursor.execute('SELECT * FROM contact WHERE id = %s', (id))
    data = cursor.fetchall()
    return render_template('/page.html', contact=data[0])


@app.route('/update/<id>', methods=['POST'])
def update(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cursor = db.cursor()
        cursor.execute('''
            UPDATE contact
            SET fullname = %s,
            email = %s,
            phone = %s
            WHERE id = %s
            ''', (fullname, phone, email, id))
        cursor.connection.commit()
        flash('contact update succesfully')
        return redirect(url_for('index'))


@app.route('/delete/<string:id>')
def delete_contacts(id):
    cursor = db.cursor()
    cursor.execute('DELETE FROM contact WHERE id ={0}'.format(id))
    cursor.connection.commit()
    flash('Contacto eliminado exitosamente')
    return redirect(url_for('index'))


if __name__=='__main__':
    app.run(debug=True)
