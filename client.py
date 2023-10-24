import socket
import sys
from _thread import start_new_thread

VERSION = "1.0"

# Set up socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
if len(sys.argv) == 2 and sys.argv[1].lower() == "help":
	print ("Usage: \npython3 client.py <IP Address> <Port>")
	exit()

# Connect to server
IP_ADDRESS = str(sys.argv[1]) if len(sys.argv) > 1 else input("IP Address: ")
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else int(input("Port: "))
server.connect((IP_ADDRESS, PORT))

def send_id(username: str, password: str) -> None:
    '''Sends and verifies version information, along with giving the information for a log in attempt.'''
    server.send(bytes(VERSION, encoding="utf-8"))
    if((version := server.recv(8).decode()) != VERSION):
        print(f"You have the wrong version! You have v{VERSION}. Server is on v{version}.")
        exit()
    
    server.send(bytes(username, encoding="utf-8"))
    server.send(bytes(password, encoding="utf-8"))

def listen_stdin() -> None:
    '''Continually listens to stdin and sends messages to the server'''
    while True:
        message = sys.stdin.readline().strip()
        server.send(bytes(message, encoding="utf-8"))

def listen_server() -> None:
    '''Continually listens for messages from the server and sends them to stdout if good.'''
    while True:
        message = server.recv(2048)
        if (message): print(str(message, "UTF-8"))
        else: exit()

send_id(input("Username: "), input("Password: "))
start_new_thread(listen_server, ())
listen_stdin()
server.close() 
