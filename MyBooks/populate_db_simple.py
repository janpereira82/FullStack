import sqlite3
import os
from werkzeug.security import generate_password_hash
from datetime import datetime

# Caminho para o banco de dados
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mybooks.db')

def create_tables(conn):
    """Cria as tabelas no banco de dados."""
    cursor = conn.cursor()
    
    # Tabela de usuários
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        points INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Tabela de livros
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        pages INTEGER NOT NULL,
        genre TEXT NOT NULL,
        description TEXT,
        cover_image TEXT
    )
    ''')
    
    # Tabela de leituras
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS book_readings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        book_id INTEGER NOT NULL,
        read_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (book_id) REFERENCES books (id)
    )
    ''')
    
    # Tabela de troféus
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS trophies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        genre TEXT NOT NULL
    )
    ''')
    
    # Tabela de troféus do usuário
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_trophies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        trophy_id INTEGER NOT NULL,
        earned_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (trophy_id) REFERENCES trophies (id)
    )
    ''')
    
    conn.commit()

def populate_users(conn):
    """Popula a tabela de usuários."""
    cursor = conn.cursor()
    
    # Limpa os dados existentes
    cursor.execute("DELETE FROM users")
    
    # Usuários de exemplo
    users = [
        ("joao", "joao@example.com", generate_password_hash("senha123"), 15),
        ("maria", "maria@example.com", generate_password_hash("senha123"), 22),
        ("pedro", "pedro@example.com", generate_password_hash("senha123"), 8),
        ("ana", "ana@example.com", generate_password_hash("senha123"), 30),
        ("carlos", "carlos@example.com", generate_password_hash("senha123"), 18),
        ("lucia", "lucia@example.com", generate_password_hash("senha123"), 25),
        ("bruno", "bruno@example.com", generate_password_hash("senha123"), 12),
        ("julia", "julia@example.com", generate_password_hash("senha123"), 20),
        ("rafael", "rafael@example.com", generate_password_hash("senha123"), 10),
        ("mariana", "mariana@example.com", generate_password_hash("senha123"), 27),
        ("teste", "teste@example.com", generate_password_hash("senha123"), 0)
    ]
    
    cursor.executemany(
        "INSERT INTO users (username, email, password_hash, points) VALUES (?, ?, ?, ?)",
        users
    )
    
    conn.commit()
    print("Usuários populados com sucesso!")

def populate_books(conn):
    """Popula a tabela de livros."""
    cursor = conn.cursor()
    
    # Limpa os dados existentes
    cursor.execute("DELETE FROM books")
    
    # Livros de exemplo
    books = [
        # Ficção Científica
        ("Fundação", "Isaac Asimov", 320, "Ficção Científica", 
         "Primeiro livro da série Fundação, uma das mais importantes da ficção científica.",
         "fundacao.jpg"),
        ("Duna", "Frank Herbert", 450, "Ficção Científica", 
         "Uma obra-prima da ficção científica que se passa em um planeta desértico.",
         "duna.jpg"),
        ("Neuromancer", "William Gibson", 280, "Ficção Científica", 
         "Romance que definiu o subgênero cyberpunk.",
         "neuromancer.jpg"),
        ("Eu, Robô", "Isaac Asimov", 240, "Ficção Científica", 
         "Coletânea de contos sobre robôs e as três leis da robótica.",
         "eu_robo.jpg"),
        ("2001: Uma Odisseia no Espaço", "Arthur C. Clarke", 290, "Ficção Científica", 
         "Clássico da ficção científica que inspirou o filme de Stanley Kubrick.",
         "2001.jpg"),
        
        # Fantasia
        ("O Senhor dos Anéis", "J.R.R. Tolkien", 1200, "Fantasia", 
         "Épico de fantasia que se tornou um dos livros mais vendidos da história.",
         "senhor_dos_aneis.jpg"),
        ("Harry Potter e a Pedra Filosofal", "J.K. Rowling", 320, "Fantasia", 
         "Primeiro livro da série Harry Potter.",
         "harry_potter.jpg"),
        ("As Crônicas de Nárnia", "C.S. Lewis", 750, "Fantasia", 
         "Série de sete livros de fantasia ambientados no mundo mágico de Nárnia.",
         "narnia.jpg"),
        ("O Nome do Vento", "Patrick Rothfuss", 650, "Fantasia", 
         "Primeiro livro da trilogia A Crônica do Matador do Rei.",
         "nome_do_vento.jpg"),
        ("A Roda do Tempo", "Robert Jordan", 850, "Fantasia", 
         "Primeiro livro de uma das mais extensas séries de fantasia já escritas.",
         "roda_do_tempo.jpg"),
        
        # Romance
        ("Orgulho e Preconceito", "Jane Austen", 380, "Romance", 
         "Um dos romances mais populares da literatura inglesa.",
         "orgulho_preconceito.jpg"),
        ("Dom Casmurro", "Machado de Assis", 210, "Romance", 
         "Um dos romances mais importantes da literatura brasileira.",
         "dom_casmurro.jpg"),
        ("O Morro dos Ventos Uivantes", "Emily Brontë", 320, "Romance", 
         "Romance gótico que se passa no ambiente selvagem dos moors ingleses.",
         "morro_ventos.jpg"),
        ("Cem Anos de Solidão", "Gabriel García Márquez", 420, "Romance", 
         "Obra-prima do realismo mágico que narra a história da família Buendía.",
         "cem_anos.jpg"),
        ("O Grande Gatsby", "F. Scott Fitzgerald", 180, "Romance", 
         "Romance ambientado na era do jazz que retrata o sonho americano.",
         "gatsby.jpg"),
        
        # Não-Ficção
        ("Sapiens: Uma Breve História da Humanidade", "Yuval Noah Harari", 450, "Não-Ficção", 
         "Uma visão inovadora sobre a história e evolução da humanidade.",
         "sapiens.jpg"),
        ("Cosmos", "Carl Sagan", 380, "Não-Ficção", 
         "Uma viagem pela história da astronomia e do universo.",
         "cosmos.jpg"),
        ("Uma Breve História do Tempo", "Stephen Hawking", 250, "Não-Ficção", 
         "Explicações sobre cosmologia, buracos negros e a natureza do tempo.",
         "breve_historia.jpg"),
        ("O Poder do Hábito", "Charles Duhigg", 320, "Não-Ficção", 
         "Por que fazemos o que fazemos na vida e nos negócios.",
         "poder_habito.jpg"),
        ("Armas, Germes e Aço", "Jared Diamond", 480, "Não-Ficção", 
         "Os destinos das sociedades humanas e como foram moldados.",
         "armas_germes.jpg")
    ]
    
    cursor.executemany(
        "INSERT INTO books (title, author, pages, genre, description, cover_image) VALUES (?, ?, ?, ?, ?, ?)",
        books
    )
    
    conn.commit()
    print("Livros populados com sucesso!")

