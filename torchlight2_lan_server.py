import os
import re
import time
import socket
import traceback
from datetime import datetime
import threading


intro_str = """
******************************************************************
*             Torchlight 2 Lan Game Server Tool V1.0             *
*                      Author: Jhj  2022.2                       *
*                                                                *
*     A message forwarding tool for Torchlight 2 lan game.       *
*     Only the game host needs to start this tool.               *
*                                                                *
* Usage:                                                         *
* 1. Set up a VLAN or make sure all clients have direct IPs.     *
* 2. Host a LAN game and start this tool. Enter all client IPs.  *
*    The tool will send room info to clients automatically.      *
* 3. After all clients are connected, you can choose to close    *
*    this tool.                                                  *
*                                                                *
* If you encounter any bug, please fill an issue on Github:      *
* https://github.com/jhj0411jhj/torchlight2_lan_game_server_tool *
*                                                                *
******************************************************************
"""

SRC_PORT = 4549
DST_PORT = 4549


def check_ip(ipAddr):
    compile_ip = re.compile('^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$')
    if compile_ip.match(ipAddr):
        return True
    else:
        return False


def get_time():
    return str(datetime.now())


def send_data(stop, sock, data, addr_list, send_times=25, send_interval=1.0):
    for i in range(send_times):
        if stop():
            print('Stop sending old data at %d/%d.' % (i, send_times))
            return
        for addr in addr_list:
            sock.sendto(data, addr)

        # check stop flag while sleeping
        for _ in range(int(send_interval)):
            if stop():
                print('Stop sending old data at %d/%d.' % (i + 1, send_times))
                return
            time.sleep(send_interval / int(send_interval))
    else:
        print('Stop sending old data at %d/%d.' % (send_times, send_times))


def main():
    # input client ip
    while True:
        ips = input('Please input client IPs, separated by space( ) or comma(,)\n'
                    '  (e.g. 1.2.3.4, 5.6.7.8)\n> ')
        client_ip_list = re.split('[, \t]', ips)
        client_ip_list = [ip for ip in client_ip_list if ip != '']
        print('\nclient_ip_list:', client_ip_list)

        # check ip
        valid = True
        for ip in client_ip_list:
            if not check_ip(ip):
                print('(%s) is not a valid ip!' % ip)
                valid = False
        if len(client_ip_list) == 0:
            valid = False
        print()
        if valid:
            break

    client_addr_list = [(ip, DST_PORT) for ip in client_ip_list]

    # setup socket
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udp.bind(('', SRC_PORT))

    # start forwarding
    print('=' * 5, get_time(), 'Start detecting room info\n')
    send_thread = None  # type: threading.Thread
    thread_stop_flag = False
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
            if send_thread:
                # stop thread that sends the old room info
                thread_stop_flag = True
                send_thread.join()
            thread_stop_flag = False
            send_times = 12
            send_interval = 2.0
            if send_times * send_interval >= 30:
                print('\n    Since the original room message is sent every 30 secs, \n'
                      '    (send_times * send_interval) should preferably be set below 30, \n'
                      '    otherwise the sending procedure will be early stopped.\n')

            send_thread = threading.Thread(
                target=send_data,
                args=((lambda: thread_stop_flag), udp, data, client_addr_list),
                kwargs=dict(send_times=send_times, send_interval=send_interval),
            )
            send_thread.setDaemon(True)
            send_thread.start()

            print('client_addr_list:', client_addr_list)
            print('[Forward message to clients (times=%d, interval=%.1fs)]\n' % (send_times, send_interval))
    # udp.close()


if __name__ == '__main__':
    try:
        print(intro_str)
        main()
    except Exception:
        print('===== Exception!!!')
        print(traceback.format_exc())
        os.system('pause')
