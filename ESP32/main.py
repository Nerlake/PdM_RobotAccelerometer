from machine import Pin, I2C
from motor import MotorDriver
from MPU6050 import MPU6050
from time import sleep
from NetworkEsp import NetworkEsp

# Connection to remote server
net = NetworkEsp("LeoESP", "leo07112000", "172.20.10.5", 12345)
net.connect()

# Init motors and sensors
motors = MotorDriver(20, 22, 19, 18)
i2c = I2C(0, scl=Pin(7), sda=Pin(6), freq=100000)
mpu = MPU6050(bus=i2c)

# Start motors
motors.set_speed(100)
motors.forward()
print("Motors are running")

# Main loop
while True:
    accel = mpu.read_accel_data()
    gyro = mpu.read_gyro_data()
    magnitude = mpu.read_accel_abs(g=True)

    msg = "{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f}\n".format(
        accel["x"], accel["y"], accel["z"],
        gyro["x"], gyro["y"], gyro["z"],
        magnitude
    )
    net.send(msg)
    sleep(0.5)

