import os
from machine import Pin, I2C
from motor import MotorDriver
from MPU6050 import MPU6050
from time import sleep


motors = MotorDriver(20, 22, 19, 18)
i2c = I2C(0, scl=Pin(7), sda=Pin(6), freq=100000)
mpu = MPU6050(bus=i2c)


print("Test moteur avant...")
motors.set_speed(100)
motors.forward()
print("Moteurs en marche")
while True:
    accel = mpu.read_accel_data(g=False)
    gyro = mpu.read_gyro_data()
    temp = mpu.read_temperature()
    magnitude = mpu.read_accel_abs(g=True)

    print("Accélération (m/s²) → X:{:.2f}, Y:{:.2f}, Z:{:.2f}".format(accel["x"], accel["y"], accel["z"]))
    print("Gyroscope (°/s)     → X:{:.2f}, Y:{:.2f}, Z:{:.2f}".format(gyro["x"], gyro["y"], gyro["z"]))
    print("Température         → {:.2f} °C".format(temp))
    print("G-Force absolue     → {:.2f} g".format(magnitude))
    print("-" * 50)
    sleep(0.5)
