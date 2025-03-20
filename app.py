from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from flask_mail import Mail, Message
from enviar_email import configurar_mail, enviar_email

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tarefas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

mail = configurar_mail(app)

class Tarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200))
    prioridade = db.Column(db.String(10), nullable=False)
    data_vencimento = db.Column(db.Date, nullable=False)

def verificar_tarefas_e_enviar_email():
    hoje = datetime.today().date()
    tarefas = Tarefa.query.filter(Tarefa.data_vencimento == hoje + timedelta(days=1)).all()
    
    for tarefa in tarefas:
        enviar_email(mail, [tarefa])

scheduler = BackgroundScheduler()
scheduler.add_job(verificar_tarefas_e_enviar_email, 'interval', days=1, start_date=datetime.today())
scheduler.start()

@app.route("/", methods=["GET", "POST"])
def index():
    hoje = datetime.today().date()

    if request.method == "POST":
        filtro_data = request.form.get("filtro_data")
        if filtro_data:
            tarefas = Tarefa.query.filter(Tarefa.data_vencimento == filtro_data).all()
        else:
            tarefas = Tarefa.query.all()
    else:
        tarefas = Tarefa.query.all()

    return render_template("index.html", tarefas=tarefas, hoje=hoje)

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

@app.route("/excluir/<int:id>", methods=["GET", "POST"])
def excluir(id):
    tarefa = Tarefa.query.get(id)
    db.session.delete(tarefa)
    db.session.commit()
    return redirect("/")

@app.route("/enviar_email", methods=["GET"])
def enviar_email_route():
    tarefas = Tarefa.query.all()
    enviar_email(mail, tarefas)
    return "E-mail enviado com sucesso!"

if __name__ == "__main__":
    app.run(debug=True)