def populate_trophies(conn):
    """Popula a tabela de troféus."""
    cursor = conn.cursor()
    
    # Limpa os dados existentes
    cursor.execute("DELETE FROM trophies")
    
    # Troféus de exemplo
    trophies = [
        ("Leitor de Ficção Científica", "Leu 5 livros de Ficção Científica", "Ficção Científica"),
        ("Leitor de Fantasia", "Leu 5 livros de Fantasia", "Fantasia"),
        ("Leitor de Romance", "Leu 5 livros de Romance", "Romance"),
        ("Leitor de Não-Ficção", "Leu 5 livros de Não-Ficção", "Não-Ficção")
    ]
    
    cursor.executemany(
        "INSERT INTO trophies (name, description, genre) VALUES (?, ?, ?)",
        trophies
    )
    
    conn.commit()
    print("Troféus populados com sucesso!")

def add_readings_for_teste_user(conn):
    """Adiciona algumas leituras para o usuário 'teste'."""
    cursor = conn.cursor()
    
    # Limpa os dados existentes
    cursor.execute("DELETE FROM book_readings")
    
    # Obtém o ID do usuário 'teste'
    cursor.execute("SELECT id FROM users WHERE username = 'teste'")
    user_id = cursor.fetchone()[0]
    
    # Adiciona leituras de livros de Ficção Científica
    for book_id in range(1, 4):  # Adiciona 3 livros de Ficção Científica
        cursor.execute(
            "INSERT INTO book_readings (user_id, book_id) VALUES (?, ?)",
            (user_id, book_id)
        )
        
        # Atualiza os pontos do usuário
        cursor.execute("SELECT pages FROM books WHERE id = ?", (book_id,))
        pages = cursor.fetchone()[0]
        points = 1 + (pages // 100)
        
        cursor.execute(
            "UPDATE users SET points = points + ? WHERE id = ?",
            (points, user_id)
        )
    
    # Adiciona leituras de livros de Fantasia
    for book_id in range(6, 8):  # Adiciona 2 livros de Fantasia
        cursor.execute(
            "INSERT INTO book_readings (user_id, book_id) VALUES (?, ?)",
            (user_id, book_id)
        )
        
        # Atualiza os pontos do usuário
        cursor.execute("SELECT pages FROM books WHERE id = ?", (book_id,))
        pages = cursor.fetchone()[0]
        points = 1 + (pages // 100)
        
        cursor.execute(
            "UPDATE users SET points = points + ? WHERE id = ?",
            (points, user_id)
        )
    
    conn.commit()
    print("Leituras para o usuário 'teste' adicionadas com sucesso!")

def main():
    """Função principal para popular o banco de dados."""
    # Verifica se o banco de dados já existe e o remove
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"Banco de dados existente removido: {DB_PATH}")
    
    # Cria uma nova conexão com o banco de dados
    conn = sqlite3.connect(DB_PATH)
    
    try:
        # Cria as tabelas
        create_tables(conn)
        
        # Popula as tabelas
        populate_users(conn)
        populate_books(conn)
        populate_trophies(conn)
        add_readings_for_teste_user(conn)
        
        print(f"Banco de dados criado e populado com sucesso: {DB_PATH}")
    except Exception as e:
        print(f"Erro ao popular o banco de dados: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
