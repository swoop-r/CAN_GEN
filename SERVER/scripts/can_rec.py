#receive simulated CAN traffic from Client
#transmit simulated CAN traffic over UDP to Kali
import socket

# set forward to True to enable forwarding to Kali
FORWARD = True
LISTEN_PORT = 5005
KALI_IP = "192.168.100.3"
KALI_PORT = 5005

print("Listening for CAN Frames on UDP port {LISTEN_PORT}...")


# setup receiving socket
recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recv_sock.bind(("0.0.0.0", LISTEN_PORT))

# setup sending socket
send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


# loop processing incoming packets
while True:
    packet, addr = recv_sock.recvfrom(128)
    print(f"From {addr[0]}:{addr[1]}  ->  {packet.hex()}")
    
    if FORWARD:
        print("Forwarder running...")
        try:
            send_sock.sendto(packet, (KALI_IP, KALI_PORT))
        except Exception as e:
            print("Forward error:", e)