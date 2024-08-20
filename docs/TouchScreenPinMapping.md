# MSP4031 TouchScreen Pin Mapping for ESP32-S3-DevKitC-1

[Hosyund](https://hosyond.com/)

[MSP4031/ST7796 LCD Wiki](http://www.lcdwiki.com/4.0inch_Capacitive_SPI_Module_ST7796#Product_Parameters)

## LCD Pin Overview

![MSP4031 TouchScreen Image](/docs/img/TouchScreen-MSP4031.png)

- **LCD_CS**: Chip Select, used to select the LCD.
- **LCD_RST**: Reset, used to reset the LCD.
- **LCD_RS**: Register Select (also known as Data/Command pin), used to switch between data and command mode.
- **SDI_MOSI**: Master Out Slave In, used to send data from the microcontroller to the LCD.
- **SCK**: Serial Clock, used to synchronize data transmission.
- **LED**: Controls the backlight of the LCD.
- **SDO_MISO**: Master In Slave Out, used to receive data from the LCD (if needed).
- **CTP_SCL**: Clock line for the capacitive touch panel.
- **CTP_RST**: Reset for the capacitive touch panel.
- **CTP_SDA**: Data line for the capacitive touch panel.
- **CTP_INT**: Interrupt pin for the capacitive touch panel.


## ESP32-S3 SPI Pin Overview

![ESP32-S3-DevKitC-1 Image](/docs/img/ESP32-S3_DevKitC-1_pinlayout_v1.1.jpg)

- **FSPICLK_in/_out_mux**: SPI Clock input/output multiplexer. This pin is used to select the clock source for the SPI bus.
- **FSPICS0_in/_out**: Chip Select 0 input/output. This pin is used to select the SPI device.
- **FSPICS1~5_out**: Chip Select 1 to 5 output. These pins are used to select additional SPI devices.
- **FSPID_in/_out**: SPI Data input/output. This pin is used for data transmission.
- **FSPIQ_in/_out**: SPI Q (Quad) data input/output. This pin is used for quad SPI data transmission.
- **FSPIWP_in/_out**: Write Protect input/output. This pin is used to control write protection.
- **FSPIHD_in/_out**: Hold input/output. This pin is used to pause data transmission.
- **FSPIIO4~7_in/_out**: SPI IO pins 4 to 7 input/output. These pins are used for additional data lines in octal SPI mode.
- **FSPIDQS_out**: Data Strobe output. This pin is used to synchronize data transmission.


## LCD to ESP32-S3 Pin Mappings

1. **LCD_CS (Chip Select)** --> **FSPICS0_in/_out**:
   - **Reasoning**: The Chip Select (CS) pin is used to select the LCD device on the SPI bus. The FSPICS0 pin on the ESP32 serves the same purpose.

2. **LCD_RST (Reset)** --> **Not directly mapped**:
   - **Reasoning**: The Reset (RST) pin is used to reset the LCD. This pin does not have a direct equivalent in the SPI pin set, so you can connect it to any available GPIO pin on the ESP32 and control it through software.

3. **LCD_RS (Register Select/Data Command)** --> **FSPIHD_in/_out**:
   - **Reasoning**: The Register Select (RS) pin, also known as Data/Command (DC), is used to switch between sending data and commands. The FSPIHD pin can be used for this purpose.

4. **SDI_MOSI (Master Out Slave In)** --> **FSPID_in/_out**:
   - **Reasoning**: The MOSI pin is used to send data from the microcontroller to the LCD. The FSPID pin on the ESP32 is used for data transmission.

5. **SCK (Serial Clock)** --> **FSPICLK_in/_out_mux**:
   - **Reasoning**: The Serial Clock (SCK) pin is used to synchronize data transmission. The FSPICLK pin on the ESP32 serves this purpose.

6. **LED (Backlight Control)** --> **Not directly mapped**:
   - **Reasoning**: The LED pin controls the backlight of the LCD. This pin does not have a direct equivalent in the SPI pin set, so you can connect it to any available GPIO pin on the ESP32 and control it through software.

7. **SDO_MISO (Master In Slave Out)** --> **FSPIQ_in/_out**:
   - **Reasoning**: The MISO pin is used to receive data from the LCD. The FSPIQ pin on the ESP32 is used for data reception.

Here's a summary of the pin mappings:

| LCD Pin | ESP32 Pin |
|---------|-----------|
| LCD_CS    | FSPICS0_in/_out     |
| LCD_RST   | Any GPIO            |
| LCD_RS    | FSPIHD_in/_out      |
| SDI_MOSI  | FSPID_in/_out       |
| SCK       | FSPICLK_in/_out_mux |
| LED       | Any GPIO            |
| SDO_MISO  | FSPIQ_in/_out       |
