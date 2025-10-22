from flask import redirect, request, make_response, url_for, render_template, abort, flash
from app.blueprints.auth import auth_bp
from app.models.user import Usuario

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.cookies.get('usuario'):
        return redirect(url_for('main.index'))
    
    mensagem = "Faça login para acessar nossos serviços"
    
    if request.method == 'POST':
        email = request.form['email'].lower()
        senha = request.form['senha']

        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and usuario.senha == senha:
            resposta = make_response(redirect(url_for('main.index')))
            resposta.set_cookie('usuario', usuario.nome, max_age=60*30)
            return resposta
        mensagem = "Usuário ou senha inválido(s)"
    
    flash(mensagem)
    return render_template('auth/login.html')
    
@auth_bp.route('/logout', methods=['GET'])
def logout():
    resposta = make_response(redirect(url_for('auth.login')))
    resposta.set_cookie('usuario', '', expires=0)
    return resposta