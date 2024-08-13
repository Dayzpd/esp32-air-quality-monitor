import dht
import machine
import micropython
import time

import utils

sensor = None

DATA_PIN = micropython.const(1)

def init():
    global sensor

    try:
        sensor = dht.DHT22(machine.Pin(DATA_PIN))

        print("Successfully initialized DHT22 sensor!")

    except Exception as err:

        msg = "Failed to initialize DHT22 sensor..."

        utils.log_error(msg, err)

CURRENT_READING = {}

def read(__=None):
    global CURRENT_READING, sensor

    sensor.measure()

    time.sleep(2)

    temp_c = sensor.temperature()
    humidity = sensor.humidity()

    temp_f = temp_c * 9/5 + 32

    CURRENT_READING = dict(
        temp_c=temp_c,
        temp_f=temp_f,
        rel_humidity=humidity
    )

    for k,v in CURRENT_READING.items():
        print(f"{k}: {v}")

# import dht22; dht22.init(); dht22.read();
