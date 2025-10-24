from flask import render_template

def registrar_erros(app):

    @app.errorhandler(404)
    def pagina_nao_encontrada(error):
        return render_template('main/404.html'), 404

    @app.errorhandler(403)
    def acesso_proibido(error):
        return render_template('main/403.html'), 403

    @app.errorhandler(401)
    def nao_autorizado(error):
        return render_template('main/401.html'), 401