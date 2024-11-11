from flask import Flask, request, render_template, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configurações de conexão ao MySQL
app.config['MYSQL_HOST'] = '127.0.0.1' 
app.config['MYSQL_USER'] = 'root'      
app.config['MYSQL_PASSWORD'] = 'fatec'
app.config['MYSQL_DB'] = 'contatos'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/contatos')
def contatos():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM contatos")
    contatos = cursor.fetchall()  # Busca os contatos no banco de dados
    cursor.close()
    return render_template('contatos.html', contatos=contatos)

@app.route('/contato', methods=['GET', 'POST'])
def contato():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')  
        mensagem = request.form.get('mensagem')  
        
        # Conexão com o banco de dados para salvar os dados
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO contatos (email, senha, mensagem) VALUES (%s, %s, %s)", (email, senha, mensagem))
        mysql.connection.commit()
        cursor.close()

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM contatos")
        contatos = cursor.fetchall()
        
        return redirect(url_for('contatos'))
    
    return render_template('contato.html')

if __name__ == '__main__':
    app.run(debug=True)

