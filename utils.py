def tratar_ping(conexao, dados):
    args = dados.split(b' ')
    conexao.enviar(b':server PONG server :' + args[1])

def tratar_nick_valido(servidor, conexao, nick):
    servidor.mudar_nick_conexao(conexao, nick)