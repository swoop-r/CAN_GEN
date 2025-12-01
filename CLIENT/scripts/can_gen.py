# script to generate a J1939-Compliant CAN Frame
# and then forward the frame across the network
# to the host, defined in the SERVER_IP and SERVER_PORT

import cantools
import os
import socket
import time
import random

# load the DBC file with path relative to this script
# assumes the DBC file is in the same directory
DBC_PATH = os.path.join(os.path.dirname(__file__), "j1939.dbc")
db = cantools.database.load_file(DBC_PATH)



# config for local Server
SERVER_IP = "192.168.10.194"
SERVER_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


# Dated J1939 source from Tom Hawkins suggests GPM13 for Parameter Group Number (PGN)
# for engine controls. more information available: https://www.csselectronics.com/pages/j1939-explained-simple-intro-tutorial#j1939-pgn-spn 
msg = db.get_message_by_name("GPM13")

# baseline values on init
rpm = 800.0
torque = 0.0
speed = 0

# simple function to change values
# more uniformly, less pure random
# uses random.uniform()
def changeValues(value, min, max, step):
    value += random.uniform(-step, step)

    #maintain the expected bounds
    if value < min:
        value = min
    if value > max:
        value = max
    
    return value

while True:
    # modulate rpm from idle to 2850
    rpm = changeValues(rpm, 400, 2850, 50)
    
    # change torque with realistic small steps
    torque = changeValues(torque, -50, 100, 3)
    
    speed = changeValues(speed, 0, 120, 1)

    # encoding the data according to the DBC
    # if the names do not match, it will error out
    # check DBC file to ensure correct signal names
    data = msg.encode({
        "EngineSpeed": rpm,
        "ActualEngine_PercentTorque": torque,
        "VehicleSpeed" : speed,
        "EngineTorqueMode" : 1,
        "PercentLoadAtCurrentSpeed" : random.randint(20, 80),
        "DriversDemandEngine_PercentTorque" : random.randint( -20, 50),
        "EngineRunning" : 1,
        "EngineControlAllowed" : 1
    })


    # 29-bit J1939 ID

    frame_id = msg.frame_id | 0x80000000  # OR with 0x80000000 to mark extended
    # constructing a new frame with ID (converted to bytes) and appending data
    frame = frame_id.to_bytes(4, 'big') + data
    sock.sendto(frame, (SERVER_IP, SERVER_PORT))
    print("Sent frame (frame sample rpm/torque/speed):" , rpm, torque, speed)

    # Mimics the 100hz refresh rate of J1939
    time.sleep(0.1)