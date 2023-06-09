from client import Client, HOST, PORT

Client("alice", HOST, PORT).send_message("table1 select")