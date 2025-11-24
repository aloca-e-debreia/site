import uuid
from app import db
from flask_security.models import fsqla_v3
from sqlalchemy.ext.hybrid import hybrid_property
from ..utils.crypto import encrypt_data, decrypt_data

role_user = db.Table(
    'role_user',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id'), primary_key=True),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'), primary_key=True)
)

class Role(db.Model, fsqla_v3.FsRoleMixin):
    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(200), nullable=True)

class User(db.Model, fsqla_v3.FsUserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), unique=True)

    name = db.Column(db.String(100), nullable=False)
    birthdate = db.Column(db.Date, nullable=True)
    cpf = db.Column(db.String(11), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    _cpf_encrypted = db.Column(db.String(255), unique=True, nullable=True)

    @hybrid_property
    def cpf(self):
        return decrypt_data(self._cpf_encrypted) 

    @cpf.setter
    def cpf(self, plain_cpf):
        self._cpf_encrypted = encrypt_data(plain_cpf) 

    active = db.Column(db.Boolean(), default=True)
    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))

    roles = db.relationship('Role', secondary=role_user, backref=db.backref('users', lazy='dynamic'))
    address = db.relationship("Address", backref='user')

    def __repr__(self):
        return f"<User(name='{self.name}, birthdate='{self.birthdate}', cpf='{self.cpf}', email='{self.email}', senha='{self.password}')>"
    
def select_users_with_role(role):
    user_role = Role.query.filter_by(name=role).first()
    if user_role:
        users = user_role.users
        return users
    return []
