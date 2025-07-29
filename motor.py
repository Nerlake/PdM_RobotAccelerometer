from machine import Pin, PWM


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

