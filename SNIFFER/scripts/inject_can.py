#create the vcan interface:
#sudo modprobe vcan
#sudo ip link add dev vcan0 type vcan
#sudo ip link set vcan0 up

#may need run: pip install python-can cantools

import socket
import can

UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", UDP_PORT))

bus = can.interface.Bus(channel='vcan0', bustype='socketcan')


print("Listening... injecting to vcan0")

while True:
    pkt, _ = sock.recvfrom(64)

    can_id = int.from_bytes(pkt[:4], 'big')
    data = pkt[4:]

    msg = can.Message(
        arbitration_id=can_id,
        data=data,
        is_extended_id=True
    )

    bus.send(msg)
    print("Injected ->", msg)