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

# --- IMPROVED SERVO FUNCTIONS ---

def aci_to_duty(aci):
    """
    Converts angle (0-180) to a PCA9685 12-bit duty value.
    Typical servo pulse: 1ms (min) to 2ms (max) within a 20ms period (50Hz).
    At 50Hz: period = 20ms, 4096 steps → 1 step = ~4.88µs
    1ms  → ~204 steps  (0 degrees)
    1.5ms → ~307 steps (90 degrees)
    2ms  → ~409 steps  (180 degrees)
    """
    min_duty = 204   # ~1ms pulse
    max_duty = 409   # ~2ms pulse
    return int(min_duty + (aci / 180.0) * (max_duty - min_duty))

def servo_0_calistir(aci=90):
    """Moves servo on channel 0 to given angle (0-180)."""
    servolar.duty(0, aci_to_duty(aci))

def servo_1_calistir(aci=90):
    """Moves servo on channel 1 to given angle (0-180)."""
    servolar.duty(1, aci_to_duty(aci))

def servo_0_dur():
    """Stops sending signal to servo 0 (servo goes limp)."""
    servolar.duty(0, 0)

def servo_1_dur():
    """Stops sending signal to servo 1 (servo goes limp)."""
    servolar.duty(1, 0)

def servo_0_ortala():
    """Centers servo 0 to 90 degrees."""
    servo_0_calistir(90)

def servo_1_ortala():
    """Centers servo 1 to 90 degrees."""
    servo_1_calistir(90)

def servo_0_tarama(adim=10, bekleme=0.05):
    """
    Sweeps servo 0 from 0 → 180 → 0 degrees.
    adim  : step size in degrees (smaller = smoother)
    bekleme: delay between steps in seconds
    """
    for aci in range(0, 181, adim):
        servo_0_calistir(aci)
        time.sleep(bekleme)
    for aci in range(180, -1, -adim):
        servo_0_calistir(aci)
        time.sleep(bekleme)

def servo_1_tarama(adim=10, bekleme=0.05):
    """
    Sweeps servo 1 from 0 → 180 → 0 degrees.
    adim  : step size in degrees (smaller = smoother)
    bekleme: delay between steps in seconds
    """
    for aci in range(0, 181, adim):
        servo_1_calistir(aci)
        time.sleep(bekleme)
    for aci in range(180, -1, -adim):
        servo_1_calistir(aci)
        time.sleep(bekleme)

def her_ikisi_calistir(aci0=90, aci1=90):
    """Moves both servos at the same time to given angles."""
    servo_0_calistir(aci0)
    servo_1_calistir(aci1)

def her_ikisi_dur():
    """Stops signal to both servos."""
    servo_0_dur()
    servo_1_dur()

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
        her_ikisi_calistir(0, 180)    # Servo 0 → 0°, Servo 1 → 180°
        time.sleep(1)
        her_ikisi_calistir(180, 0)    # Opposite
        time.sleep(1)
        servo_0_tarama(adim=5)        # Smooth sweep on servo 0
        tekerlek_ileri(1)
        #tekerlek_ileri(1)
        #tekerlek_geri(0.5)
        pass

    time.sleep(0.1)