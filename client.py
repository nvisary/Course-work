import socket
import time
import matplotlib.pyplot as plt

BUF_SIZE = 4096

run_client = True
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

commands = {"STOP_CLIENT": 0, "RUN_TEST1": 1, "RUN_TEST2": 2, "PRINT_GRAPHICS": 3}
img = open("img/cat.bmp", "rb")
img_size = len(img.read())
img.seek(0)

speeds_udp = []
times_udp = []
times_tcp = []
speeds_tcp = []
distance = [5, 10, 15, 20]

while run_client:
    print("Client actions:")
    for key, command in commands.items():
        print("command {0}: {1}".format(command, key))

    print("******\nData: ")
    print("UDP\nSpeeds: ", speeds_udp)
    print("Times: ", times_udp)
    print("TCP\nSpeeds: ", speeds_tcp)
    print("Times: ", times_tcp)
    print("******")

    command = int(input("Input command: "))
    if command == commands["STOP_CLIENT"]:
        run_client = False
        udp_socket.close()

    if command == commands["RUN_TEST1"]:
        print("Тест 1.")
        print("Скорость UDP соединения в зависимости от расстояния.")
        print("Запустите Test1 на сервере.")
        speeds_udp = []
        times_udp = []
        server_ip = input("Введите ip-адресс UDP сервера: ")
        server_port = int(input("Введите порт UDP сервера: "))

        for dist in distance:
            print("Отойдите на расстояние в {0} метров от точки доступа.".format(dist))
            input("Для продолжения нажмите enter")
            print("Начинаю тестирование.")
            print("Отправляю картинку.")
            start_time = time.time()

            count_parts = img_size // BUF_SIZE
            parts = 0
            img.seek(0)
            print("Передача...")
            while True:
                part = img.read(BUF_SIZE)
                udp_socket.sendto(part, (server_ip, server_port))
                parts += 1
                if len(part) < BUF_SIZE:
                    break
            end_time = time.time()
            print("Передача окончена.")
            send_time = end_time - start_time
            print("start time: ", start_time)
            print("end time: ", end_time)
            if send_time:
                speed = BUF_SIZE * parts / send_time / 1024 / 1024
            else:
                speed = 0
            speeds_udp.append(speed)
            times_udp.append(send_time)
            print("Затраченное на отправку время: ", send_time)
            print("Скорость: {0} Б/Сек".format(speed))
    if command == commands["RUN_TEST2"]:
        print("Тест 2.")
        print("Скорость TCP соединения в зависимости от расстояния.")
        print("Запустите Test2 на сервере.")
        server_ip = input("Введите ip-адресс TCP сервера: ")
        server_port = int(input("Введите порт TCP сервера: "))
        tcp_socket.connect((server_ip, server_port))
        print("Соединение установлено.")
        for dist in distance:
            print("Отойдите на расстояние в {0} метров от точки доступа.".format(dist))
            input("Для продолжения нажмите enter")
            print("Начинаю тестирование.")
            print("Отправляю картинку.")
            img.seek(0)
            start_time = time.time()
            tcp_socket.send(img.read())
            end_time = time.time()
            elapsed_time = end_time - start_time
            speed = img_size / elapsed_time / 1024 / 1024
            times_tcp.append(elapsed_time)
            speeds_tcp.append(speed)
            print("Затраченное на отправку время: ", elapsed_time)
            print("Скорость: {0} Mб/Сек".format(speed))
    if command == commands["PRINT_GRAPHICS"]:
        if len(times_udp) == len(distance) == len(speeds_udp) == len(speeds_tcp):
            plt.title("Скорость от расстояния")
            plt.xlabel("Расстояние")
            plt.ylabel("Скорость передачи Мб/с")
            plt.plot(distance, speeds_udp, label="speed UDP")
            plt.plot(distance, speeds_tcp, label="speed TCP")
            plt.legend()
            plt.show()

            plt.title("Время передачи от расстояния")
            plt.xlabel("Расстояние")
            plt.ylabel("Время передачи с")
            plt.plot(distance, times_udp, label="time UDP")
            plt.plot(distance, times_tcp, label="time TCP")
            plt.legend()
            plt.show()
