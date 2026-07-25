import machine
import time
import rp2

# --- PART 1: THE BLUE BOARD DRIVER ---
class PCA9685:
    def __init__(self, i2c, address=0x40):
        self.i2c = i2c
        self.address = address
        self._write(0x00, 0x00)
    def _write(self, reg, value):
        self.i2c.writeto_mem(self.address, reg, bytearray([value]))
    def freq(self, freq):
        prescale = int(25000000.0 / 4096.0 / freq + 0.5) - 1
        self._write(0x00, 0x10)
        self._write(0xFE, prescale)
        self._write(0x00, 0xA1)
        time.sleep(0.005)
    def duty(self, index, value):
        self._write(0x08 + 4 * index, value & 0xFF)
        self._write(0x09 + 4 * index, value >> 8)

# --- PART 2: SETUP ---
sda = machine.Pin(0)
scl = machine.Pin(1)
i2c = machine.I2C(0, sda=sda, scl=scl)
servolar = PCA9685(i2c)
servolar.freq(50)

motor_ileri = machine.Pin(14, machine.Pin.OUT)
motor_geri = machine.Pin(15, machine.Pin.OUT)

def bootsel_button_pressed():
    return (rp2.bootsel_button() == 1)

# --- PART 3: METHODS ---

def servo_0_calistir(aci=90):
    duty = int((aci / 180) * 6000 + 1500)
    servolar.duty(0, duty)

def servo_1_calistir(aci=90):
    duty = int((aci / 180) * 6000 + 1500)
    servolar.duty(1, duty)

def servo_0_dur():
    servolar.duty(0, 0)

def servo_1_dur():
    servolar.duty(1, 0)

def tekerlek_ileri(sure):
    motor_ileri.value(1)
    motor_geri.value(0)
    time.sleep(sure)
    motor_ileri.value(0)
    motor_geri.value(0)

def tekerlek_geri(sure):
    motor_ileri.value(0)
    motor_geri.value(1)
    time.sleep(sure)
    motor_ileri.value(0)
    motor_geri.value(0)

def tekerlek_dur():
    motor_ileri.value(0)
    motor_geri.value(0)

# --- PART 4: RUN ---
print("Hazır! İstediğin methodu çağır.")
while True:
    if bootsel_button_pressed():
        
        # Buraya istediğin methodu yaz:
        # Örnekler:
        servo_0_calistir(180)
        servo_1_calistir(180)
        tekerlek_ileri(1)
        tekerlek_geri(0.5)
        pass

    time.sleep(0.1)