from flask_mail import Mail, Message

def configurar_mail(app):
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'Exemplo@gmail.com'#coloque o email do remetente
    app.config['MAIL_PASSWORD'] = '**** **** **** ****'#senha do emial 
    app.config['MAIL_DEFAULT_SENDER'] = 'exemplo@gmail.com'#coloque o email do remetente

    mail = Mail(app)
    return mail

def enviar_email(mail, tarefas):
    corpo = "Aqui estão as suas tarefas com vencimento próximo:\n\n"
    for tarefa in tarefas:
        corpo += f"ID: {tarefa.id}, Título: {tarefa.titulo}, Descrição: {tarefa.descricao}, Prioridade: {tarefa.prioridade}, Data de Vencimento: {tarefa.data_vencimento}\n"

    msg = Message(
        'Alerta de Vencimento de Tarefa',
        recipients=['exemplok@gmail.com']#email do destinatario
    )
    msg.body = corpo

    try:
        mail.send(msg)
    except Exception as e:
        print(f'Ocorreu um erro ao tentar enviar o e-mail: {e}')