from flask import render_template

def registrar_erros(app):

    @app.errorhandler(404)
    def pagina_nao_encontrada(error):
        dados_erro = {
            'titulo' : 'Erro 404 - Página não encontrada',
            'mensagem' : 'Ops, parece que você se perdeu na nossa locadora',
            'codigo' : 404
        }
        return render_template('main/errors.html', dados_erro=dados_erro), 404

    @app.errorhandler(403)
    def acesso_proibido(error):
        dados_erro = {
            'titulo' : 'Erro 403 - Acesso proibido',
            'mensagem' : 'Sapeca! Pare de se meter onde não deve...',
            'codigo' : 403
        }
        return render_template('main/errors.html', dados_erro=dados_erro), 403

    @app.errorhandler(401)
    def nao_autorizado(error):
        dados_erro = {
            'titulo' : 'Erro 401 - Acesso não autorizado',
            'mensagem' : 'Pra acessar nossos serviços, tem que logar, né, meu rei?',
            'codigo' : 401
        }
        return render_template('main/errors.html', dados_erro=dados_erro), 401