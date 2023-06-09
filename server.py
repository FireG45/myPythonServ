import socket
import sqlite3
import time

# HDRS = 'HTTPS/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
# HDRS_404 = 'HTTPS/1.1 200 404\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'

HOST = '127.0.0.1'
PORT = 2048

DAC, MAC, RBAC = 'alowed', 'levels', 'roles'

class Server:
    def __init__(self, host, port, politics = DAC) -> None:
         self.host = host
         self.port = port
         self.politics = politics
    
    def add_to_allowed(table, login): # метод для добавления пользователя в список разрешенных
        auth_con = sqlite3.connect("auth.db")
        cur = auth_con.cursor()
        cur.execute(f"INSERT INTO {table}_alowed VALUES ('{login}')")
        auth_con.commit()
        auth_con.close()
        
    def set_level(table, login, level): # метод для назначения пользователю уровнея доступа
        auth_con = sqlite3.connect("auth.db")
        cur = auth_con.cursor()
        if (lenm := len(cur.execute(f"SELECT * FROM {table}_levels WHERE login = '{login}'").fetchall())) == 0:
            cur.execute(f"INSERT INTO {table}_levels VALUES ('{login}', '{level}')")
        else:
            cur.execute(f"UPDATE {table}_levels SET level = '{level}' WHERE login = '{login}'")
        auth_con.commit()
        auth_con.close()
    
    def set_role(table, login, role): # метод для назначения пользователю роли
        auth_con = sqlite3.connect("auth.db")
        cur = auth_con.cursor()
        if len(cur.execute(f"SELECT * FROM {table}_roles WHERE login = '{login}'").fetchall()) == 0:
            cur.execute(f"INSERT INTO {table}_roles VALUES ('{login}', '{role}')")
        else:
            cur.execute(f"UPDATE {table}_roles SET role = '{role}' WHERE login = '{login}'")
        auth_con.commit()
        auth_con.close()
    
    def remove_from(login, table): # удаление пользователя из списка разрешенных
        auth_con = sqlite3.connect("auth.db")
        cur = auth_con.cursor()
        cur.execute(f"DELETE FROM {table} WHERE login = '{login}'")
        auth_con.commit()
        auth_con.close()
    
    def clear(table): # очистка таблица
        auth_con = sqlite3.connect("auth.db")
        cur = auth_con.cursor()
        cur.execute(f"DELETE FROM {table}")
        auth_con.commit()
        auth_con.close()
        
    def check_permission(self, login, table): # проверка пользователя на наличие у него доступа
        permission = False
        auth_con = sqlite3.connect("auth.db")
        cur = auth_con.cursor()
        res = cur.execute(f"SELECT * FROM {table}_{self.politics} WHERE login = \'{login}\'")
        res_data = res.fetchone()
        permission = not res_data is None
        if not res_data is None and self.politics == MAC:
            permission = res_data[1] >= 4
        if not res_data is None and self.politics == RBAC:
            permission = res_data[1] == 'user'
        auth_con.close()
        return permission
    
    def start_server(self): # старт сервера
        bd_con = sqlite3.connect("data.db") # подключение к бд
        cur = bd_con.cursor()
        server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) # создание объекта сервера
        server.bind((self.host, self.port)) # присовение ему IP и порта
        server.listen() # слушаем сообщения
        print(f"Сервер запущен!")
        while True:
            try:
                client, adress = server.accept() # получаем сообщение
                request = client.recv(1024).decode("utf-8") # декодируем его в строку
                splitted_request = request.split(' ') # разбиваем по пробелу
                permission = self.check_permission(splitted_request[0], splitted_request[1]) # проверяем разрешения
                if permission: 
                    match splitted_request[2]: # в зависимсоти от запроса и наличия разрешения выполняем его
                        case 'select':
                            res = cur.execute(f"SELECT * FROM {splitted_request[1]}")
                            res_data = res.fetchall()
                            client.send(repr(res_data).encode("utf-8"))
                        case 'insert':
                            query = f"INSERT INTO {splitted_request[1]} VALUES ({splitted_request[3]}, {splitted_request[4]}, {splitted_request[5]})"
                            res = cur.execute(query)
                            res_data = res.fetchall()
                            client.send(repr(res_data).encode("utf-8"))
                        case 'delete':
                            query = f"DELETE FROM {splitted_request[1]} WHERE id = {splitted_request[3]}"
                            res = cur.execute(query)
                            res_data = res.fetchall()
                            client.send(repr(res_data).encode("utf-8"))
                    bd_con.commit()
                else:
                    client.send("-".encode("utf-8"))
                with open("audit.log", '+a') as log: # пишем в аудит запроси его результат 
                    status = "Разрешено" if permission else "Отказано"
                    log.write(f"{time.asctime()}| Запрос: [{request}]| Статус: {status}\n")
                client.shutdown(socket.SHUT_WR) 
            except KeyboardInterrupt:
                print("Выключение...")
                break

    # def load_view(request):
    #     try:
    #         path = request.split(' ')[1]
    #         response = ''
    #         with open('views' + path, 'rb') as file:
    #             response = file.read()
    #     except FileNotFoundError:
    #         return (HDRS_404 + "<h1>Error 404 page not found<h1>").encode('utf-8')
    #     return HDRS.encode("utf-8") + response

if __name__ == "__main__":
    Server(HOST, PORT, RBAC).start_server()