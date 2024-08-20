import collections
import math
import time
from machine import SoftI2C, Pin


GasMeasurement = collections.namedtuple(
    "GasMeasurement",
    ("name", "adc", "v", "rs", "ppm")
)

class GroveMultichannelGasSensor:
    WARMING_UP = 0xFE  # Define according to your sensor's datasheet
    WARMING_DOWN = 0xFF  # Define according to your sensor's datasheet
    GM_102B = 0x01  # Define according to your sensor's datasheet
    GM_302B = 0x03  # Define according to your sensor's datasheet
    GM_502B = 0x05  # Define according to your sensor's datasheet
    GM_702B = 0x07  # Define according to your sensor's datasheet
    CHANGE_I2C_ADDR = 0x55  # Define according to your sensor's datasheet

    NO2_R0 = 1.07
    C2H5OH_R0 = 1.0
    VOC_R0 = 1.0
    CO_R0 = 3.21

    def __init__(self, i2c, address=0x08):
        self.i2c = i2c
        self.address = address
        self.is_preheated = False
        self.preheated()

    def _write_byte(self, cmd):
        self.i2c.writeto(self.address, bytes([cmd]))
        time.sleep(0.01)  # Delay for stability

    def _read_32bit(self):
        data = self.i2c.readfrom(self.address, 4)
        value = int.from_bytes(data, 'little')
        time.sleep(0.01)  # Delay for stability
        return value

    def preheated(self):
        self._write_byte(self.WARMING_UP)
        self.is_preheated = True

    def unpreheated(self):
        self._write_byte(self.WARMING_DOWN)
        self.is_preheated = False

    def get_gm102b(self):
        if not self.is_preheated:
            self.preheated()
        self._write_byte(self.GM_102B)
        return self._read_32bit()

    def get_gm302b(self):
        if not self.is_preheated:
            self.preheated()
        self._write_byte(self.GM_302B)
        return self._read_32bit()

    def get_gm502b(self):
        if not self.is_preheated:
            self.preheated()
        self._write_byte(self.GM_502B)
        return self._read_32bit()

    def get_gm702b(self):
        if not self.is_preheated:
            self.preheated()
        self._write_byte(self.GM_702B)
        return self._read_32bit()

    def change_address(self, new_address):
        if new_address == 0 or new_address > 127:
            new_address = 0x08
        self.i2c.writeto(self.address, bytes([self.CHANGE_I2C_ADDR, new_address]))
        self.address = new_address

    @staticmethod
    def calc_voltage(adc):
        return ( adc / 1024 ) * 3.3

    @staticmethod
    def calc_resistance(volt):
        return ( 3.3 - volt ) / volt

    def measure_no2(self) -> GasMeasurement:
        for _ in range(100):
            adc = self.get_gm102b()
        volt = GroveMultichannelGasSensor.calc_voltage(adc)
        rs_gas = GroveMultichannelGasSensor.calc_resistance(volt)
        ratio = rs_gas / GroveMultichannelGasSensor.NO2_R0
        lgPPM = (math.log10(ratio) * 1.9) - 0.2
        ppm = math.pow(10, lgPPM)

        return GasMeasurement(name="NO2", adc=adc, v=volt, rs=rs_gas, ppm=ppm)

    def measure_c2h5oh(self) -> GasMeasurement:
        for _ in range(100):
            adc = self.get_gm302b()
        volt = GroveMultichannelGasSensor.calc_voltage(adc)
        rs_gas = GroveMultichannelGasSensor.calc_resistance(volt)
        ratio = rs_gas / GroveMultichannelGasSensor.C2H5OH_R0
        lgPPM = (math.log10(ratio) * 1.9) - 0.2
        ppm = math.pow(10, lgPPM)

        return GasMeasurement(name="C2H5OH", adc=adc, v=volt, rs=rs_gas, ppm=ppm)

    def measure_voc(self) -> GasMeasurement:
        for _ in range(100):
            adc = self.get_gm502b()
        volt = GroveMultichannelGasSensor.calc_voltage(adc)
        rs_gas = GroveMultichannelGasSensor.calc_resistance(volt)
        ratio = rs_gas / GroveMultichannelGasSensor.VOC_R0
        lgPPM = (math.log10(ratio) * 1.9) - 0.2
        ppm = math.pow(10, lgPPM)

        return GasMeasurement(name="VOC", adc=adc, v=volt, rs=rs_gas, ppm=ppm)

    def measure_co(self) -> GasMeasurement:
        for _ in range(100):
            adc = self.get_gm702b()
        volt = GroveMultichannelGasSensor.calc_voltage(adc)
        rs_gas = GroveMultichannelGasSensor.calc_resistance(volt)
        ratio = rs_gas / GroveMultichannelGasSensor.CO_R0
        lgPPM = (math.log10(ratio) * ( -2.82 )) - 0.12
        ppm = math.pow(10, lgPPM)

        return GasMeasurement(name="CO", adc=adc, v=volt, rs=rs_gas, ppm=ppm)

    def debug(self):

        def _debug(func):
            gas = func()
            print(f"{gas.name}: {gas.adc} ADC, {gas.v} V, {gas.rs} Ohm, {gas.ppm} PPM")

        _debug(self.measure_no2)
        _debug(self.measure_c2h5oh)
        _debug(self.measure_voc)
        _debug(self.measure_co)

SDA = Pin(47)
SCL = Pin(48)

sensor = None

def _init_gas():
    global sensor

    i2c = SoftI2C(sda=SDA, scl=SCL)
    addrs = i2c.scan()
    assert len(addrs), "No I2C device found for Multichannel Gas Sensor!"

    print(f"Found Multichannel Gas Sensor on I2C address: {addrs[0]}")

    sensor = GroveMultichannelGasSensor(i2c)

    print("Initialized Multichannel Gas Sensor!")

def init():
    _init_gas()
