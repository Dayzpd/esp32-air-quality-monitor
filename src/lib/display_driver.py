
import lvgl as lv
import ft6x36
import lcd_bus
import micropython
from machine import SPI, Pin, SDCard
import st7796  # NOQA
import task_handler
import i2c
import vfs

import utils

#DISPLAY_CS = micropython.const(13)
#DISPLAY_RESET = micropython.const(27)
#DISPLAY_DC_RS = micropython.const(2)
#DISPLAY_MOSI = micropython.const(23)
#DISPLAY_SCK = micropython.const(18)
#DISPLAY_LED = micropython.const(15)
#DISPLAY_MISO = micropython.const(19)
#TOUCH_SCL = micropython.const(22)
#TOUCH_RESET = micropython.const(5)
#TOUCH_SDA = micropython.const(21)
#TOUCH_INTERRUPT = micropython.const(39)
#SD_SELECT_CONTROL = micropython.const()




"""
VCC (5V)
GND
LCD_CS   | Touch4 ADC14 GIOP13 | 10
LCD_RST  | Touch7 ADC17 GIOP27 | 4
LCD_RS   | Touch2 ADC12 GIOP2  | 9
SDI_MOSI | VSPI MOSI GIOP23    | 11
SCK      | VSPI SCK GIOP18     | 12
LED      | Touch3 ADC13 GIOP15 | 5
SDO_MISO | VSPI MISO GIOP19    | 13
CTP_SCL  | I2C SCL GIOP22      | 6
CTP_RST  | VSPI SS GIOP5       | 8
CTP_SDA  | I2C SDA GIOP21      | 7
CTP_INT  | ADC3 GIOP39         | unused
SD_CS    | ?                   | 39
"""

# some displays have a bezel that covers a small portion of the viewable area
# of the display. This is to offset the display data so it is not covered by
# the bezel. Keep in mind that you will have to adjust the width and height in
# order to compensate for the right and bottom edges of the display.
_OFFSET_X = micropython.const(0)
_OFFSET_Y = micropython.const(0)


display = None
touch = None
sd = None
spi_bus = None

WIDTH = micropython.const(320)
HEIGHT = micropython.const(480)

DISPLAY_FREQ = micropython.const(80000000)
DISPLAY_CS = micropython.const(10)
DISPLAY_RESET = micropython.const(4)
DISPLAY_DC_RS = micropython.const(9)
DISPLAY_MOSI = micropython.const(11)
DISPLAY_SCK = micropython.const(12)
DISPLAY_LED = micropython.const(5)
DISPLAY_MISO = micropython.const(13)

TOUCH_FREQ = micropython.const(100000)
TOUCH_SCL = micropython.const(6)
TOUCH_RESET = micropython.const(8)
TOUCH_SDA = micropython.const(7)
TOUCH_INTERRUPT = micropython.const(4) # Currently unused

SD_FREQ = micropython.const(20000000)
SD_SELECT_CONTROL = micropython.const(39)


def _init_spi_bus():

    spi_bus = None

    try:

        spi_bus = SPI.Bus(
            host=2,
            sck=DISPLAY_SCK,
            mosi=DISPLAY_MOSI,
            miso=DISPLAY_MISO
        )

        print("Initialized SPI Bus #2 for LCD Display!")

    except Exception as err:

        msg = "Failed to initialize SPI Bus #2 for LCD Display..."

        utils.log_error(msg, err)

    return spi_bus


def _mount_sdcard(**kw):
    global sd, spi_bus

    sd = None

    if "freq" not in kw:
        kw["freq"]=SD_FREQ

    try:

        sd = SDCard(
            spi_bus=spi_bus,
            cs=SD_SELECT_CONTROL,
            **kw
        )

        vfs.mount(sd, "/sd")

        print("Mounted sd card at /sd")

    except Exception as err:

        msg = "Failed to mount SD Card..."

        utils.log_error(msg, err)


def _init_display():
    global spi_bus

    display = None

    try:

        data_bus = lcd_bus.SPIBus(
            spi_bus=spi_bus,
            dc=DISPLAY_DC_RS,
            freq=DISPLAY_FREQ,
            cs=DISPLAY_CS,
        )

        display = st7796.ST7796(
            data_bus=data_bus,
            display_width=WIDTH,
            display_height=HEIGHT,
            reset_pin=DISPLAY_RESET,
            reset_state=st7796.STATE_LOW,
            backlight_pin=DISPLAY_LED,
            backlight_on_state=st7796.STATE_HIGH,
            color_space=lv.COLOR_FORMAT.RGB565,
            rgb565_byte_swap=True
        )

        display.set_rotation(135)

        display.init()

        display.set_backlight(100)

        print("Initialized LCD Display!")

    except Exception as err:

        msg = "Failed to initialize LCD Display..."

        utils.log_error(msg, err)

    return display


def _init_touch():

    touch = None

    try:

        i2c_bus = i2c.I2C.Bus(
            host=1,
            scl=TOUCH_SCL,
            sda=TOUCH_SDA,
            freq=TOUCH_FREQ,
            use_locks=False
        )
        touch_i2c = i2c.I2C.Device(
            i2c_bus,
            ft6x36.I2C_ADDR,
            ft6x36.BITS
        )
        touch = ft6x36.FT6x36(touch_i2c)

        print("Initialized Display Touch driver!")

    except Exception as err:

        msg = "Failed to initialize Touch driver..."

        utils.log_error(msg, err)

    return touch

th = None

@utils.stacktrace
def init():
    global display, sd, spi_bus, th, touch

    lv.init()

    spi_bus = _init_spi_bus()

    if not spi_bus:
        return

    display = _init_display()

    if not display:
        return

    th = task_handler.TaskHandler()

    touch = _init_touch()

    _mount_sdcard()
