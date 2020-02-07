import pymysql
from flask import Flask, render_template, request, url_for
from werkzeug.utils import redirect

from OpcoesCadastro import PlanoPlus, Cadastro

conexao = pymysql.connect(
    host='localhost',
    user='root',
    passwd='',
    database='novadata'
)

cursor = conexao.cursor()

cursor.execute("CREATE TABLE plano("
               "id_plano INT PRIMARY KEY,"
               "nome_plano VARCHAR(30) NOT NULL)")

cursor.execute("CREATE TABLE usuario("
               "id_usuario INT NOT NULL AUTO_INCREMENT PRIMARY KEY,"
               "user_usuario VARCHAR(30) NOT NULL,"
               "email_usuario VARCHAR(50) NOT NULL,"
               "senha_usuario VARCHAR(20) NOT NULL,"
               "telefone_usuario VARCHAR(9),"
               "cartao_usuario VARCHAR(16),"
               "id_plano INT,"
               "CONSTRAINT fk_user_plano FOREIGN KEY (id_plano) REFERENCES plano(id_plano))")

cursor.execute("INSERT INTO plano(id_plano, nome_plano) VALUES (1, 'Free')")
cursor.execute("INSERT INTO plano(id_plano, nome_plano) VALUES (2, 'Premium')")


app = Flask(__name__)

@app.route('/Loged', methods=["GET","POST"])
def UsuarioLogado():

    nome = request.args['nome']
    email = request.args['email']
    telefone = request.args['telefone']
    senha = request.args['senha']
    numCartao = request.args['cartao']

    if(len(numCartao) == 0):
        cursor.execute("""INSERT INTO usuario(user_usuario, email_usuario, senha_usuario,
        telefone_usuario, cartao_usuario, id_plano) VALUES 
        ("%s", "%s", "%s", "%s", "%s", "%s")"""
        % (nome, email, senha, telefone, numCartao, 1))

        conexao.commit()

        cursor.execute("SELECT user_usuario FROM usuario WHERE user_usuario ='" + nome + "'")
        (sel,) = cursor.fetchone()
        s = sel
        p = 'Free'

        c = Cadastro.Cadastro(nome, email, telefone, senha)

        return render_template('PaginaLoged.html', conteudo=c, select=s, plano=p)
    else:
        cursor.execute("""INSERT INTO usuario(user_usuario, email_usuario, senha_usuario,
        telefone_usuario, cartao_usuario, id_plano) VALUES 
        ("%s", "%s", "%s", "%s", "%s", "%s")"""
        % (nome, email, senha, telefone, numCartao, 2))

        conexao.commit()

        cursor.execute("SELECT user_usuario FROM usuario WHERE user_usuario ='" + nome + "'")
        (sel,) = cursor.fetchone()
        s = sel
        p = 'Premium'

        c = PlanoPlus.PlanoPlus(nome, email, telefone, senha, numCartao)

        return render_template('PaginaLoged.html', conteudo=c, select=s, plano=p)


@app.route('/AlteraSenha')
def alteraSenha():
    antigaSenha = request.args['antigaSenha']
    novaSenha = request.args['novaSenha']


    cursor.execute(""" UPDATE usuario 
    SET senha_usuario=%s 
    WHERE senha_usuario=%s""", (novaSenha, antigaSenha))

    conexao.commit()

    return render_template('SenhaAlterada.html')

@app.route('/DeletaConta')
def deletaConta():

    req = request.args

    senhadeletar = req.get("emailDel")

    cursor.execute(""" DELETE from  usuario 
    WHERE email_usuario=%s""", (senhadeletar))

    conexao.commit()

    return render_template('ContaDeletada.html')


@app.route('/')
def cadastroUsuario():

    if request.method == "POST":
        return redirect(url_for("Loged"))
    return render_template('Login.html')



app.run()

