import socket
import asyncio

class Servidor:
    def __init__(self, porta):
        self.nicks = {}
        self.nicks_i = 0
        s = self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', porta))
        s.listen(5)

    def registrar_monitor_de_conexoes_aceitas(self, callback):
        asyncio.get_event_loop().add_reader(self.s, lambda: callback(Conexao(self.s.accept(), self.nicks_i)))

    def adicionar_nick(self, conexao, nick):
        self.nicks_i += 1
        self.nicks[nick.lower()] = conexao

    def mudar_nick_conexao(self, conexao, nick):
        self.nicks[nick.lower()] = self.nicks.pop(conexao.get_nick().lower())
        conexao.set_nick(nick)

    def checa_nick_existe(self, nick):
        return nick.lower() in self.nicks

class Conexao:
    def __init__(self, accept_tuple, id):
        self.initial_nick = True
        self.id = id
        self.s, _ = accept_tuple
        self.nick = f'client{id}'.encode()
        self.dados_residuais = b''  #conexao.dados_residuais guarda dados que não foram anteriormente enviados com \n

    def registrar_recebedor(self, callback):
        asyncio.get_event_loop().add_reader(self.s, lambda: callback(self, self.s.recv(8192)))

    def enviar(self, dados):
        self.s.sendall(dados)

    def fechar(self):
        asyncio.get_event_loop().remove_reader(self.s)
        self.s.close()

    def set_nick(self, new_nick):
        self.nick = new_nick
        self.initial_nick = False
    
    def get_nick(self):
        return self.nick

    def get_id(self):
        return self.id

    def is_initial_nick(self):
        return self.initial_nick