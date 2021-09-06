def tratar_ping(dados):
    args = dados.split(b' ')
    if(len(args) == 1):
        dados_env = b':server PONG server :\r\n'
    else:
        dados_env = b':server PONG server :' + args[1] + b'\n'
    return dados_env


def tratar_nick_valido(servidor, conexao, nick):
    dados_env = ""
    if servidor.checa_nick_existe(nick):
        apelido_atual = conexao.get_nick() if not conexao.is_initial_nick() else b'*'
        dados_env = f":server 433 {apelido_atual.decode()} {nick.decode()} :Nickname is already in use\r\n".encode(
        )
    elif conexao.is_initial_nick():
        servidor.mudar_nick_conexao(conexao, nick)
        conexao.enviar(f":server 001 {nick.decode()} :Welcome\r\n".encode())
        dados_env = f":server 422 {nick.decode()} :MOTD File is missing\r\n".encode(
        )
    else:
        dados_env = f":{conexao.get_nick().decode()} NICK {nick.decode()}\r\n".encode()
        servidor.mudar_nick_conexao(conexao, nick)
    return dados_env


def tratar_join_valido(servidor, conexao, channel):
    dados_env = ""
    servidor.incluir_conexao_canal(conexao, channel)
    dados_env = f":{conexao.get_nick().decode()} JOIN :{channel.decode()}\r\n".encode()
    channel_cons = servidor.get_channel_users(channel).copy()
    for con in channel_cons:
        con.enviar(dados_env)

    # enviar lista de membros do canal pra con que acaba de entrar
    cons_nick = [con.get_nick() for con in channel_cons]
    cons_nick.sort()
    dados_env = f':server 353 {conexao.get_nick().decode()} = {channel.decode()} :'.encode()
    
    for nick in cons_nick:
        dados_env += nick + b' '
    dados_env = dados_env[:-1]
    dados_env += b"\r\n"
    conexao.enviar(dados_env)
    dados_env = f":server 366 {conexao.get_nick().decode()} {channel.decode()} :End of /NAMES list.\r\n".encode()
    conexao.enviar(dados_env)


def tratar_part(servidor, conexao, channel):
    dados_env = ""
    channel_cons = servidor.get_channel_users(channel).copy()
    servidor.remover_conexao_canal(conexao, channel)
    dados_env = f":{conexao.get_nick().decode()} PART {channel.decode()}\r\n".encode()
    for con in channel_cons:
        con.enviar(dados_env)
