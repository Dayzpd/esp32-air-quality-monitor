# LVGL Micropython

## Overview

The LVGL project has their own Micropython fork that includes LVGL; however, they only support up to Micropython v1.20. I only ran into issues building the firmware for the ESP32-S3-DevKitC-1-N8R8 module. Consequently, I did some research and stumbled upon an alternative project led by Kevin Schlosser ([lvgl_micropython](https://github.com/lvgl-micropython/lvgl_micropython)) for building the latest version of Micropython with LVGL included.

The interesting aspect of the project is that he's automated process of building and flashing the firmware file to where you only need to run a python script and then flash the firmware. Additionally, it also includes the option to bake in specific drivers for your particular display and touch drivers.

## Steps

1. Clone the lvl_micropython repo:

    ```bash
    $ git clone git@github.com:lvgl-micropython/lvgl_micropython.git
    ```

2. Build the firmware:

    Since I am using the `ESP32-32-DevKitC-1-N8R8`, I specify the `ESP32_GENERIC_S3` board with variant `SPIRAM_OCT` since it has 8mb of Octal SPIRAM. The flash storage size is `8mb` although this will vary if you have a different model of the ESP32-S3-DevKitC-1. For the DISPLAY and INDEV, I specify `st7796` and `ft6x36` since the Hosyund 4" MSP-4031 TouchScreen uses the `st7796s` display driver and `FT6336u` touch driver (see [LCD Wiki MSP-4031](http://www.lcdwiki.com/4.0inch_Capacitive_SPI_Module_ST7796#Product_Parameters)).

    ```bash
    $ cd lvgl_micropython
    $ python3 make.py esp32 submodules clean mpy_cross BOARD=ESP32_GENERIC_S3 BOARD_VARIANT=SPIRAM_OCT --flash-size=8 DISPLAY=st7796 INDEV=ft6x36
    ```

    *Note: Your mileage will vary if you use a different microcontroller and touchscreen.*

3. Flash the firmware:

    ```bash
    $ ~/.espressif/python_env/idf5.2_py3.10_env/bin/python -m esptool --chip esp32s3 -p /dev/ttyUSB1 -b 460800 --before default_reset --after hard_reset write_flash --flash_mode dio --flash_size 8MB --flash_freq 80m --erase-all 0x0 ~/workspaces/lvgl_micropython/build/lvgl_micropy_ESP32_GENERIC_S3-SPIRAM_OCT-8.bin
    ```

    *Note: After the build, it will print to stdout the command you need to run for flashing to the board. You just need to specify the proper serial port which in my case was /dev/ttyUSB1.*
