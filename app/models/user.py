class Usuario:
    def __init__(self, nome, sobrenome, cpf, idade, email, senha):
        self.__nome = nome
        self.__sobrenome = sobrenome
        self.__idade = idade
        self.__cpf = cpf
        self.__email = email
        self.__senha = senha

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
    
    @property
    def lista(self):
        return self.__lista

    def criar(self, usuario: Usuario):
        self.__lista[usuario.email] = usuario
        with open('app/models/db.txt', 'a') as file:
            file.write(f"{usuario.nome} {usuario.sobrenome} {usuario.cpf} {usuario.idade} {usuario.email} {usuario.senha}\n")

    def remover(self, usuario: Usuario):
        self.__lista.pop(usuario.email)

usuarios = Usuarios()

with open('app/models/db.txt', 'r') as file:
    while (linha := file.readline().split()):
        usuario = Usuario(nome=linha[0], sobrenome=linha[1], cpf=linha[2], idade=int(linha[3]), email=linha[4], senha=linha[5])
        usuarios.lista[usuario.email] = usuario