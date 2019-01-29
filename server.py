# сервер запускаем на Raspberry
# он ждет подключения, обрабатывая команды / либо команды вводятся с клавиатуры
import socket
import util
import matplotlib.pyplot as plt

commands = {"STOP_SERVER": 0, "RUN_TEST1": 1, "RUN_TEST2": 2, "PRINT_GRAPHICS": 3}

run_server = True
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_tcp_port = int(input("Введите порт TCP сервера: "))
server_udp_port = int(input("Введите порт UDP сервера: "))

udp_socket.bind(("", server_udp_port))
tcp_socket.bind(("", server_tcp_port))
tcp_socket.listen(1)

img = open("img/cat.bmp", "rb")
img_size = len(img.read())

lost_packets = []
distance = [5, 10, 15, 20]

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
        print("Запустите Test1 на клиенте.")

        for dist in distance:
            print("Сервер UDP запущен и ожидает данных на порту {0}".format(server_udp_port))
            count_parts = img_size // util.BUFF_SIZE

            file_data, lost = util.recv_all(udp_socket, count_parts)
            udp_socket.settimeout(100)
            lost_packets.append(lost)
            print("Lost: ", lost)
            f = open("received.bmp", "wb")
            f.write(file_data)
            f.close()
            print("Изображение принято и сохранено.")

    if command == commands["RUN_TEST2"]:
        print("Тест 2.")
        print("Скорость TCP соединения в зависимости от расстояния")
        print("Сервер TCP запущен и ожидает данных на порту {0}".format(server_tcp_port))
        print("Запустите Test2 на клиенте.")
        connection, address = tcp_socket.accept()

        for dist in distance:

            file_data = connection.recv(img_size)
            f = open("tcp_received{0}.bmp".format(dist), "wb")
            f.write(file_data)
            f.close()


    if command == commands["PRINT_GRAPHICS"]:
        if len(lost_packets) == len(distance):
            plt.title("UDP потери от расстояния")
            plt.xlabel("Расстояние м")
            plt.ylabel("Потерянные пакеты %")
            plt.plot(distance, lost_packets)
            plt.show()
