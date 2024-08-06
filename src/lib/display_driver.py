
import lvgl as lv
from ft6x36 import ft6x36
from st7796 import st7796
import micropython

DISPLAY_LED = micropython.const(15)
DISPLAY_RESET = micropython.const(27)
DISPLAY_MOSI = micropython.const(23)
DISPLAY_CS = micropython.const(13)
DISPLAY_DC_RS = micropython.const(2)
DISPLAY_SCK = micropython.const(18)
DISPLAY_MISO = micropython.const(19)

TOUCH_SDA = micropython.const(21)
TOUCH_SCL = micropython.const(22)
TOUCH_RESET = micropython.const(5)
TOUCH_INTERRUPT = micropython.const(39)


display = None
touch = None


def _init_display():
    global display

    if display:
        return

    display = st7796(
        miso=DISPLAY_MISO,
        mosi=DISPLAY_MOSI,
        clk=DISPLAY_SCK,
        cs=DISPLAY_CS,
        dc=DISPLAY_DC_RS,
        rst=DISPLAY_RESET,
        backlight=DISPLAY_LED,
        power=-1,
        width=480,
        height=320,
        factor=24,
        double_buffer=True
    )
    print("Initialized Display!")


def _init_touch():
    global touch

    if touch:
        return

    touch = ft6x36(
        sda=TOUCH_SDA,
        scl=TOUCH_SCL,
        rst=TOUCH_RESET,
        itp=TOUCH_INTERRUPT,
        freq=400000,
        width=320,
        height=480,
        inv_x=True,
        swap_xy=True,
    )

    print("Initialized Touch!")

def init():
    _init_display()
    _init_touch()
