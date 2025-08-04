import socket
from anomalies_detection import AnomaliesDetection

host = "0.0.0.0"
port = 12345

# Load and train the anomaly detection model
print("Loading training dataset...")
model = AnomaliesDetection()
model.train("data/normal_data.csv")

# Initialize server socket
server_socket = socket.socket()
server_socket.bind((host, port))
server_socket.listen(1)
print("Waiting for connection on port", port, "...")

# Accept client connection (ESP32)
conn, addr = server_socket.accept()
print(f"Client connected from {addr}")



# Expected feature names in the incoming data
feature_names = ["accel_x", "accel_y", "accel_z", "gyro_x", "gyro_y", "gyro_z", "gforce"]

# Handle incoming data and detect anomalies
while True:
    data = conn.recv(1024)
    if not data:
        break

    line = data.decode().strip()

    try:
        values = list(map(float, line.split(",")))
        if len(values) != len(feature_names):
            print(f"Ignored line: invalid number of values ({len(values)})")
            continue

        row = dict(zip(feature_names, values))
        is_anomaly = model.predict(row)

        if is_anomaly:
            print("Anomaly detected:", row)
        else:
            print("No anomaly detected:")

    except Exception as e:
        print("Error during parsing or prediction:", e)
        continue

# Close connections
conn.close()
server_socket.close()
print("Connection closed.")
