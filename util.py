def recv_all(sock):
    BUFF_SIZE = 4096
    data = b''
    while True:
        part, address = sock.recvfrom(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            break
    return data
