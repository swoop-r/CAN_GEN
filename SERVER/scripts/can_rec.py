#receive simulated CAN traffic from Client
#transmit simulated CAN traffic over UDP to Kali
import socket

FORWARD = False
LISTEN_PORT = 5005
KALI_IP = "192.168.100.3"
KALI_PORT = 5005

print("Listening for CAN Frames on UDP port {LISTEN_PORT}...")

recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recv_sock.bind(("0.0.0.0", LISTEN_PORT))


send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("Forwarder running...")

while True:
    packet, addr = recv_sock.recvfrom(128)
    print(f"From {addr[0]}:{addr[1]}  ->  {packet.hex()}")
    
    if FORWARD:
        try:
            send_sock.sendto(packet, (KALI_IP, KALI_PORT))
        except Exception as e:
            print("Forward error:", e)