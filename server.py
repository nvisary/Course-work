# сервер запускаем на Raspberry
# он ждет подключения, обрабатывая команды / либо команды вводятся с клавиатуры
import socket
import util
commands = {"STOP_SERVER": 0, "RUN_TEST1": 1}

run_server = True
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_port = int(input("Введите порт UDP сервера: "))
udp_socket.bind(("", server_port))

img = open("img/cat.bmp", "rb")
img_size = len(img.read())

while run_server:
    print("Server actions: ")
    for key, command in commands.items():
        print("command {0}: {1}".format(command, key))

    command = int(input("Input command: "))
    if command == commands["STOP_SERVER"]:
        run_server = False

    if command == commands["RUN_TEST1"]:
        print("Тест 1.")
        print("Скорость UDP соединения в зависимости от расстояния.")
        distance = [5, 10, 15, 20]
        print("Запустите Test1 на клиенте.")
        for dist in distance:
            print("Сервер UDP запущен и ожидает данных на порту {0}".format(server_port))
            count_parts = img_size // util.BUFF_SIZE

            file_data, lost_packets = util.recv_all(udp_socket, count_parts)
            udp_socket.settimeout(100)
            print("Lost: ", lost_packets)
            f = open("received.bmp", "wb")
            f.write(file_data)
            f.close()
            print("Изображение принято и сохранено.")


