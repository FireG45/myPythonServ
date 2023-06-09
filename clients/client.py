import socket

HOST = '127.0.0.1'
PORT = 2048

class Client:
    def __init__(self, login, host, port) -> None:
        self.login = login
        self.host = host
        self.port = port
    
    def send_message(self, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # создаем объект сокета
            try:
                s.connect((self.host, self.port)) # подключаемся к адресу сервера
                s.sendall(f"{self.login} {message}".encode("utf-8")) # отправляем запрос 
                data = s.recv(1024).decode("utf-8") # получаем данные и разшифровываепм в строку
                if data[0] == '-':
                    print("Нет доступа!")
                else:    
                    print(*data[1:-1][1:-1].split('), ('), sep='\n') # выводим полученное сообщение
            except ConnectionRefusedError:
                print("Сервер недоступен!")
