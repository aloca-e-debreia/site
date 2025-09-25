class Usuario:
    def __init__(self, user_id, nome, sobrenome, cpf, idade, email, senha):
        self.__user_id = user_id
        self.__nome = nome
        self.__sobrenome = sobrenome
        self.__idade = idade
        self.__cpf = cpf
        self.__email = email
        self.__senha = senha

    @property
    def user_id(self):
        return self.__user_id
    @user_id.setter
    def id (self, valor):
        self.__user_id = valor

    @property
    def nome(self):
        return self.__nome
    @nome.setter
    def nome (self, valor):
        self.__nome = valor
    
    @property
    def sobrenome(self):
        return self.__sobrenome
    @sobrenome.setter
    def sobrenome (self, valor):
        self.__sobrenome = valor

    @property
    def idade(self):
        return self.__idade
    @idade.setter
    def idade(self, valor):
        self.__idade = int(valor)
    
    @property
    def cpf(self):
        return self.__cpf
    @cpf.setter
    def cpf (self, valor):
        self.__cpf = valor

    @property
    def email(self):
        return self.__email
    @email.setter
    def email(self, valor):
        self.__email = valor

    @property
    def senha(self):
        return self.__senha
    @senha.setter
    def senha(self, valor):
        self.__senha = valor

class Usuarios:
    def __init__(self):
        self.__lista = dict()
        self.__next_id = 1
    
    @property
    def lista(self):
        return self.__lista
    
    @property
    def next_id(self):
        return self.__next_id
    @next_id.setter
    def next_id(self, valor):
        self.__next_id = valor

    def criar(self, usuario: Usuario):
        self.__lista[usuario.user_id] = usuario
        self.__next_id += 1
        with open('app/models/db.txt', 'a+') as file:
            file.write(f"{usuario.user_id} {usuario.nome} {usuario.sobrenome} {usuario.cpf} {usuario.idade} {usuario.email} {usuario.senha}\n")

    def remover(self, usuario: Usuario):
        self.__lista.pop(usuario.user_id)

usuarios = Usuarios()

with open('app/models/db.txt', 'r+') as file:
    while (linha := file.readline().split()):
        usuario = Usuario(user_id=int(linha[0]), nome=linha[1], sobrenome=linha[2], cpf=linha[3], idade=int(linha[4]), email=linha[5], senha=linha[6])
        usuarios.lista[usuario.user_id] = usuario