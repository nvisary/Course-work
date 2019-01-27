BUFF_SIZE = 4096


def recv_all(sock, count_parts):
    data = b''
    count = 0
    while True:
        try:
            part, address = sock.recvfrom(BUFF_SIZE)
            sock.settimeout(1)
            count += 1
            data += part
            if len(part) < BUFF_SIZE:
                break
        except:
            break
    lost = count / count_parts
    return data, lost
