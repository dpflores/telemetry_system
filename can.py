# Getting CAN data
import socket
import struct

class CAN():
    def __init__(self, can_frame_fmt, can_port,can_id):
        self.can_id = can_id
        self.can_frame_fmt = can_frame_fmt
        self.can_frame_size = struct.calcsize(can_frame_fmt)
        self.s = socket.socket(socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
        self.s.bind((can_port,))


        # For speed measurements
        self.previous_speed = 0
        self.speed = 0
        ## jsjsjs

    def dissect_can_frame(self, frame):
        can_id, can_dlc, data = struct.unpack(self.can_frame_fmt, frame) 
        return (can_id, can_dlc, data[:can_dlc])
    
    def build_can_frame(self, can_id, data):
        can_dlc = len(data)
        data = data.rjust(8, b'\x00')
        print(data) ###
        return struct.pack(self.can_frame_fmt, can_id, can_dlc, data)
    
    def send_can(self, data):
        self.s.send(self.build_can_frame(self.can_id, data))

    def send_control(self, speed, steering):    
        ## Check this function
        data = speed
        can_data = self.build_can_frame(self.can_id, data)
        self.s.send(can_data)
        

    def get_vel(self, sender_id):
        cf, addr = self.s.recvfrom(16)
        can_id = self.dissect_can_frame(cf)[0]
        if can_id == sender_id :
            can_dlc = self.dissect_can_frame(cf)[1]
            dataL = hex((self.dissect_can_frame(cf)[2])[0])#Data LSB
            dataH = hex((self.dissect_can_frame(cf)[2])[1])#Data HSB
    
            #data= (int (dataH,16))<<8| int (dataL,16)
            self.speed = int (dataH,16) + int (dataL,16)

            return self.speed

        self.previous_speed = self.speed
        return self.previous_speed
