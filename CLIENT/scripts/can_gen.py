#script to generate a J1939-Compliant CAN Frame
#and then forward the frame across the network
#to the host, defined in the SERVER_IP and SERVER_PORT

import cantools
import socket
import time
import random

db = cantools.database.load_file("j1939.dbc", encoding='utf-8', strict=False)



#config for local Server
SERVER_IP = "192.168.100.1"
SERVER_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


# example PGN 61444
msg = db.get_message_by_name("EEC1")

while True:
    rpm = random.uniform(400, 2850)
    torque = random.randint(0, 100)
    
    data = msg.encode({
        "EngineSpeed": rpm,
        "ActualEnginePercentTorque": torque
    })


    # 29-bit J1939 ID

    frame = msg.frame_id.to_bytes(4, 'big') + data

    sock.sendto(frame, (SERVER_IP, SERVER_PORT))
    print("Sent frame:" , rpm, torque)


    time.sleep(0.1)