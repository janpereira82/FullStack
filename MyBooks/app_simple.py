from flask import Flask, render_template, redirect, url_for, flash, request, g
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import check_password_hash
import sqlite3
import os
from datetime import datetime

# Configuração da aplicação
app = Flask(__name__, template_folder='app/templates')
app.config['SECRET_KEY'] = 'chave-secreta-do-app'
app.config['DATABASE'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mybooks.db')

# Configuração do login manager
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# Classe para representar um usuário para o Flask-Login
class User(UserMixin):
    def __init__(self, id, username, email, points):
        self.id = id
        self.username = username
        self.email = email
        self.points = points
        self.book_readings = []
        
    def check_password(self, password):
        """Verifica se a senha está correta."""
        db = get_db()
        user = db.execute('SELECT password_hash FROM users WHERE id = ?', (self.id,)).fetchone()
        return check_password_hash(user['password_hash'], password)
    
    def add_points(self, points):
        """Adiciona pontos ao usuário."""
        db = get_db()
        db.execute('UPDATE users SET points = points + ? WHERE id = ?', (points, self.id))
        db.commit()
        self.points += points

# Função para obter uma conexão com o banco de dados
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
        db.row_factory = sqlite3.Row
    return db

# Função para fechar a conexão com o banco de dados
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Função para carregar um usuário pelo ID
@login_manager.user_loader
def load_user(user_id):
    db = get_db()
    user = db.execute('SELECT id, username, email, points FROM users WHERE id = ?', (user_id,)).fetchone()
    if user:
        return User(user['id'], user['username'], user['email'], user['points'])
    return None

# Função para calcular os pontos de um livro
def calculate_book_points(pages):
    return 1 + (pages // 100)

# Rotas da aplicação
@app.route('/')
def index():
    """Página inicial."""
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login."""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        db = get_db()
        user_data = db.execute('SELECT id, username, email, points, password_hash FROM users WHERE email = ?', (email,)).fetchone()
        
        if not user_data or not check_password_hash(user_data['password_hash'], password):
            flash('Credenciais inválidas. Por favor, tente novamente.')
            return redirect(url_for('login'))
        
        user = User(user_data['id'], user_data['username'], user_data['email'], user_data['points'])
        login_user(user)
        return redirect(url_for('books'))
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """Rota para logout."""
    logout_user()
    return redirect(url_for('login'))

@app.route('/books')
@login_required
def books():
    """Página com a lista de livros."""
    genre = request.args.get('genre')
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    db = get_db()
    
    # Obter os gêneros distintos
    genres = db.execute('SELECT DISTINCT genre FROM books').fetchall()
    genres = [g['genre'] for g in genres]
    
    # Obter os livros com filtro de gênero, se aplicável
    if genre:
        query = 'SELECT * FROM books WHERE genre = ? LIMIT ? OFFSET ?'
        params = (genre, per_page, (page - 1) * per_page)
        count_query = 'SELECT COUNT(*) as count FROM books WHERE genre = ?'
        count_params = (genre,)
    else:
        query = 'SELECT * FROM books LIMIT ? OFFSET ?'
        params = (per_page, (page - 1) * per_page)
        count_query = 'SELECT COUNT(*) as count FROM books'
        count_params = ()
    
    books_data = db.execute(query, params).fetchall()
    total_books = db.execute(count_query, count_params).fetchone()['count']
    
    # Verificar quais livros o usuário já leu
    read_books = set()
    readings = db.execute('SELECT book_id FROM book_readings WHERE user_id = ?', (current_user.id,)).fetchall()
    for reading in readings:
        read_books.add(reading['book_id'])
    
    # Criar uma classe para simular a paginação do SQLAlchemy
    class Pagination:
        def __init__(self, items, page, per_page, total):
            self.items = items
            self.page = page
            self.per_page = per_page
            self.total = total
            
        @property
        def pages(self):
            return max(1, self.total // self.per_page + (1 if self.total % self.per_page > 0 else 0))
        
        @property
        def has_prev(self):
            return self.page > 1
        
        @property
        def has_next(self):
            return self.page < self.pages
        
        @property
        def prev_num(self):
            return self.page - 1 if self.has_prev else None
        
        @property
        def next_num(self):
            return self.page + 1 if self.has_next else None
        
        def iter_pages(self, left_edge=2, left_current=2, right_current=5, right_edge=2):
            last = 0
            for num in range(1, self.pages + 1):
                if num <= left_edge or \
                   (num > self.page - left_current - 1 and num < self.page + right_current) or \
                   num > self.pages - right_edge:
                    if last + 1 != num:
                        yield None
                    yield num
                    last = num
    
    # Converter objetos Row para dicionários e adicionar método calculate_points
    books_dict = []
    for book in books_data:
        book_dict = dict(book)
        book_dict['calculate_points'] = lambda pages=book_dict['pages']: calculate_book_points(pages)
        books_dict.append(book_dict)
    
    # Criar objeto de paginação
    pagination = Pagination(books_dict, page, per_page, total_books)
    
    return render_template('books.html', books=pagination, genres=genres, read_books=read_books)

@app.route('/book/<int:book_id>')
@login_required
def book(book_id):
    """Página de detalhes de um livro."""
    db = get_db()
    book = db.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
    
    if not book:
        flash('Livro não encontrado.')
        return redirect(url_for('books'))
    
    # Converter objeto Row para dicionário e adicionar método calculate_points
    book_dict = dict(book)
    book_dict['calculate_points'] = lambda: calculate_book_points(book_dict['pages'])
    
    # Verificar se o usuário já leu este livro
    already_read = db.execute(
        'SELECT 1 FROM book_readings WHERE user_id = ? AND book_id = ?',
        (current_user.id, book_id)
    ).fetchone() is not None
    
    return render_template('book.html', book=book_dict, already_read=already_read)

@app.route('/mark_as_read/<int:book_id>', methods=['POST'])
@login_required
def mark_as_read(book_id):
    """Marca um livro como lido."""
    db = get_db()
    book = db.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
    
    if not book:
        flash('Livro não encontrado.')
        return redirect(url_for('books'))
    
    # Converter objeto Row para dicionário
    book_dict = dict(book)
    
    # Verificar se o usuário já leu este livro
    already_read = db.execute(
        'SELECT 1 FROM book_readings WHERE user_id = ? AND book_id = ?',
        (current_user.id, book_id)
    ).fetchone()
    
    if already_read:
        flash('Você já marcou este livro como lido.')
        return redirect(url_for('book', book_id=book_id))
    
    # Registrar a leitura
    db.execute(
        'INSERT INTO book_readings (user_id, book_id) VALUES (?, ?)',
        (current_user.id, book_id)
    )
    
    # Calcular e adicionar pontos
    points = calculate_book_points(book_dict['pages'])
    db.execute(
        'UPDATE users SET points = points + ? WHERE id = ?',
        (points, current_user.id)
    )
    
    # Verificar se o usuário ganhou um troféu
    genre_readings = db.execute(
        '''
        SELECT COUNT(*) as count
        FROM book_readings br
        JOIN books b ON br.book_id = b.id
        WHERE br.user_id = ? AND b.genre = ?
        ''',
        (current_user.id, book_dict['genre'])
    ).fetchone()['count']
    
    if genre_readings == 5:
        # Verificar se o troféu existe
        trophy = db.execute(
            'SELECT id, name FROM trophies WHERE genre = ?',
            (book_dict['genre'],)
        ).fetchone()
        
        if trophy:
            # Converter objeto Row para dicionário
            trophy_dict = dict(trophy)
            
            # Verificar se o usuário já tem este troféu
            has_trophy = db.execute(
                'SELECT 1 FROM user_trophies WHERE user_id = ? AND trophy_id = ?',
                (current_user.id, trophy_dict['id'])
            ).fetchone()
            
            if not has_trophy:
                db.execute(
                    'INSERT INTO user_trophies (user_id, trophy_id) VALUES (?, ?)',
                    (current_user.id, trophy_dict['id'])
                )
                flash(f'Parabéns! Você ganhou o troféu "{trophy_dict["name"]}"!')
    
    db.commit()
    
    flash(f'Livro "{book_dict["title"]}" marcado como lido! Você ganhou {points} pontos.')
    return redirect(url_for('book', book_id=book_id))

@app.route('/ranking')
@login_required
def ranking():
    """Página com o ranking dos 10 usuários com maior pontuação."""
    db = get_db()
    top_users = db.execute(
        'SELECT id, username, points FROM users ORDER BY points DESC LIMIT 10'
    ).fetchall()
    
    # Converter objetos Row para dicionários
    top_users_dict = [dict(user) for user in top_users]
    
    return render_template('ranking.html', users=top_users_dict)

@app.route('/profile')
@login_required
def profile():
    """Página de perfil do usuário."""
    db = get_db()
    
    # Obter os troféus do usuário
    user_trophies = db.execute(
        '''
        SELECT t.*
        FROM user_trophies ut
        JOIN trophies t ON ut.trophy_id = t.id
        WHERE ut.user_id = ?
        ''',
        (current_user.id,)
    ).fetchall()
    
    # Converter objetos Row para dicionários
    user_trophies_dict = [dict(trophy) for trophy in user_trophies]
    
    # Obter os livros lidos pelo usuário
    books_read = db.execute(
        '''
        SELECT b.*
        FROM book_readings br
        JOIN books b ON br.book_id = b.id
        WHERE br.user_id = ?
        ''',
        (current_user.id,)
    ).fetchall()
    
    # Converter objetos Row para dicionários e adicionar método calculate_points
    books_read_dict = []
    for book in books_read:
        book_dict = dict(book)
        book_dict['calculate_points'] = lambda pages=book_dict['pages']: calculate_book_points(pages)
        books_read_dict.append(book_dict)
    
    # Verificar troféus que o usuário ainda não conquistou
    all_trophies = db.execute('SELECT * FROM trophies').fetchall()
    missing_trophies = []
    
    for trophy in all_trophies:
        # Verificar se o usuário já tem este troféu
        has_trophy = False
        for user_trophy in user_trophies_dict:
            if user_trophy['id'] == trophy['id']:
                has_trophy = True
                break
        
        if not has_trophy:
            # Contar quantos livros o usuário leu deste gênero
            genre_count = db.execute(
                '''
                SELECT COUNT(*) as count
                FROM book_readings br
                JOIN books b ON br.book_id = b.id
                WHERE br.user_id = ? AND b.genre = ?
                ''',
                (current_user.id, trophy['genre'])
            ).fetchone()['count']
            
            missing_trophies.append({
                'trophy': dict(trophy),
                'progress': genre_count,
                'target': 5
            })
    
    return render_template('profile.html', 
                          trophies=user_trophies_dict, 
                          books_read=books_read_dict, 
                          missing_trophies=missing_trophies)

if __name__ == "__main__":
    app.run(debug=True)
