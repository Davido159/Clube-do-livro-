from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash  # Para gerar e verificar hash de senha
from db_utils import connect_db  # Função de conexão com o banco de dados
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

app = Flask(__name__)
app.secret_key = 'G7x!R9e@#qZk4tB%aL2$Wv8*HnFz3uJ'  # Substitua por uma chave secreta real

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        try:
            db = connect_db()  # Conexão com o banco de dados
            cursor = db.cursor()

            cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            user = cursor.fetchone()  # Resultado como dicionário

            cursor.close()
            db.close()

            # Verificação do hash da senha
            if user and check_password_hash(user['senha'], senha):  # Comparação do hash com a senha informada
                session['user_id'] = user['id']
                return redirect(url_for('home'))
            else:
                flash('Usuário ou senha incorretos.', 'error')
                return redirect(url_for('login'))
        except Exception as e:
            flash(f"Erro no login: {e}", "error")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        usuario = request.form['usuario']
        nome_completo = request.form['nome_completo']
        data_nascimento = request.form['data_nascimento']

        try:
            db = connect_db()
            cursor = db.cursor()

            cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            usuario_existente = cursor.fetchone()

            if usuario_existente:
                flash('E-mail já utilizado, escolha outro.', 'error')
                cursor.close()
                db.close()
                return redirect(url_for('register'))

            senha_hash = generate_password_hash(senha)  # Gerar o hash da senha

            cursor.execute(
                "INSERT INTO usuarios (email, senha, usuario, nome_completo, data_nascimento) VALUES (%s, %s, %s, %s, %s)",
                (email, senha_hash, usuario, nome_completo, data_nascimento)
            )
            db.commit()
            cursor.close()
            db.close()

            flash('Cadastro realizado com sucesso!', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f"Erro no cadastro: {e}", "error")
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    try:
        db = connect_db()
        cursor = db.cursor()

        cursor.execute("""
            SELECT salas.id, salas.nome FROM salas
            JOIN usuarios ON salas.criador_id = usuarios.id
            WHERE usuarios.id = %s
        """, (session['user_id'],))
        salas = cursor.fetchall()

        cursor.execute("SELECT * FROM livros")
        livros = cursor.fetchall()

        cursor.close()
        db.close()

        return render_template('home.html', salas=salas, livros=livros)
    except Exception as e:
        flash(f"Erro ao carregar a página inicial: {e}", "error")
        return redirect(url_for('login'))

@app.route('/create_room', methods=['GET', 'POST'])
def create_room():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        nome_sala = request.form['nome_sala']
        senha_sala = request.form['senha_sala']
        user_id = session['user_id']

        try:
            db = connect_db()
            cursor = db.cursor()

            cursor.execute("SELECT * FROM salas WHERE nome = %s", (nome_sala,))
            sala_existente = cursor.fetchone()

            if sala_existente:
                flash("Este nome de sala já foi escolhido. Escolha outro nome.", 'error')
                cursor.close()
                db.close()
                return redirect(url_for('create_room'))

            cursor.execute(
                "INSERT INTO salas (nome, senha, criador_id) VALUES (%s, %s, %s)",
                (nome_sala, senha_sala, user_id)
            )
            db.commit()
            cursor.close()
            db.close()

            flash('Sala criada com sucesso!', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            flash(f"Erro ao criar sala: {e}", "error")
            return redirect(url_for('create_room'))

    return render_template('create_room.html')

@app.route('/room/<int:sala_id>', methods=['GET', 'POST'])
def room(sala_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    try:
        db = connect_db()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM salas WHERE id = %s", (sala_id,))
        sala = cursor.fetchone()

        if not sala:
            return "Sala não encontrada.", 404

        cursor.execute("""
            SELECT * FROM sala_livros WHERE sala_id = %s AND EXISTS (
                SELECT * FROM usuarios WHERE id = %s
            )
        """, (sala_id, session['user_id']))
        sala_usuario = cursor.fetchone()

        if request.method == 'POST':
            livro_id = request.form.get('livro_id')
            data_encontro = request.form.get('data_encontro')

            cursor.execute(
                "INSERT INTO sala_livros (sala_id, livro_id, data_encontro) VALUES (%s, %s, %s)",
                (sala_id, livro_id, data_encontro)
            )
            db.commit()

            flash('Encontro agendado com sucesso!', 'success')
            return redirect(url_for('room', sala_id=sala_id))

        cursor.close()
        db.close()

        return render_template('room.html', sala=sala)
    except Exception as e:
        flash(f"Erro ao carregar a sala: {e}", "error")
        return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
