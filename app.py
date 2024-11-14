import requests
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from db_utils import connect_db

app = Flask(__name__)
app.secret_key = 'G7x!R9e@#qZk4tB%aL2$Wv8*HnFz3uJ'

# Função para buscar dados dos livros da API Open Library
def fetch_books_from_api():
    try:
        response = requests.get("https://openlibrary.org/subjects/love.json?limit=5")  # Exemplo de categoria 'love'
        if response.status_code == 200:
            data = response.json()
            books = []
            for doc in data.get("works", []):
                book = {
                    "titulo": doc.get("title"),
                    "autor": ', '.join(author['name'] for author in doc.get('authors', [])),
                    "genero": doc.get("subject", [])[0] if doc.get("subject") else "Desconhecido",
                    "pais_origem": "Desconhecido",  # Informação não disponível diretamente na Open Library
                    "quantidade_paginas": doc.get("number_of_pages", "Desconhecido")
                }
                books.append(book)
            return books
        else:
            flash("Erro ao buscar livros da API.", "error")
            return []
    except Exception as e:
        flash(f"Erro ao conectar com a API: {e}", "error")
        return []

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        try:
            db = connect_db()
            cursor = db.cursor()

            cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            user = cursor.fetchone()

            cursor.close()
            db.close()

            if user and check_password_hash(user['senha'], senha):
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

            senha_hash = generate_password_hash(senha)

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

        # Buscar as salas do usuário
        cursor.execute("""
            SELECT salas.id, salas.nome FROM salas
            JOIN usuarios ON salas.criador_id = usuarios.id
            WHERE usuarios.id = %s
        """, (session['user_id'],))
        salas = cursor.fetchall()

        # Buscar livros da API ou banco de dados
        livros = fetch_books_from_api()  # Ou buscar no banco de dados

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

        # Buscar os encontros agendados para a sala
        cursor.execute("""
            SELECT sala_livros.livro_id, sala_livros.data_encontro, livros.titulo
            FROM sala_livros
            JOIN livros ON sala_livros.livro_id = livros.id
            WHERE sala_livros.sala_id = %s
        """, (sala_id,))
        encontros = cursor.fetchall()

        # Buscar os livros disponíveis para a sala
        cursor.execute("""
            SELECT livros.id, livros.titulo, livros.autor
            FROM livros
            LEFT JOIN sala_livros ON livros.id = sala_livros.livro_id
            WHERE sala_livros.sala_id IS NULL OR sala_livros.sala_id = %s
        """, (sala_id,))
        livros = cursor.fetchall()

        if request.method == 'POST':
            livro_id = request.form.get('livro_id')
            data_encontro = request.form.get('data_encontro')

            if livro_id and data_encontro:
                cursor.execute(
                    "INSERT INTO sala_livros (sala_id, livro_id, data_encontro) VALUES (%s, %s, %s)",
                    (sala_id, livro_id, data_encontro)
                )
                db.commit()

                flash('Encontro agendado com sucesso!', 'success')
                return redirect(url_for('room', sala_id=sala_id))

        cursor.close()
        db.close()

        return render_template('room.html', sala=sala, encontros=encontros, livros=livros)
    
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
