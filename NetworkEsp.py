import socket
import network
from time import sleep


class NetworkEsp:
    def __init__(self, ssid, password, server_ip, server_port):
        self.ssid = ssid
        self.password = password
        self.server_ip = server_ip
        self.server_port = server_port
        self.sock = None

    def connect(self):
        wlan = network.WLAN(network.STA_IF)
        if wlan.active():
            wlan.active(False)
        wlan.active(True)
        nets = wlan.scan()
        for net in nets:
            print("-", net[0].decode())
        wlan.connect(self.ssid, self.password)

        print(f"Connecting to Wi-Fi {self.ssid}...")

        max_attempts = 20
        for i in range(max_attempts):
            status = wlan.status()
            print(f"  Attempt {i + 1}/{max_attempts} → status : {status}")
            if status == network.STAT_GOT_IP:
                break
            sleep(1)
        else:
            print("Failed to connect to Wi-Fi.")
            return

        print("Connected with IP :", wlan.ifconfig()[0])

        print("Connecting to server...")
        self.sock = socket.socket()
        self.sock.connect((self.server_ip, self.server_port))
        print("Connected to server.")

    def send(self, data):
        if self.sock:
            try:
                self.sock.send(data.encode())
            except Exception as e:
                print("Sending error :", e)

    def close(self):
        if self.sock:
            self.sock.close()
            print("Closed socket.")

