import pytest
from app import create_app
from models.models import db, User, Book
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
                Book(title="Livro Teste 2", author="Autor Teste", pages=300, genre="Fantasia", 
                     description="Descrição do livro teste 2"),
                Book(title="Livro Teste 3", author="Autor Teste", pages=150, genre="Romance", 
                     description="Descrição do livro teste 3")
            ]
            for book in books:
                db.session.add(book)
                
            db.session.commit()
        yield client

def login(client, email="teste@example.com", password="senha123"):
    """Função auxiliar para fazer login."""
    return client.post('/login', data={
        'email': email,
        'password': password
    }, follow_redirects=True)

def test_books_list_authenticated(client):
    """Teste de aceitação: Verificar se a lista de livros é exibida corretamente para usuário autenticado."""
    login(client)
    response = client.get('/books')
    assert response.status_code == 200
    assert b'Livros Dispon' in response.data
    assert b'Livro Teste 1' in response.data
    assert b'Livro Teste 2' in response.data
    assert b'Livro Teste 3' in response.data

def test_books_list_unauthenticated(client):
    """Teste de aceitação: Verificar se usuário não autenticado é redirecionado para login."""
    response = client.get('/books', follow_redirects=False)
    assert response.status_code == 302
    assert '/login' in response.headers['Location']

def test_books_filter_by_genre(client):
    """Teste de aceitação: Verificar se é possível filtrar livros por estilo/categoria."""
    login(client)
    response = client.get('/books?genre=Fantasia')
    assert response.status_code == 200
    assert b'Livro Teste 2' in response.data
    assert b'Livro Teste 1' not in response.data
    assert b'Livro Teste 3' not in response.data

def test_book_details(client):
    """Teste de aceitação: Verificar se os detalhes de um livro são exibidos corretamente."""
    login(client)
    response = client.get('/book/1')
    assert response.status_code == 200
    assert b'Livro Teste 1' in response.data
    assert b'Autor Teste' in response.data
    assert b'200 p' in response.data
    assert b'Fic' in response.data
    assert b'Marcar como lido' in response.data
