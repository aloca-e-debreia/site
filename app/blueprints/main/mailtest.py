#testando

from flask import Blueprint, render_template, current_app 
from app.extensions import mail 
from flask_mail import Message 
from . import main_bp

def register_app_email(app:object)->None:

    @app.route('/teste-email')
    def teste_email():
        if not current_app.config.get('MAIL_SERVER'):
            return "Erro: Flask-Mail não configurado no app.config!", 400

        destinatario = 'joaolupyo@gmail.com' 

        msg = Message(
            subject="Teste de Configuração de E-mail (Projeto Locação)",
            recipients=[destinatario],
            body="Se você recebeu este e-mail, a configuração do Flask-Mail está correta.",
            html="<h2>Sucesso!</h2><p>A configuração do Flask-Mail está **funcionando perfeitamente**.</p>"
        )
        
        try:
            mail.send(msg)
            return f"E-mail de teste enviado para {destinatario}!"
        except Exception as e:
            return f"Erro Crítico ao Enviar E-mail: {str(e)}", 500