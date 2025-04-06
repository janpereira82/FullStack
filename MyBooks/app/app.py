from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models.models import db, User, Book, Trophy, BookReading, UserTrophy
import os
from werkzeug.security import check_password_hash
from sqlalchemy import func, desc

def create_app():
    """Cria e configura a aplicação Flask."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'chave-secreta-do-app'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mybooks.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
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
            
            user = User.query.filter_by(email=email).first()
            
            if not user or not user.check_password(password):
                flash('Credenciais inválidas. Por favor, tente novamente.')
                return redirect(url_for('login'))
            
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
        
        if genre:
            books = Book.query.filter_by(genre=genre).paginate(page=page, per_page=per_page)
        else:
            books = Book.query.paginate(page=page, per_page=per_page)
        
        genres = db.session.query(Book.genre).distinct().all()
        genres = [g[0] for g in genres]
        
        # Verificar quais livros o usuário já leu
        read_books = set()
        for reading in current_user.book_readings:
            read_books.add(reading.book_id)
        
        return render_template('books.html', books=books, genres=genres, read_books=read_books)
    
    @app.route('/book/<int:book_id>')
    @login_required
    def book(book_id):
        """Página de detalhes de um livro."""
        book = Book.query.get_or_404(book_id)
        
        # Verificar se o usuário já leu este livro
        already_read = BookReading.query.filter_by(user_id=current_user.id, book_id=book_id).first() is not None
        
        return render_template('book.html', book=book, already_read=already_read)
    
    @app.route('/mark_as_read/<int:book_id>', methods=['POST'])
    @login_required
    def mark_as_read(book_id):
        """Marca um livro como lido."""
        book = Book.query.get_or_404(book_id)
        
        # Verificar se o usuário já leu este livro
        if BookReading.query.filter_by(user_id=current_user.id, book_id=book_id).first():
            flash('Você já marcou este livro como lido.')
            return redirect(url_for('book', book_id=book_id))
        
        # Registrar a leitura
        reading = BookReading(user_id=current_user.id, book_id=book_id)
        db.session.add(reading)
        
        # Calcular e adicionar pontos
        points = book.calculate_points()
        current_user.add_points(points)
        
        # Verificar se o usuário ganhou um troféu
        genre_readings = BookReading.query.join(Book).filter(
            BookReading.user_id == current_user.id,
            Book.genre == book.genre
        ).count()
        
        if genre_readings == 5:
            # Verificar se o troféu existe
            trophy = Trophy.query.filter_by(genre=book.genre).first()
            
            if trophy and not UserTrophy.query.filter_by(user_id=current_user.id, trophy_id=trophy.id).first():
                user_trophy = UserTrophy(user_id=current_user.id, trophy_id=trophy.id)
                db.session.add(user_trophy)
                flash(f'Parabéns! Você ganhou o troféu "{trophy.name}"!')
        
        db.session.commit()
        
        flash(f'Livro "{book.title}" marcado como lido! Você ganhou {points} pontos.')
        return redirect(url_for('book', book_id=book_id))
    
    @app.route('/ranking')
    @login_required
    def ranking():
        """Página com o ranking dos 10 usuários com maior pontuação."""
        top_users = User.query.order_by(User.points.desc()).limit(10).all()
        return render_template('ranking.html', users=top_users)
    
    @app.route('/profile')
    @login_required
    def profile():
        """Página de perfil do usuário."""
        # Obter os troféus do usuário
        user_trophies = UserTrophy.query.filter_by(user_id=current_user.id).all()
        trophies = []
        
        for user_trophy in user_trophies:
            trophy = Trophy.query.get(user_trophy.trophy_id)
            trophies.append(trophy)
        
        # Obter os livros lidos pelo usuário
        readings = BookReading.query.filter_by(user_id=current_user.id).all()
        books_read = []
        
        for reading in readings:
            book = Book.query.get(reading.book_id)
            books_read.append(book)
        
        # Verificar troféus que o usuário ainda não conquistou
        all_trophies = Trophy.query.all()
        missing_trophies = []
        
        for trophy in all_trophies:
            if trophy not in trophies:
                # Contar quantos livros o usuário leu deste gênero
                genre_count = BookReading.query.join(Book).filter(
                    BookReading.user_id == current_user.id,
                    Book.genre == trophy.genre
                ).count()
                
                missing_trophies.append({
                    'trophy': trophy,
                    'progress': genre_count,
                    'target': 5
                })
        
        return render_template('profile.html', 
                              trophies=trophies, 
                              books_read=books_read, 
                              missing_trophies=missing_trophies)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
