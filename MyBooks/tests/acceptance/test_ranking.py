import pytest
from app import create_app
from models.models import db, User
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
            # Criar usuários de teste com diferentes pontuações
            users = [
                User(username="user1", email="user1@example.com", points=30),
                User(username="user2", email="user2@example.com", points=25),
                User(username="user3", email="user3@example.com", points=20),
                User(username="user4", email="user4@example.com", points=15),
                User(username="user5", email="user5@example.com", points=10),
                User(username="user6", email="user6@example.com", points=8),
                User(username="user7", email="user7@example.com", points=6),
                User(username="user8", email="user8@example.com", points=4),
                User(username="user9", email="user9@example.com", points=2),
                User(username="user10", email="user10@example.com", points=1),
                User(username="user11", email="user11@example.com", points=0),
                User(username="teste", email="teste@example.com", points=5)
            ]
            
            for user in users:
                user.set_password("senha123")
                db.session.add(user)
                
            db.session.commit()
        yield client

def login(client, email="teste@example.com", password="senha123"):
    """Função auxiliar para fazer login."""
    return client.post('/login', data={
        'email': email,
        'password': password
    }, follow_redirects=True)

def test_ranking_display(client):
    """Teste de aceitação: Verificar se o ranking exibe os 10 usuários com maior pontuação em ordem decrescente."""
    login(client)
    response = client.get('/ranking')
    assert response.status_code == 200
    
    # Verificar se o título da página está correto
    assert b'Ranking dos Leitores' in response.data
    
    # Verificar se os usuários são exibidos em ordem decrescente de pontuação
    assert response.data.find(b'user1') < response.data.find(b'user2')
    assert response.data.find(b'user2') < response.data.find(b'user3')
    
    # Verificar se apenas os 10 primeiros usuários são exibidos
    assert b'user1' in response.data
    assert b'user10' in response.data
    assert b'user11' not in response.data  # user11 tem 0 pontos e não deve aparecer no top 10

def test_ranking_user_info(client):
    """Teste de aceitação: Verificar se as informações de cada usuário (nome e pontuação) são exibidas corretamente."""
    login(client)
    response = client.get('/ranking')
    assert response.status_code == 200
    
    # Verificar se o nome e a pontuação dos usuários são exibidos
    assert b'user1' in response.data
    assert b'30 pontos' in response.data
    
    assert b'user5' in response.data
    assert b'10 pontos' in response.data

def test_ranking_current_user_highlight(client):
    """Teste de aceitação: Verificar se o usuário atual é destacado no ranking."""
    login(client)
    response = client.get('/ranking')
    assert response.status_code == 200
    
    # Verificar se o usuário atual é destacado
    assert b'teste' in response.data
    assert b'Voc\xc3\xaa' in response.data  # "Você" em UTF-8
