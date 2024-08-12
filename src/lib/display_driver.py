
import lvgl as lv
import ft6x36
import lcd_bus
import micropython
from machine import SPI, Pin, SDCard
import st7796  # NOQA
import task_handler
import i2c


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
LCD_CS   | Touch4 ADC14 GIOP13 | 8
LCD_RST  | Touch7 ADC17 GIOP27 | 3/ 9
LCD_RS   | Touch2 ADC12 GIOP2  | 14
SDI_MOSI | VSPI MOSI GIOP23    | 13
SCK      | VSPI SCK GIOP18     | 12
LED      | Touch3 ADC13 GIOP15 | 11
SDO_MISO | VSPI MISO GIOP19    | 10
CTP_SCL  | I2C SCL GIOP22      | 7
CTP_RST  | VSPI SS GIOP5       | 6
CTP_SDA  | I2C SDA GIOP21      | 5
CTP_INT  | ADC3 GIOP39         | 4
SD_CS    | ?                   | 1
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

_WIDTH = micropython.const(320)
_HEIGHT = micropython.const(480)
#_BUFFER_SIZE = int((_WIDTH * _HEIGHT * 2) / 10)
_BUFFER_SIZE = _WIDTH * _HEIGHT * 3

_FREQ = micropython.const(80000000)
_TP_FREQ = micropython.const(100000)
_SD_FREQ = micropython.const(20000000)

DISPLAY_CS = micropython.const(10)
DISPLAY_RESET = micropython.const(4)
DISPLAY_DC_RS = micropython.const(9)
DISPLAY_MOSI = micropython.const(11)
DISPLAY_SCK = micropython.const(12)
DISPLAY_LED = micropython.const(5)
DISPLAY_MISO = micropython.const(13)
TOUCH_SCL = micropython.const(6)
TOUCH_RESET = micropython.const(8)
TOUCH_SDA = micropython.const(7)
TOUCH_INTERRUPT = micropython.const(4)
SD_SELECT_CONTROL = micropython.const(39)

print(5)


def sdcard(
    **kw
):

    if "freq" not in kw:
        kw["freq"]=_SD_FREQ

    return SDCard(
        spi_bus=spi_bus,
        cs=SD_SELECT_CONTROL,
        **kw
    )


def _init_display():
    global display, sd

    if display:
        return

    spi_bus = SPI.Bus(
        host=2,
        sck=DISPLAY_SCK,
        mosi=DISPLAY_MOSI,
        miso=DISPLAY_MISO
    )

    data_bus = lcd_bus.SPIBus(
        spi_bus=spi_bus,
        dc=DISPLAY_DC_RS,
        freq=_FREQ,
        cs=DISPLAY_CS,
    )

    #buf1 = bus.allocate_framebuffer(_BUFFER_SIZE, lcd_bus.MEMORY_SPIRAM)
    #buf2 = bus.allocate_framebuffer(_BUFFER_SIZE, lcd_bus.MEMORY_SPIRAM)

    display = st7796.ST7796(
        data_bus=data_bus,
        display_width=_WIDTH,
        display_height=_HEIGHT,
        #frame_buffer1=buf1,
        #frame_buffer2=buf2,
        reset_pin=DISPLAY_RESET,
        reset_state=st7796.STATE_LOW,
        backlight_pin=DISPLAY_LED,
        backlight_on_state=st7796.STATE_HIGH,
        #offset_x=_OFFSET_X,
        #offset_y=_OFFSET_Y,
        color_space=lv.COLOR_FORMAT.RGB565,
        rgb565_byte_swap=True
    )



    display.set_rotation(135)

    display.init()

    display.set_backlight(100)
    print("Initialized Display!")
    print("Initialized SD Card!")




def _init_touch():
    global touch

    if touch:
        return

    i2c_bus = i2c.I2C.Bus(
        host=1,
        scl=TOUCH_SCL,
        sda=TOUCH_SDA,
        freq=_TP_FREQ,
        use_locks=False
    )
    touch_i2c = i2c.I2C.Device(
        i2c_bus,
        ft6x36.I2C_ADDR,
        ft6x36.BITS
    )
    touch = ft6x36.FT6x36(touch_i2c)

    print("Initialized Touch!")

th = None
def init():
    global th
    lv.init()
    _init_display()
    th = task_handler.TaskHandler()

    _init_touch()
