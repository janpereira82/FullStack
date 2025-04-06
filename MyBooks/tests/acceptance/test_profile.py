import pytest
from app import create_app
from models.models import db, User, Book, Trophy, BookReading, UserTrophy
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
            user = User(username="teste", email="teste@example.com", points=10)
            user.set_password("senha123")
            db.session.add(user)
            
            # Criar livros de teste
            books = [
                Book(title="Livro Teste 1", author="Autor Teste", pages=200, genre="Ficção Científica", 
                     description="Descrição do livro teste 1"),
                Book(title="Livro Teste 2", author="Autor Teste", pages=300, genre="Fantasia", 
                     description="Descrição do livro teste 2")
            ]
            for book in books:
                db.session.add(book)
            
            # Criar troféus de teste
            trophies = [
                Trophy(name="Leitor de Ficção Científica", description="Leu 5 livros de Ficção Científica", 
                      genre="Ficção Científica"),
                Trophy(name="Leitor de Fantasia", description="Leu 5 livros de Fantasia", 
                      genre="Fantasia")
            ]
            for trophy in trophies:
                db.session.add(trophy)
                
            db.session.commit()
            
            # Registrar leituras e troféus para o usuário de teste
            reading1 = BookReading(user_id=1, book_id=1)
            db.session.add(reading1)
            
            user_trophy = UserTrophy(user_id=1, trophy_id=1)
            db.session.add(user_trophy)
            
            db.session.commit()
        yield client

def login(client, email="teste@example.com", password="senha123"):
    """Função auxiliar para fazer login."""
    return client.post('/login', data={
        'email': email,
        'password': password
    }, follow_redirects=True)

def test_profile_points_display(client):
    """Teste de aceitação: Verificar se os pontos do usuário são exibidos corretamente."""
    login(client)
    response = client.get('/profile')
    assert response.status_code == 200
    
    # Verificar se os pontos são exibidos corretamente
    assert b'10 pontos' in response.data

def test_profile_trophies_display(client):
    """Teste de aceitação: Verificar se todos os troféus conquistados são exibidos corretamente."""
    login(client)
    response = client.get('/profile')
    assert response.status_code == 200
    
    # Verificar se o troféu conquistado é exibido
    assert b'Leitor de Fic' in response.data
    assert b'Leu 5 livros de Fic' in response.data
    
    # Verificar se o troféu não conquistado não é exibido na seção de troféus conquistados
    assert b'Leitor de Fantasia' not in response.data

def test_profile_missing_trophies_info(client):
    """Teste de aceitação: Verificar se há informações sobre como conquistar novos troféus."""
    login(client)
    response = client.get('/profile')
    assert response.status_code == 200
    
    # Verificar se há informações sobre troféus não conquistados
    assert b'Pr\xc3\xb3ximos Trof\xc3\xa9us' in response.data  # "Próximos Troféus" em UTF-8
    assert b'Leitor de Fantasia' in response.data
    
    # Verificar se há informações sobre o progresso
    assert b'1/5' in response.data or b'0/5' in response.data

def test_profile_books_read(client):
    """Teste de aceitação: Verificar se os livros lidos pelo usuário são exibidos corretamente."""
    login(client)
    response = client.get('/profile')
    assert response.status_code == 200
    
    # Verificar se os livros lidos são exibidos
    assert b'Livros que J\xc3\xa1 Li' in response.data  # "Livros que Já Li" em UTF-8
    assert b'Livro Teste 1' in response.data
    
    # Verificar se livros não lidos não são exibidos
    assert b'Livro Teste 2' not in response.data
