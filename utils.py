def tratar_ping(dados):
    args = dados.split(b' ')
    if(len(args)==1):
        dados_env = b':server PONG server :\r\n'
    else:
        dados_env = b':server PONG server :' + args[1] + b'\r\n'
    return dados_env

def tratar_nick_valido(servidor, conexao, nick):
    dados_env = ""
    if servidor.checa_nick_existe(nick):
        apelido_atual = conexao.get_nick() if not conexao.initial_nick else b'*'
        dados_env = f":server 433 {apelido_atual.decode()} {nick.decode()} :Nickname is already in use\r\n".encode()
    elif conexao.is_initial_nick():
        servidor.mudar_nick_conexao(conexao, nick)
        dados_env = f":server 001 {nick.decode()} :Welcome\r\n".encode()    
    else:
        servidor.mudar_nick_conexao(conexao, nick)
        dados_env = f":{conexao.get_nick().decode()} NICK {nick.decode()}\r\n".encode()
    return dados_env
