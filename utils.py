def tratar_ping(dados):
    args = dados.split(b' ')
    if(len(args)==1):
        dados_env = b':server PONG server :'
    else:
        dados_env = b':server PONG server :' + args[1]
    return dados_env

def tratar_nick_valido(servidor, conexao, nick):
    servidor.mudar_nick_conexao(conexao, nick)
