"""
a simple version of torchlight2_lan_server.py
only for test
"""

import time
import socket
from datetime import datetime


def get_time():
    return str(datetime.now())


client_ip_list = [
    '1.2.3.4',
]
print('client_ip_list:', client_ip_list)

# setup socket
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
udp.bind(('', 4549))

# start forwarding
print('=' * 5, get_time(), 'Start detecting room info\n')
while True:
    # receive msg
    data, addr = udp.recvfrom(1024)
    print('=' * 5, get_time(), 'Receive message. len:', len(data))
    print(data, addr)
    if len(data) <= 30:  # todo: confirm len
        # not a room msg
        print('[Ignore message]\n')
    else:
        # forward room msg to clients
        for _ in range(5):
            for client_ip in client_ip_list:
                udp.sendto(data, (client_ip, 4549))
            time.sleep(0.2)
        print('client_ip_list:', client_ip_list)
        print('[Forward message to clients]\n')
# udp.close()
