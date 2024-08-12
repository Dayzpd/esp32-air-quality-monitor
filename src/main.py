import json
from machine import Timer
import micropython
import socket
import time

from pms7003 import Pms7003

SDA = micropython.const(21)
SCL = micropython.const(22)
UART = micropython.const(2)

CURRENT_READING = {}
pms = None
#pms = Pms7003(UART)

def update_current_reading(__):
    global CURRENT_READING
    
    
    pms.wakeup()

    time.sleep(10)

    pms.send_read_instruction()

    time.sleep(5)

    pms.read()

    time.sleep(5)

    pms.send_read_instruction()

    time.sleep(5)

    CURRENT_READING = pms.read()

    pms.sleep()


def web_server():
            
    # Set up socket for web server
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.setblocking(0)
    s.bind(addr)
    s.listen(1)

    print('listening on', addr)

    # Main loop for handling client requests
    while True:
        try:
            cl, addr = s.accept()
            print('client connected from', addr)
            request = cl.recv(1024)
            print(request)

            response = json.dumps(CURRENT_READING)
            cl.send('HTTP/1.0 200 OK\r\nContent-type: application/json\r\n\r\n')
            cl.send(response)
            cl.close()

        except:
            pass
        time.sleep(0.1)


if __name__ == "__main__":
    print("READY")
    #tim3 = Timer(3)
    #tim3.init(
    #    period=60000,
    #    mode=Timer.PERIODIC,
    #    callback=lambda __: micropython.schedule(update_current_reading, 0)
    #)
    #web_server()
    