from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    """Modelo para representar os usuários do sistema."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    points = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    book_readings = db.relationship('BookReading', backref='user', lazy=True)
    trophies = db.relationship('UserTrophy', backref='user', lazy=True)
    
    def set_password(self, password):
        """Define a senha do usuário."""
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        """Verifica se a senha está correta."""
        return check_password_hash(self.password_hash, password)
    
    def add_points(self, points):
        """Adiciona pontos ao usuário."""
        self.points += points
        db.session.commit()
    
    def __repr__(self):
        return f'<User {self.username}>'


class Book(db.Model):
    """Modelo para representar os livros disponíveis no sistema."""
    __tablename__ = 'books'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    cover_image = db.Column(db.String(200))
    
    readings = db.relationship('BookReading', backref='book', lazy=True)
    
    def calculate_points(self):
        """Calcula os pontos que o livro vale com base no número de páginas."""
        # 1 ponto base + 1 ponto adicional a cada 100 páginas
        return 1 + (self.pages // 100)
    
    def __repr__(self):
        return f'<Book {self.title}>'


class BookReading(db.Model):
    """Modelo para representar a leitura de um livro por um usuário."""
    __tablename__ = 'book_readings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    read_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<BookReading user_id={self.user_id} book_id={self.book_id}>'


class Trophy(db.Model):
    """Modelo para representar os troféus disponíveis no sistema."""
    __tablename__ = 'trophies'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    genre = db.Column(db.String(50), nullable=False)
    
    user_trophies = db.relationship('UserTrophy', backref='trophy', lazy=True)
    
    def __repr__(self):
        return f'<Trophy {self.name}>'


class UserTrophy(db.Model):
    """Modelo para representar os troféus conquistados por um usuário."""
    __tablename__ = 'user_trophies'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    trophy_id = db.Column(db.Integer, db.ForeignKey('trophies.id'), nullable=False)
    earned_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<UserTrophy user_id={self.user_id} trophy_id={self.trophy_id}>'
