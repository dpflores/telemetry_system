import time
import socket
import struct
import sys


can_frame_fmt = "=IB3x8s"
can_frame_size = struct.calcsize (can_frame_fmt)

def dissect_can_frame(frame):
    can_id, can_dlc, data = struct.unpack(can_frame_fmt, frame) 
    return (can_id, can_dlc, data[:can_dlc])

def build_can_frame(can_id, data):
    can_dlc = len(data)
    data = data.ljust(8, b'\x00')
    return struct.pack(can_frame_fmt, can_id, can_dlc, data)
    


s = socket.socket (socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
# s.bind(("can0",))              
#s.bind(("can1",))  
print(build_can_frame(0x09, b'\x05\x06'))
while True:
    s.send(build_can_frame(0x09, b'\x05\x06')) 