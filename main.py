import os
import time
from machine import Pin, I2C
from motor import MotorDriver
from MPU6050 import MPU6050
from time import sleep

# Initialisation du moteur et du capteur
motors = MotorDriver(20, 22, 19, 18)
i2c = I2C(0, scl=Pin(7), sda=Pin(6), freq=100000)
mpu = MPU6050(bus=i2c)

# --- Création du dossier daté ---
base_name = time.localtime()  # (année, mois, jour, ...)
date_str = "{:04d}-{:02d}-{:02d}".format(base_name[0], base_name[1], base_name[2])
base_folder = date_str + "-jeudedonnées"
folder = base_folder
i = 1
while folder in os.listdir():
    folder = "{}_{}".format(base_folder, i)
    i += 1

os.mkdir(folder)

# --- Création du fichier avec en-tête ---
file_path = "{}/donnees.txt".format(folder)
with open(file_path, "w") as f:
    f.write("AccélérationX\tAccélérationY\tAccélérationZ\tGyroX\tGyroY\tGyroZ\tTempérature\tGForce\n")

# --- Lancement des moteurs ---
print("Test moteur avant...")
motors.set_speed(100)
motors.forward()
print("Moteurs en marche")

# --- Boucle de mesure et enregistrement ---
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

    with open(file_path, "a") as f:
        f.write("{:.2f}\t{:.2f}\t{:.2f}\t{:.2f}\t{:.2f}\t{:.2f}\t{:.2f}\t{:.2f}\n".format(
            accel["x"], accel["y"], accel["z"],
            gyro["x"], gyro["y"], gyro["z"],
            temp, magnitude
        ))

    sleep(0.5)
