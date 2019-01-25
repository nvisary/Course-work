import socket
import time

run_client = True
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

commands = {"STOP_CLIENT": 0,  "RUN_TEST1": 1}
img = open("img/cat.jpg", "rb")
img_data = img.read()
buf_size = len(img_data)

while run_client:
    print("Client actions:")
    for key, command in commands.items():
        print("command {0}: {1}".format(command, key))

    command = int(input("Input command: "))
    if command == commands["STOP_CLIENT"]:
        run_client = False

    if command == commands["RUN_TEST1"]:
        speeds = []
        times = []
        distance = [5, 10, 15, 20]
        print("Тест 1.")
        print("Скорость UDP соединения в зависимости от расстояния.")
        print("Запустите Test1 на сервере.")

        server_ip = input("Введите ip-адресс UDP сервера: ")
        server_port = int(input("Введите порт UDP сервера: "))

        for dist in distance:
            print("Отойдите на расстояние в {0} метров от точки доступа.".format(dist))
            input("Для продолжения нажмите enter")
            print("Начинаю тестирование.")
            print("Отправка размера картинки.")
            udp_socket.sendto(bytes(str(buf_size), "utf-8"), (server_ip, server_port))
            print("Ожидаю готовности от сервера.")
            data, address = udp_socket.recvfrom(1024)
            data = data.decode("utf-8")
            if data == "READY":
                print("Сервер готов.")
                print("Отправляю картинку.")
                start_time = time.time()
                udp_socket.sendto(img_data, (server_ip, server_port))
                end_time = time.time()
                send_time = end_time - start_time
                if send_time:
                    speed = buf_size / send_time
                else:
                    speed = 0
                speeds.append(speed)
                times.append(send_time)
                print("Затраченное на отправку время: ", send_time)
                print("Скорость: {0} Б/Сек".format(speed))
        print(speeds)
        print(times)
