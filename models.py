from app import db

class Tarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255), nullable=True)
    prioridade = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'<Tarefa {self.titulo}>'
