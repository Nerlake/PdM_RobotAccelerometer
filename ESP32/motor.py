from machine import Pin, PWM
from time import sleep


class MotorDriver:
    def __init__(self, in1, in2, in3, in4, freq=20000):
        self.m1a = PWM(Pin(in1), freq=freq)
        self.m1b = PWM(Pin(in2), freq=freq)
        self.m2a = PWM(Pin(in3), freq=freq)
        self.m2b = PWM(Pin(in4), freq=freq)
        self._speed = 100  # default speed percent
        self.stop()

    def set_speed(self, percent):
        # percent: 0-100
        self._speed = max(0, min(percent, 100))

    def motor1(self, speed):
        # speed: -100 (full back) ... 0 (stop) ... 100 (full forward)
        if speed > 0:
            self.m1a.duty_u16(int(speed / 100 * 65535))
            self.m1b.duty_u16(0)
        elif speed < 0:
            self.m1a.duty_u16(0)
            self.m1b.duty_u16(int(-speed / 100 * 65535))
        else:
            self.m1a.duty_u16(0)
            self.m1b.duty_u16(0)

    def motor2(self, speed):
        if speed > 0:
            self.m2a.duty_u16(int(speed / 100 * 65535))
            self.m2b.duty_u16(0)
        elif speed < 0:
            self.m2a.duty_u16(0)
            self.m2b.duty_u16(int(-speed / 100 * 65535))
        else:
            self.m2a.duty_u16(0)
            self.m2b.duty_u16(0)

    def forward(self):
        self.motor1(self._speed)
        self.motor2(self._speed)

    def backward(self):
        self.motor1(-self._speed)
        self.motor2(-self._speed)

    def left(self):
        self.motor1(-self._speed)
        self.motor2(self._speed)

    def right(self):
        self.motor1(self._speed)
        self.motor2(-self._speed)

    def stop(self):
        self.motor1(0)
        self.motor2(0)

    def run_test_cycle(self, sensor_reader=None, data_sender=None, loop=False):
        print("Running motor test cycle...")

        phases = [
            {"speed": 70, "duration": 20, "label": "70% speed"},
            {"speed": 0, "duration": 5, "label": "Stopped"},
            {"speed": 80, "duration": 20, "label": "80% speed"},
            {"speed": 0, "duration": 5, "label": "Stopped"},
            {"speed": 90, "duration": 20, "label": "90% speed"},
            {"speed": 0, "duration": 5, "label": "Stopped"},
            {"speed": 100, "duration": 20, "label": "100% speed"},
            {"speed": 0, "duration": 5, "label": "Stopped"}
        ]

        while True:
            for phase in phases:
                self.set_speed(phase["speed"])
                if phase["speed"] == 0:
                    self.stop()
                else:
                    self.forward()

                print(f"Phase: {phase['label']} ({phase['duration']}s)")

                if sensor_reader and data_sender:
                    for _ in range(int(phase["duration"] / 0.5)):
                        msg = sensor_reader()
                        data_sender(msg)
                        sleep(0.5)
                else:
                    sleep(phase["duration"])

            print("Motor test cycle completed.")

            if not loop:
                break

        self.stop()
        print("Motor stopped.")

    def run_constant_cycle(self, speed=80, duration=60, sensor_reader=None, data_sender=None):
        print(f"Running constant cycle at {speed}% speed for {duration} seconds")

        self.set_speed(speed)
        self.forward()

        steps = int(duration / 0.5)

        for _ in range(steps):
            if sensor_reader and data_sender:
                msg = sensor_reader()
                data_sender(msg)
            sleep(0.5)

        self.stop()
        print("Constant cycle finished. Motor stopped.")



