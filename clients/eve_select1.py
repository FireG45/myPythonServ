from client import Client, HOST, PORT

Client("eve", HOST, PORT).send_message("table1 select")