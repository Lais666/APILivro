import pytest
from main import app, db
from models import Livro, Usuario
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
        with app.app_context():
            db.drop_all()

def test_get_livro(client):
    response = client.get('/livro')
    assert response.status_code == 200
    assert b'Lista de Livros' in response.data

def test_post_livro(client):
    with client.session_transaction() as session:
        session['id_usuario'] = 1

    response = client.post('/livro', json={
        'id_livro': 1,
        'titulo': 'Python Testing',
        'autor': 'Author Name',
        'ano_publicacao': 2021
    })
    assert response.status_code == 200
    assert b'Livro Cadastrado com Sucesso' in response.data  # Esta linha precisa estar alinhada corretamente


def test_login(client):
    with app.app_context():
        usuario = Usuario(id_usuario=1, email='test@example.com', senha='123456')
        db.session.add(usuario)
        db.session.commit()

    response = client.post('/login', json={
        'email': 'test@example.com',
        'senha': '123456'
    })
    assert response.status_code == 200
    assert b'Login com sucesso' in response.data

def test_logout(client):
    with client.session_transaction() as session:
        session['id_usuario'] = 1

    response = client.post('/logout')
    assert response.status_code == 200
    assert b'Logout bem Sucedido' in response.data

def test_put_livro(client):
    with client.session_transaction() as session:
        session['id_usuario'] = 1

    with app.app_context():
        livro = Livro(id_livro=1, titulo='Old Title', autor='Old Author', ano_publicacao=2020)
        db.session.add(livro)
        db.session.commit()

    response = client.put('/livro/1', json={
        'titulo': 'New Title',
        'autor': 'New Author',
        'ano_publicacao': 2022
    })
    assert response.status_code == 200
    assert b'Livro atualizado com sucesso' in response.data

def test_delete_livro(client):
    with client.session_transaction() as session:
        session['id_usuario'] = 1

    with app.app_context():
        livro = Livro(id_livro=1, titulo='Title', autor='Author', ano_publicacao=2020)
        db.session.add(livro)
        db.session.commit()

    response = client.delete('/livro/1')
    assert response.status_code == 200

    response_data = json.loads(response.data.decode('utf-8'))
    assert 'Livro excluído com sucesso' in response_data['mensagem']
