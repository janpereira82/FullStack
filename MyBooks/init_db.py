from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chave-secreta-do-app'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'mybooks.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definição dos modelos
class User(db.Model):
    """Modelo para representar os usuários do sistema."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    points = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        """Define a senha do usuário."""
        self.password_hash = generate_password_hash(password)

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

class BookReading(db.Model):
    """Modelo para representar a leitura de um livro por um usuário."""
    __tablename__ = 'book_readings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    read_date = db.Column(db.DateTime, default=datetime.utcnow)

class Trophy(db.Model):
    """Modelo para representar os troféus disponíveis no sistema."""
    __tablename__ = 'trophies'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    genre = db.Column(db.String(50), nullable=False)

class UserTrophy(db.Model):
    """Modelo para representar os troféus conquistados por um usuário."""
    __tablename__ = 'user_trophies'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    trophy_id = db.Column(db.Integer, db.ForeignKey('trophies.id'), nullable=False)
    earned_date = db.Column(db.DateTime, default=datetime.utcnow)

def init_db():
    """Inicializa o banco de dados com dados de exemplo."""
    with app.app_context():
        # Cria as tabelas
        db.create_all()
        
        # Verifica se já existem dados no banco
        if User.query.count() > 0:
            print("Banco de dados já inicializado.")
            return
        
        # Cria usuários de exemplo
        users = [
            User(username="joao", email="joao@example.com", points=15),
            User(username="maria", email="maria@example.com", points=22),
            User(username="pedro", email="pedro@example.com", points=8),
            User(username="ana", email="ana@example.com", points=30),
            User(username="carlos", email="carlos@example.com", points=18),
            User(username="lucia", email="lucia@example.com", points=25),
            User(username="bruno", email="bruno@example.com", points=12),
            User(username="julia", email="julia@example.com", points=20),
            User(username="rafael", email="rafael@example.com", points=10),
            User(username="mariana", email="mariana@example.com", points=27),
            User(username="teste", email="teste@example.com", points=0)
        ]
        
        for user in users:
            user.set_password("senha123")
            db.session.add(user)
        
        # Cria livros de exemplo
        books = [
            # Ficção Científica
            Book(title="Fundação", author="Isaac Asimov", pages=320, genre="Ficção Científica", 
                 description="Primeiro livro da série Fundação, uma das mais importantes da ficção científica.",
                 cover_image="fundacao.jpg"),
            Book(title="Duna", author="Frank Herbert", pages=450, genre="Ficção Científica", 
                 description="Uma obra-prima da ficção científica que se passa em um planeta desértico.",
                 cover_image="duna.jpg"),
            Book(title="Neuromancer", author="William Gibson", pages=280, genre="Ficção Científica", 
                 description="Romance que definiu o subgênero cyberpunk.",
                 cover_image="neuromancer.jpg"),
            Book(title="Eu, Robô", author="Isaac Asimov", pages=240, genre="Ficção Científica", 
                 description="Coletânea de contos sobre robôs e as três leis da robótica.",
                 cover_image="eu_robo.jpg"),
            Book(title="2001: Uma Odisseia no Espaço", author="Arthur C. Clarke", pages=290, genre="Ficção Científica", 
                 description="Clássico da ficção científica que inspirou o filme de Stanley Kubrick.",
                 cover_image="2001.jpg"),
            
            # Fantasia
            Book(title="O Senhor dos Anéis", author="J.R.R. Tolkien", pages=1200, genre="Fantasia", 
                 description="Épico de fantasia que se tornou um dos livros mais vendidos da história.",
                 cover_image="senhor_dos_aneis.jpg"),
            Book(title="Harry Potter e a Pedra Filosofal", author="J.K. Rowling", pages=320, genre="Fantasia", 
                 description="Primeiro livro da série Harry Potter.",
                 cover_image="harry_potter.jpg"),
            Book(title="As Crônicas de Nárnia", author="C.S. Lewis", pages=750, genre="Fantasia", 
                 description="Série de sete livros de fantasia ambientados no mundo mágico de Nárnia.",
                 cover_image="narnia.jpg"),
            Book(title="O Nome do Vento", author="Patrick Rothfuss", pages=650, genre="Fantasia", 
                 description="Primeiro livro da trilogia A Crônica do Matador do Rei.",
                 cover_image="nome_do_vento.jpg"),
            Book(title="A Roda do Tempo", author="Robert Jordan", pages=850, genre="Fantasia", 
                 description="Primeiro livro de uma das mais extensas séries de fantasia já escritas.",
                 cover_image="roda_do_tempo.jpg"),
            
            # Romance
            Book(title="Orgulho e Preconceito", author="Jane Austen", pages=380, genre="Romance", 
                 description="Um dos romances mais populares da literatura inglesa.",
                 cover_image="orgulho_preconceito.jpg"),
            Book(title="Dom Casmurro", author="Machado de Assis", pages=210, genre="Romance", 
                 description="Um dos romances mais importantes da literatura brasileira.",
                 cover_image="dom_casmurro.jpg"),
            Book(title="O Morro dos Ventos Uivantes", author="Emily Brontë", pages=320, genre="Romance", 
                 description="Romance gótico que se passa no ambiente selvagem dos moors ingleses.",
                 cover_image="morro_ventos.jpg"),
            Book(title="Cem Anos de Solidão", author="Gabriel García Márquez", pages=420, genre="Romance", 
                 description="Obra-prima do realismo mágico que narra a história da família Buendía.",
                 cover_image="cem_anos.jpg"),
            Book(title="O Grande Gatsby", author="F. Scott Fitzgerald", pages=180, genre="Romance", 
                 description="Romance ambientado na era do jazz que retrata o sonho americano.",
                 cover_image="gatsby.jpg"),
            
            # Não-Ficção
            Book(title="Sapiens: Uma Breve História da Humanidade", author="Yuval Noah Harari", pages=450, genre="Não-Ficção", 
                 description="Uma visão inovadora sobre a história e evolução da humanidade.",
                 cover_image="sapiens.jpg"),
            Book(title="Cosmos", author="Carl Sagan", pages=380, genre="Não-Ficção", 
                 description="Uma viagem pela história da astronomia e do universo.",
                 cover_image="cosmos.jpg"),
            Book(title="Uma Breve História do Tempo", author="Stephen Hawking", pages=250, genre="Não-Ficção", 
                 description="Explicações sobre cosmologia, buracos negros e a natureza do tempo.",
                 cover_image="breve_historia.jpg"),
            Book(title="O Poder do Hábito", author="Charles Duhigg", pages=320, genre="Não-Ficção", 
                 description="Por que fazemos o que fazemos na vida e nos negócios.",
                 cover_image="poder_habito.jpg"),
            Book(title="Armas, Germes e Aço", author="Jared Diamond", pages=480, genre="Não-Ficção", 
                 description="Os destinos das sociedades humanas e como foram moldados.",
                 cover_image="armas_germes.jpg"),
        ]
        
        for book in books:
            db.session.add(book)
        
        # Cria troféus de exemplo
        trophies = [
            Trophy(name="Leitor de Ficção Científica", description="Leu 5 livros de Ficção Científica", genre="Ficção Científica"),
            Trophy(name="Leitor de Fantasia", description="Leu 5 livros de Fantasia", genre="Fantasia"),
            Trophy(name="Leitor de Romance", description="Leu 5 livros de Romance", genre="Romance"),
            Trophy(name="Leitor de Não-Ficção", description="Leu 5 livros de Não-Ficção", genre="Não-Ficção"),
        ]
        
        for trophy in trophies:
            db.session.add(trophy)
        
        db.session.commit()
        print("Banco de dados inicializado com sucesso!")

if __name__ == "__main__":
    init_db()
