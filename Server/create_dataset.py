import socket
import os

host = "0.0.0.0"
port = 12345
csv_path = "data/normal_data.csv"

os.makedirs("data", exist_ok=True)

if not os.path.exists(csv_path):
    with open(csv_path, "w") as f:
        f.write("accel_x,accel_y,accel_z,gyro_x,gyro_y,gyro_z,gforce,mic\n")

server_socket = socket.socket()
server_socket.bind((host, port))
server_socket.listen(1)

conn, addr = server_socket.accept()

with open(csv_path, "a") as f:
    while True:
        data = conn.recv(1024)
        if not data:
            break
        line = data.decode().strip()

        if line:
            print("Reçu :", line)
            f.write(line + "\n")
            f.flush()

conn.close()
server_socket.close()
print("Connection has been closed")
