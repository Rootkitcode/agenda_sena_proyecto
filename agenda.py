from flask import Flask, render_template, request, flash, url_for, session, jsonify
from werkzeug.utils import redirect
from flask_mysqldb import MySQL
import pymysql
import bcrypt

# conexion a la base de datos

db = pymysql.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    db = 'login'
)

app = Flask(__name__)
api = MySQL(app)

app.secret_key = 'darwin_y_monica'

#Generamos el encriptado
encriptado = bcrypt.gensalt()

#defino la ruta principal

@app.route('/')


def main():
    if 'name' in session:
        return render_template('inicio.html')
    else:


        return render_template('ingresar.html')

#definimos la ruta del index
@app.route('/inicio')
def inicio():
    if 'name' in session:
        return render_template('inicio.html')
    else:

    #verificamos que exista la seccion del usuario

        return render_template('ingresar.html')

@app.route('/registrar', methods=['GET','POST'])
def registrar():
    if (request.method == 'GET'):

        if 'name' in session:
            return render_template('inicio.html')
        else:        #Acceso no permitido para este usuario
            return render_template('ingresar.html')
    else:
        #obtenemos los datos
        name = request.form['nameregister']
        last = request.form['lastnames']
        phone = request.form['phoneregister']
        ocupation = request.form['ocupationregister']
        age = request.form['ageregister']
        addres = request.form['addresregister']
        company = request.form['companynameregister']
        document = request.form['documentregister']
        email = request.form['emailregister']
        password = request.form['passwordregister']
        password_encode = password.encode("utf-8")
        password_encript = bcrypt.hashpw(password_encode, encriptado)

        '''print('Agregando datos')
        print('password_encode: ', password_encode)
        print('password_encript', password_encript)'''

        sQuery = "INSERT INTO login (name, last, phone, ocupation, age, addres, company, document, email, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        cursor = db.cursor()
        cursor.execute(sQuery,(name, last, phone, ocupation, age, addres, company,
                               document, email, password_encript))
        cursor.connection.commit()

        #procedemos a registrar la sesion
        session['name'] = name
        #session['email'] = email

        #redirigimos a la pagina
        return redirect(url_for('inicio'))

    #definimos la ruta de ingresar

@app.route('/ingresar', methods = ['GET', 'POST'])

def  ingresar():
    if request.method == 'GET':

        if 'name' in session:
            return render_template('inicio.html')
        else:
            return render_template('ingresar.html')
    else:

        #obtengamos los datos
        email = request.form['emaillogin']
        password = request.form['passwordlogin']
        password_encode = password.encode("utf-8")

        #preparamos el cursor para la ejecucion

        #cursor = pymysql.connections.cursor()

        sQuery = "SELECT email, password, name FROM login WHERE email = %s"

        #ejecutamos la sentencia
        cursor = db.cursor()
        cursor.execute(sQuery,[email])

        #obtenemos el dato
        user = cursor.fetchone()

        # cerramos la consulta
        cursor.close()

        #vericamos si se obtuvieron datos
        if (user !=None):
            password_encript_encode = user[1].encode()

             #procedemos a verificar el password del usuario

            if(bcrypt.checkpw(password_encode, password_encript_encode)):

                #registramos la sesion

                session['name'] = user[2]
                #session['email'] = email

                #redirigimos al page
                return redirect(url_for('inicio'))
            else:
                flash("Password incorrect, please try other password", "alert-warning")

                #lo redirigimos al index

                return render_template('ingresar.html')
        else:

            flash("The email don't exist, please try with othe email", "alert-warning")

            return render_template('ingresar.html')




@app.route('/listEvent', methods = ['GET', 'POST'])
def listEvent():
    if request.method == 'POST':
        eventName = request.form['eventName']
        eventDateTime = request.form['eventDateTime']

        cursor = db.cursor()
        sql = "INSERT INTO events (eventName, eventDateTime) VALUES (%s, %s);"
        cursor.execute(sql, (eventName, eventDateTime))
        cursor.connection.commit()
        cursor.close()
        return render_template('listEvent2.html')


@app.route('/listEvent2')
def listEvent2():
    cursor = db.cursor()
    sql = "SELECT * FROM events"
    cursor.execute(sql)
    cursor.connection.commit()
    events = cursor.fetchall()
    events = list(events)
    print(events)
    cursor.close()
    return render_template('listEvent2.html', events = events)









#definimos la ruta de salida o logout

@app.route('/logout')
def logout():
    #limpiamos la sesion
    session.clear()

    #redirigimos al index
    return redirect(url_for('ingresar'))


if __name__=='__main__':
    app.run(debug=True)
