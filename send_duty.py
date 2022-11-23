from can import *


# CAN configuration
can_id = 0x10
can_frame_fmt = "=IB3x8s"
can_port = "can0"

can = CAN(can_frame_fmt, can_port, can_id)

speed =257
speed_data = speed.to_bytes(2, 'big')

print(speed_data)
print(int.from_bytes(speed_data,'big'))
can.send_control(speed_data,str(0.1))


