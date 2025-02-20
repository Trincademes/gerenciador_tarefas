from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from flask_mail import Mail, Message
from enviar_email import configurar_mail, enviar_email  # Importa as funções de enviar e-mail
import os

# Inicializando o Flask e o banco de dados
app = Flask(__name__, template_folder=os.getcwd())  # Faz o Flask procurar os templates na raiz
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tarefas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Configuração do Flask-Mail
mail = configurar_mail(app)  # Configura o Flask-Mail

# Modelo de Tarefa
class Tarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200))
    prioridade = db.Column(db.String(10), nullable=False)
    data_vencimento = db.Column(db.Date, nullable=False)

# Função para verificar tarefas e enviar e-mails
def verificar_tarefas_e_enviar_email():
    hoje = datetime.today().date()
    tarefas = Tarefa.query.filter(Tarefa.data_vencimento == hoje + timedelta(days=1)).all()  # Verifica se a tarefa vence amanhã
    
    for tarefa in tarefas:
        enviar_email(mail, [tarefa])  # Envia o e-mail para a tarefa com vencimento amanhã

# Agendando a verificação diária
scheduler = BackgroundScheduler()
scheduler.add_job(verificar_tarefas_e_enviar_email, 'interval', days=1, start_date=datetime.today())
scheduler.start()

# Rota principal (exibe tarefas e permite filtragem por data)
@app.route("/", methods=["GET", "POST"])
def index():
    hoje = datetime.today().date()

    # Filtragem por data
    if request.method == "POST":
        filtro_data = request.form.get("filtro_data")
        if filtro_data:
            tarefas = Tarefa.query.filter(Tarefa.data_vencimento == filtro_data).all()
        else:
            tarefas = Tarefa.query.all()
    else:
        tarefas = Tarefa.query.all()

    return render_template("index.html", tarefas=tarefas, hoje=hoje)

# Rota para adicionar uma nova tarefa
@app.route("/adicionar", methods=["GET", "POST"])
def adicionar():
    if request.method == "POST":
        titulo = request.form["titulo"]
        descricao = request.form["descricao"]
        prioridade = request.form["prioridade"]
        data_vencimento = datetime.strptime(request.form["data_vencimento"], "%Y-%m-%d").date()

        tarefa = Tarefa(titulo=titulo, descricao=descricao, prioridade=prioridade, data_vencimento=data_vencimento)
        db.session.add(tarefa)
        db.session.commit()
        return redirect("/")

    return render_template("adicionar.html")

# Rota para editar uma tarefa existente
@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    tarefa = Tarefa.query.get(id)

    if request.method == "POST":
        tarefa.titulo = request.form["titulo"]
        tarefa.descricao = request.form["descricao"]
        tarefa.prioridade = request.form["prioridade"]
        tarefa.data_vencimento = datetime.strptime(request.form["data_vencimento"], "%Y-%m-%d").date()

        db.session.commit()
        return redirect("/")

    return render_template("editar.html", tarefa=tarefa)

# Rota para excluir uma tarefa
@app.route("/excluir/<int:id>", methods=["GET", "POST"])
def excluir(id):
    tarefa = Tarefa.query.get(id)
    db.session.delete(tarefa)
    db.session.commit()
    return redirect("/")

# Rota para enviar o e-mail com todas as tarefas
@app.route("/enviar_email", methods=["GET"])
def enviar_email_route():
    tarefas = Tarefa.query.all()  # Recupera todas as tarefas
    enviar_email(mail, tarefas)   # Envia o e-mail com as tarefas
    return "E-mail enviado com sucesso!"

if __name__ == "__main__":
    app.run(debug=True)
