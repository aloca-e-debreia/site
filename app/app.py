from flask import Flask, request, redirect, render_template, url_for
from auth.cadastro import cadastro_bp
from auth.login import login_bp

app = Flask(__name__)

app.secret_key = "minha-chave-super-secreta"

app.register_blueprint(cadastro_bp)
app.register_blueprint(login_bp)

@app.route('/')
def index():
    usuario = request.cookies.get('usuario')
    if usuario:
        return render_template('main/index.html', usuario=usuario)
    return redirect(url_for('login.login'))

if __name__ == "__main__":
    app.run(debug=True)