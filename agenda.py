from flask import Flask, render_template, request, flash, url_for
from werkzeug.utils import redirect
from flask_mysqldb import MySQL
import pymysql

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


@app.route('/')
def index():
    cursor = db.cursor()
    cursor.execute('SELECT * FROM contact')
    data = cursor.fetchall()
    return render_template('index.html', contacts=data)


@app.route('/add_contacts', methods=['POST'])
def add_contacts():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']

        cursor = db.cursor()
        cursor.execute('INSERT INTO contact(fullname, phone, email) VALUES(%s, %s, %s)',
                       (fullname, phone, email))
        cursor.connection.commit()
        flash('Contacto agregado satisfactoriamente')
        return redirect(url_for('index'))


@app.route('/edit/<id>')
def get_contact(id):
    cursor = db.cursor()
    cursor.execute('SELECT * FROM contact WHERE id = %s', (id))
    data = cursor.fetchall()
    return render_template('/edit.html', contact=data[0])


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
