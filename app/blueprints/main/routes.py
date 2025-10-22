from flask import request, redirect, render_template, url_for
from app.blueprints.main import main_bp

@main_bp.route('/')
def index():
    usuario = request.cookies.get('usuario')
    if usuario:
        return render_template('main/index.html', usuario=usuario)
    return redirect(url_for('auth.login'))