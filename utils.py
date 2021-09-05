def tratar_ping(dados):
    args = dados.split(b' ')
    if(len(args)==1):
        dados_env = b':server PONG server :\r\n'
    else:
        dados_env = b':server PONG server :' + args[1] + b'\n'
    return dados_env

def tratar_nick_valido(servidor, conexao, nick):
    dados_env = ""
    if servidor.checa_nick_existe(nick):
        apelido_atual = conexao.get_nick() if not conexao.is_initial_nick() else b'*'
        dados_env = f":server 433 {apelido_atual.decode()} {nick.decode()} :Nickname is already in use\r\n".encode()
    elif conexao.is_initial_nick():
        servidor.mudar_nick_conexao(conexao, nick)
        conexao.enviar(f":server 001 {nick.decode()} :Welcome\r\n".encode())
        dados_env = f":server 422 {nick.decode()} :MOTD File is missing\r\n".encode()    
    else:
        dados_env = f":{conexao.get_nick().decode()} NICK {nick.decode()}\r\n".encode()
        servidor.mudar_nick_conexao(conexao, nick)
    return dados_env
