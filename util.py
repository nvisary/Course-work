BUFF_SIZE = 4096

def recv_all(sock):
    data = b''
    count = 0
    while True:
        part, address = sock.recvfrom(BUFF_SIZE)
        count += 1
        data += part
        print(count)
        if len(part) < BUFF_SIZE:
            break
    return data
