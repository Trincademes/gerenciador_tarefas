from flask_mail import Mail, Message

# Função para configurar o Flask-Mail
def configurar_mail(app):
    """Configura o Flask-Mail com as credenciais e servidor do Gmail"""
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True  # Habilita TLS
    app.config['MAIL_USERNAME'] = 'vcavalciuk@gmail.com'  # Substitua pelo seu e-mail
    app.config['MAIL_PASSWORD'] = 'yrzm nynl lvym mjvc'  # Senha de app gerada
    app.config['MAIL_DEFAULT_SENDER'] = 'vcavalciuk@gmail.com'  # Substitua pelo seu e-mail

    mail = Mail(app)
    return mail

# Função para enviar um e-mail
def enviar_email(mail, tarefas):
    """Função para enviar um e-mail com a lista de tarefas"""
    # Criação do conteúdo do e-mail
    corpo = "Aqui estão as suas tarefas com vencimento próximo:\n\n"
    for tarefa in tarefas:
        corpo += f"ID: {tarefa.id}, Título: {tarefa.titulo}, Descrição: {tarefa.descricao}, Prioridade: {tarefa.prioridade}, Data de Vencimento: {tarefa.data_vencimento}\n"

    # Criação do e-mail
    msg = Message(
        'Alerta de Vencimento de Tarefa',
        recipients=['pedrovieiracavalciuk@gmail.com']  # Substitua pelo e-mail do destinatário
    )
    msg.body = corpo  # Corpo do e-mail

    try:
        mail.send(msg)
    except Exception as e:
        print(f'Ocorreu um erro ao tentar enviar o e-mail: {e}')
