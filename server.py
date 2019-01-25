# сервер запускаем на Raspberry
# он ждет подключения, обрабатывая команды / либо команды вводятся с клавиатуры
import socket


commands = {0: "STOP_SERVER", 1: "RUN_TEST1"}

run_server = True
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_port = int(input("Введите порт UDP сервера: "))
udp_socket.bind(("", server_port))

while run_server:
    print("Server actions: ")
    for key, command in commands.items():
        print("command {1}: {0}".format(command, key))

    command = input("Input command: ")
    if command == commands[0]:
        run_server = False

    if command == commands[1]:
        print("Тест 1.")
        print("Скорость UDP соединения в зависимости от расстояния.")
        distance = [5, 10, 15, 20]
        print("Запустите Test1 на клиенте.")
        for dist in distance:

            print("Сервер UDP запущен и ожидает данных на порту {0}".format(server_port))

            buf_size, address = udp_socket.recvfrom(1024)
            buf_size = int(buf_size.decode("utf-8"))
            print("Получен размер изображения: {0}".format(buf_size))
            print("Ожидаю отправки изображения.")
            udp_socket.sendto(bytes("READY", "utf-8"), address)
            file_data, address = udp_socket.recvfrom(buf_size)

            f = open("received.jpg", "wb")
            f.write(file_data)
            f.close()
            print("Изображение принято и сохранено.")
