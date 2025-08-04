# server_pc.py
import socket

host = "0.0.0.0"
port = 12345

server_socket = socket.socket()
server_socket.bind((host, port))
server_socket.listen(1)
print("Waiting for connection...")

conn, addr = server_socket.accept()
print(f"Connected to {addr}")

while True:
    data = conn.recv(1024)
    if not data:
        break
    print("Received :", data.decode().strip())

conn.close()
