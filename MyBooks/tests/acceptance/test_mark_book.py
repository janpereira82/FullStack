import pytest
from app import create_app
from models.models import db, User, Book, BookReading, Trophy, UserTrophy
from flask_login import login_user

@pytest.fixture
def client():
    """Configura um cliente de teste para a aplicação Flask."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Criar um usuário de teste
            user = User(username="teste", email="teste@example.com")
            user.set_password("senha123")
            db.session.add(user)
            
            # Criar livros de teste
            books = [
                Book(title="Livro Teste 1", author="Autor Teste", pages=200, genre="Ficção Científica", 
                     description="Descrição do livro teste 1"),
                Book(title="Livro Teste 2", author="Autor Teste", pages=300, genre="Ficção Científica", 
                     description="Descrição do livro teste 2"),
                Book(title="Livro Teste 3", author="Autor Teste", pages=150, genre="Ficção Científica", 
                     description="Descrição do livro teste 3"),
                Book(title="Livro Teste 4", author="Autor Teste", pages=250, genre="Ficção Científica", 
                     description="Descrição do livro teste 4"),
                Book(title="Livro Teste 5", author="Autor Teste", pages=400, genre="Ficção Científica", 
                     description="Descrição do livro teste 5")
            ]
            for book in books:
                db.session.add(book)
            
            # Criar troféu de teste
            trophy = Trophy(name="Leitor de Ficção Científica", description="Leu 5 livros de Ficção Científica", 
                           genre="Ficção Científica")
            db.session.add(trophy)
                
            db.session.commit()
        yield client

def login(client, email="teste@example.com", password="senha123"):
    """Função auxiliar para fazer login."""
    return client.post('/login', data={
        'email': email,
        'password': password
    }, follow_redirects=True)

def test_mark_book_as_read(client):
    """Teste de aceitação: Verificar se o sistema registra corretamente o livro como lido."""
    login(client)
    response = client.post('/mark_as_read/1', follow_redirects=True)
    assert response.status_code == 200
    
    # Verificar se o livro foi marcado como lido
    with client.application.app_context():
        reading = BookReading.query.filter_by(user_id=1, book_id=1).first()
        assert reading is not None

def test_points_calculation(client):
    """Teste de aceitação: Verificar se os pontos são calculados corretamente com base no número de páginas."""
    login(client)
    
    # Marcar livro 1 como lido (200 páginas = 3 pontos)
    client.post('/mark_as_read/1', follow_redirects=True)
    
    with client.application.app_context():
        user = User.query.get(1)
        assert user.points == 3  # 1 ponto base + 2 pontos por 200 páginas
        
    # Marcar livro 3 como lido (150 páginas = 2 pontos)
    client.post('/mark_as_read/3', follow_redirects=True)
    
    with client.application.app_context():
        user = User.query.get(1)
        assert user.points == 5  # 3 pontos anteriores + 2 pontos do novo livro

def test_trophy_award(client):
    """Teste de aceitação: Verificar se o troféu é concedido ao atingir 5 livros do mesmo estilo."""
    login(client)
    
    # Marcar 5 livros de Ficção Científica como lidos
    for i in range(1, 6):
        client.post(f'/mark_as_read/{i}', follow_redirects=True)
    
    # Verificar se o troféu foi concedido
    with client.application.app_context():
        user_trophy = UserTrophy.query.filter_by(user_id=1, trophy_id=1).first()
        assert user_trophy is not None

def test_prevent_duplicate_reading(client):
    """Teste de aceitação: Verificar se não é possível marcar o mesmo livro como lido mais de uma vez."""
    login(client)
    
    # Marcar livro 1 como lido pela primeira vez
    client.post('/mark_as_read/1', follow_redirects=True)
    
    # Tentar marcar o mesmo livro novamente
    response = client.post('/mark_as_read/1', follow_redirects=True)
    assert b'Voc\xc3\xaa j\xc3\xa1 marcou este livro como lido' in response.data
    
    # Verificar se há apenas um registro de leitura
    with client.application.app_context():
        readings = BookReading.query.filter_by(user_id=1, book_id=1).count()
        assert readings == 1
