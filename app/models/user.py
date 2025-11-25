import hashlib
import uuid
from app import db, encrypt_data, decrypt_data
from flask_security.models import fsqla_v3
from sqlalchemy.ext.hybrid import hybrid_property

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
    
    _email_encrypted = db.Column(db.Text, unique=True, nullable=False)
    email_hash = db.Column(db.String(64), unique=True)

    password = db.Column(db.String(200), nullable=False)

    _cpf_encrypted = db.Column(db.Text, unique=True, nullable=True)
    cpf_hash = db.Column(db.String(64), unique=True)

    active = db.Column(db.Boolean(), default=True)
    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))

    roles = db.relationship('Role', secondary=role_user, backref=db.backref('users', lazy='dynamic'))
    address = db.relationship("Address", backref='user')
    
    @hybrid_property
    def cpf(self):
        if self._cpf_encrypted is None: return None
        return decrypt_data(self._cpf_encrypted) 

    @cpf.setter
    def cpf(self, plain_cpf):
        if not plain_cpf:
            self._cpf_encrypted = None
            self.cpf_hash = None
            return
        self._cpf_encrypted = encrypt_data(plain_cpf)
        self.cpf_hash = hashlib.sha256(plain_cpf.encode()).hexdigest()

    @hybrid_property
    def email(self):
        if self._email_encrypted is None: return None
        return decrypt_data(self._email_encrypted) 

    @email.setter
    def email(self, plain_email):
        if not plain_email:
            self._email_encrypted = None
            self.email_hash = None
            return 
        self._email_encrypted = encrypt_data(plain_email)
        self.email_hash = hashlib.sha256(plain_email.encode()).hexdigest()

    def __repr__(self):
        return f"<User(name='{self.name}, birthdate='{self.birthdate}', cpf='{self.cpf_hash}', email='{self.email_hash}')>"
    
def select_users_with_role(role):
    user_role = Role.query.filter_by(name=role).first()
    if user_role:
        users = user_role.users
        return users
    return []
