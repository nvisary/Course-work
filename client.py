import socket
import time

run_client = True
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

commands = {"STOP_CLIENT": 0,  "RUN_TEST1": 1}
img = open("img/cat.bmp", "rb")


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
            print("Ожидаю готовности от сервера.")
            print("Сервер готов.")
            print("Отправляю картинку.")
            start_time = time.time()
            BUF_SIZE = 4096
            parts = 0
            img.seek(0)
            img_size = 3.33 * 1000000
            count_parts = img_size / BUF_SIZE
            while True:
                part = img.read(BUF_SIZE)
                udp_socket.sendto(part, (server_ip, server_port))
                parts += 1
                print(str(parts) + "/" + str(count_parts))
                if len(part) < BUF_SIZE:
                    break

            end_time = time.time()
            send_time = end_time - start_time
            print("start time: ", start_time)
            print("end time: ", end_time)
            if send_time:
                speed = BUF_SIZE * parts/ send_time
            else:
                speed = 0
            speeds.append(speed)
            times.append(send_time)
            print("Затраченное на отправку время: ", send_time)
            print("Скорость: {0} Б/Сек".format(speed))
        print(speeds)
        print(times)
