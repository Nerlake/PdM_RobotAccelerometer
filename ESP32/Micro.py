from machine import ADC, Pin

class Microphone:
    def __init__(self, pin_num, attenuation=ADC.ATTN_11DB, width=ADC.WIDTH_12BIT):
        self.adc = ADC(Pin(pin_num))
        self.adc.atten(attenuation)
        try:
            self.adc.width(width)
        except:
            pass

    def read_data(self):
        if hasattr(self.adc, "read_u16"):
            return self.adc.read_u16() >> 4
        return self.adc.read()



