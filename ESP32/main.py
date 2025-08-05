from machine import Pin, I2C
from motor import MotorDriver
from MPU6050 import MPU6050
from time import sleep
from NetworkEsp import NetworkEsp

# Connect to remote server
net = NetworkEsp("LeoESP", "leo07112000", "172.20.10.5", 12345)
net.connect()

# Init motors and sensors
motors = MotorDriver(20, 22, 19, 18)
i2c = I2C(0, scl=Pin(7), sda=Pin(6), freq=100000)
mpu = MPU6050(bus=i2c)

# Function to read sensor data and format message
def read_sensor_data():
    accel = mpu.read_accel_data()
    gyro = mpu.read_gyro_data()
    magnitude = mpu.read_accel_abs(g=True)
    return "{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f}\n".format(
        accel["x"], accel["y"], accel["z"],
        gyro["x"], gyro["y"], gyro["z"],
        magnitude
    )

# Run motor cycle and send data
#motors.run_test_cycle(sensor_reader=read_sensor_data, data_sender=net.send, loop=False)
motors.run_constant_cycle(100, 120, read_sensor_data, net.send)
