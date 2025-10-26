import uuid
from app import db
from flask_security.models import fsqla_v3

role_usuario = db.Table(
    'role_usuario',
    db.Column('usuario_id', db.Integer(), db.ForeignKey('usuario.id'), primary_key=True),
    db.Column('funcao_id', db.Integer(), db.ForeignKey('role.id'), primary_key=True)
)

class Role(db.Model, fsqla_v3.FsRoleMixin):
    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    descricao = db.Column(db.String(200), nullable=True)

class Usuario(db.Model, fsqla_v3.FsUserMixin):
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=True)
    cpf = db.Column(db.String(11), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    active = db.Column(db.Boolean(), default=True)
    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))

    roles = db.relationship('Role', secondary=role_usuario, backref=db.backref('usuarios', lazy='dynamic'))

    def __repr__(self):
        return f"<Usuario(nome='{self.nome}, idade='{self.idade}', cpf='{self.cpf}', email='{self.email}', senha='{self.senha}')>"
    
def select_users_with_role(role):
    user_role = Role.query.filter_by(name=role).first()
    if user_role:
        users = user_role.usuarios
        return users
    return []