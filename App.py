from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

# initializations
app = Flask(__name__)

# Mysql Connection

app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'minicursoAEMS'
mysql = MySQL(app)

# settings
app.secret_key = "mysecretkey"

# routes
@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contatos')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', contatos = data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        nome = request.form['nome']
        celular = request.form['celular']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO contatos (nome, celular, email) VALUES (%s,%s,%s)", (nome, celular, email))
        mysql.connection.commit()
        flash('Contato Adicionado com  successo')
        return redirect(url_for('Index'))

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contatos WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-contact.html', contato = data[0])

@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        nome = request.form['nome']
        celular = request.form['celular']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE contatos
            SET nome = %s,
                email = %s,
                celular = %s
            WHERE id = %s
        """, (nome, email, celular, id))
        flash('Contato Atualizado com Sucesso')
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contatos WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contato Removido com  Sucesso')
    return redirect(url_for('Index'))

# starting the app
if __name__ == "__main__":
    app.run(port=3000, debug=False)
