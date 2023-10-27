# Importações necessárias
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

# Inicialização do aplicativo Flask
app = Flask(__name__)

# Configuração da conexão MySQL
app.config['MYSQL_HOST'] = 'localhost'  # Endereço do servidor MySQL
app.config['MYSQL_USER'] = 'root'  # Nome de usuário do MySQL
app.config['MYSQL_PASSWORD'] = ''  # Senha do MySQL
app.config['MYSQL_DB'] = 'minicursoAEMS'  # Nome do banco de dados
mysql = MySQL(app)  # Inicialização do objeto MySQL para Flask

# Configuração de uma chave secreta para a aplicação (usada para cookies, sessões, etc.)
app.secret_key = "mysecretkey"

# Rotas

# Rota inicial que exibe uma lista de contatos
@app.route('/')
def Index():
    cur = mysql.connection.cursor()  # Cria um cursor para interagir com o banco de dados
    cur.execute('SELECT * FROM contatos')  # Executa uma consulta SQL para obter todos os contatos
    data = cur.fetchall()  # Obtém os resultados da consulta
    cur.close()  # Fecha o cursor
    return render_template('index.html', contatos=data)  # Renderiza uma página HTML com os contatos

# Rota para adicionar um novo contato
@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        nome = request.form['nome']
        celular = request.form['celular']
        email = request.form['email']
        cur = mysql.connection.cursor()
        # Executa uma consulta SQL para inserir um novo contato
        cur.execute("INSERT INTO contatos (nome, celular, email) VALUES (%s,%s,%s)", (nome, celular, email))
        mysql.connection.commit()  # Confirma a transação no banco de dados
        flash('Contato Adicionado com sucesso')  # Exibe uma mensagem de sucesso
        return redirect(url_for('Index'))  # Redireciona de volta para a página inicial

# Rota para editar um contato
@app.route('/edit/<id>', methods=['POST', 'GET'])
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contatos WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    return render_template('edit-contact.html', contato=data[0])

# Rota para atualizar um contato
@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        nome = request.form['nome']
        celular = request.form['celular']
        email = request.form['email']
        cur = mysql.connection.cursor()
        # Executa uma consulta SQL para atualizar os dados de um contato
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

# Rota para excluir um contato
@app.route('/delete/<string:id>', methods=['POST', 'GET'])
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contatos WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contato Removido com Sucesso')
    return redirect(url_for('Index'))

# Inicialização do aplicativo Flask
if __name__ == "__main__":
    app.run(port=3000, debug=False)
