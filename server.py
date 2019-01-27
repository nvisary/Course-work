# сервер запускаем на Raspberry
# он ждет подключения, обрабатывая команды / либо команды вводятся с клавиатуры
import socket
import util
commands = {"STOP_SERVER": 0, "RUN_TEST1": 1}

run_server = True
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_port = int(input("Введите порт UDP сервера: "))
udp_socket.bind(("", server_port))

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
            file_data = util.recv_all(udp_socket)
            f = open("received.bmp", "wb")
            f.write(file_data)
            f.close()
            print("Изображение принято и сохранено.")


