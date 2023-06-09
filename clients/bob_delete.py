from client import Client, HOST, PORT

Client("bob", HOST, PORT).send_message("table1 delete 0")