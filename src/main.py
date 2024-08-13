import json
from machine import Timer
import micropython
import socket
import time

from pms7003 import Pms7003



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
