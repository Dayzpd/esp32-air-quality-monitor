# boot.py -- run on boot-up
import binascii
import network
import time

import display_driver
#import pms7003 as pms
#import gas

WIFI_SSID = ""
WIFI_PASSWORD = ""


def connect_wifi(
    ssid: str,
    password: str,
):

    wlan = network.WLAN(network.STA_IF)

    wlan.active(True)

    wlan.scan()

    wlan.connect(ssid, password)

    while wlan.status() == network.STAT_CONNECTING:
        time.sleep(1)

    if not wlan.isconnected():

        reasons = {
            network.STAT_WRONG_PASSWORD: "incorrect password",
            network.STAT_NO_AP_FOUND: "AP not found",
            network.STAT_CONNECT_FAIL: "unknown reason",
        }

        reason = reasons.get(wlan.status())

        raise Exception(f"Failed to connect to ssid '{ssid}' due to {reason}.")

    mac_addr = binascii.hexlify(wlan.config('mac')).decode()

    formatted_mac = ":".join(mac_addr[i:i+2] for i in range(0, 12, 2))

    (ip, subnet_mask, gateway, dns_server) = wlan.ifconfig()


    print(f"Connected to ssid '{ssid}'")
    print(f"MAC: {formatted_mac}")
    print(f"IP: {ip}")

if __name__ == "__main__":
    connect_wifi(WIFI_SSID, WIFI_PASSWORD)
    display_driver.init()
    #pms.init()
    #gas.init()
