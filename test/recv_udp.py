import time
import socket

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
udp.bind(('', 4549))

print('start recv')
t = time.time()
while True:
    data, addr = udp.recvfrom(1024)
    print(time.time() - t, 's. len:', len(data))
    print(data, addr)
    # if len(data) > 30:
    #     break
