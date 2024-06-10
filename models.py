from main import db
class Livro(db.Model):
    id_livro = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(254))
    autor = db.Column(db.String(100))
    ano_publicacao = db.Column(db.Integer)

class Usuario(db.Model):
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(254))
    senha = db.Column(db.String(100))

