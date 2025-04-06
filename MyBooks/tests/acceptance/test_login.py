import pytest
from app import create_app
from models.models import db, User
import os
import tempfile

@pytest.fixture
def client():
    """Configura um cliente de teste para a aplicação Flask."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Criar um usuário de teste
            user = User(username="teste", email="teste@example.com")
            user.set_password("senha123")
            db.session.add(user)
            db.session.commit()
        yield client

def test_login_page(client):
    """Teste de aceitação: Verificar se a página de login é exibida corretamente."""
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data
    assert b'Email' in response.data
    assert b'Senha' in response.data

def test_login_success(client):
    """Teste de aceitação: Verificar se o usuário consegue fazer login com credenciais válidas."""
    response = client.post('/login', data={
        'email': 'teste@example.com',
        'password': 'senha123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Livros Dispon' in response.data  # Verifica se foi redirecionado para a página de livros

def test_login_invalid_credentials(client):
    """Teste de aceitação: Verificar se o sistema exibe mensagem de erro para credenciais inválidas."""
    response = client.post('/login', data={
        'email': 'teste@example.com',
        'password': 'senha_errada'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Credenciais inv' in response.data  # Verifica se a mensagem de erro é exibida

def test_login_redirect(client):
    """Teste de aceitação: Verificar se o usuário é redirecionado para a página principal após o login."""
    response = client.post('/login', data={
        'email': 'teste@example.com',
        'password': 'senha123'
    }, follow_redirects=False)
    assert response.status_code == 302  # Código de redirecionamento
    assert response.headers['Location'] == '/books'  # Verifica se redireciona para /books
