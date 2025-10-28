from flask import render_template

def register_errors(app):

    @app.errorhandler(404)
    def not_found(error):
        error_data = {
            'titulo' : 'Erro 404 - Página não encontrada',
            'mensagem' : 'Ops, parece que você se perdeu na nossa locadora',
            'codigo' : 404
        }
        return render_template('main/errors.html', error_data=error_data), 404

    @app.errorhandler(403)
    def forbidden(error):
        error_data = {
            'titulo' : 'Erro 403 - Acesso proibido',
            'mensagem' : 'Sapeca! Pare de se meter onde não deve...',
            'codigo' : 403
        }
        return render_template('main/errors.html', error_data=error_data), 403

    @app.errorhandler(401)
    def unauthorized(error):
        error_data = {
            'titulo' : 'Erro 401 - Acesso não autorizado',
            'mensagem' : 'Pra acessar nossos serviços, tem que logar, né, meu rei?',
            'codigo' : 401
        }
        return render_template('main/errors.html', error_data=error_data), 401