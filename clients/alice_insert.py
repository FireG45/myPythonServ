from client import Client, HOST, PORT

Client("alice", HOST, PORT).send_message("table1 insert 0 'alice1' 42")