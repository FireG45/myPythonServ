from server import Server
import sys

if __name__ == "__main__":
    match sys.argv[1]:
        case '-add':
            Server.add_to_allowed(sys.argv[2], sys.argv[3])
        case '-setP':
            Server.set_level(sys.argv[2], sys.argv[3], sys.argv[4])
        case '-setR':
            Server.set_role(sys.argv[2], sys.argv[3], sys.argv[4])
        case '-rm':
            Server.remove_from(sys.argv[3], f"{sys.argv[2]}_alowed")
        case '-rmP':
            Server.remove_from(sys.argv[3], f"{sys.argv[2]}_levels")
        case '-rmR':
            Server.remove_from(sys.argv[3], f"{sys.argv[2]}_roles")
        case '-cl':
            Server.clear(f"{sys.argv[2]}_alowed")
        case '-clP':
            Server.clear(f"{sys.argv[2]}_levels")
        case '-clR':
            Server.clear(f"{sys.argv[2]}_roles")
        case '-help':
            print("""
-add {table} {login} добавить пользователя в список пользователей с доступом к бд (DAC)
-setP {table} {login} {level} присвоить уровень доступа пользователю 
-setR {table} {login} {role} присвоить роль пользователю

-rem {table} {login} удалить пользователя из списка пользователей с доступом к бд
-remP {table} {login} удалить уровень доступа пользователя
-remR {table} {login} удалить уровень роль пользователя

-cl {table} очистить список пользователей с доступом к бд
-clP {table} очистить список уровней доступа
-clR {table} очистить список ролей
""")
        case _:
            print("Неверный флаг. Используйте -help для получения информации о флагах")