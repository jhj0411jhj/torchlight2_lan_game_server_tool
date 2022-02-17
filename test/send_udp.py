import socket

# tell others you host a room
# caution: this is a NG game message, cannot be seen in game if receivers are NG+/NG++/...
data = (
    b"\xab\x84\x54\x72\x35\x00\x2b\x02\x00\x01\x00\x64\x00\x01\x00\x01"
    b"\x04\x00\x00\x00\x00\xd5\x5f\x7a\x4e\x01\x08\x39\xca\xe2\x10\x00"
    b"\x00\x00\x00\x00\x00\x00\x08\x74\x65\x73\x74\x72\x6f\x6f\x6d\x00"
    b"\x00\x00"
)

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
udp.bind(('', 4549))

ip = '1.2.3.4'
udp.sendto(data, (ip, 4549))
udp.close()
