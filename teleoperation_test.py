import sys, select, os
if os.name == 'nt':
  import msvcrt, time
else:
  import tty, termios

VEHICLE_MAX_LIN_VEL = 250
VEHICLE_MIN_LIN_VEL = 0

STEERING_MIN_ANGLE = -2.84
STEERING_MAX_ANGLE = 2.84

LIN_VEL_STEP_SIZE = 10
STEERING_STEP_SIZE = 0.1

msg = """
Control The Vehicle
---------------------------
Moving around:
        w
   a    s    d
        x
w/s : increase/decrease linear velocity 
a/d : increase/decrease steering 
space key, x : force stop
CTRL-C to quit
"""

e = """
Communications Failed
"""

def getKey():
    if os.name == 'nt':
        timeout = 0.1
        startTime = time.time()
        while(1):
            if msvcrt.kbhit():
                if sys.version_info[0] >= 3:
                    return msvcrt.getch().decode()
                else:
                    return msvcrt.getch()
            elif time.time() - startTime > timeout:
                return ''

    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def vels(target_linear_vel, target_angular_vel):
    return "currently:\tlinear vel %s\t angular vel %s " % (target_linear_vel,target_angular_vel)

def makeSimpleProfile(output, input, slop):
    if input > output:
        output = min( input, output + slop )
    elif input < output:
        output = max( input, output - slop )
    else:
        output = input

    return output

def constrain(input, low, high):
    if input < low:
      input = low
    elif input > high:
      input = high
    else:
      input = input

    return input

def checkLinearLimitVelocity(vel):
    
    vel = constrain(vel, VEHICLE_MIN_LIN_VEL, VEHICLE_MAX_LIN_VEL)
    return vel

def checkSteeringLimit(angle):
    angle = constrain(angle, STEERING_MIN_ANGLE, STEERING_MAX_ANGLE)
    return angle

if __name__=="__main__":
    if os.name != 'nt':
        settings = termios.tcgetattr(sys.stdin)

    status = 0
    target_linear_vel   = 0.0
    target_steering  = 0.0
    control_linear_vel  = 0.0
    control_steering = 0.0

   
    print(msg)
    while True:
        key = getKey()
        if key == 'w' :
            target_linear_vel = checkLinearLimitVelocity(target_linear_vel + LIN_VEL_STEP_SIZE)
            status = status + 1
            print(vels(target_linear_vel,target_steering))
        elif key == 's' :
            target_linear_vel = checkLinearLimitVelocity(target_linear_vel - LIN_VEL_STEP_SIZE)
            status = status + 1
            print(vels(target_linear_vel,target_steering))
        elif key == 'a' :
            target_steering = checkSteeringLimit(target_steering + STEERING_STEP_SIZE)
            status = status + 1
            print(vels(target_linear_vel,target_steering))
        elif key == 'd' :
            target_steering = checkSteeringLimit(target_steering - STEERING_STEP_SIZE)
            status = status + 1
            print(vels(target_linear_vel,target_steering))
        elif key == ' ' or key == 'x' :
            target_linear_vel   = 0.0
            control_linear_vel  = 0.0
            target_steering  = 0.0
            control_steering = 0.0
            print(vels(target_linear_vel, target_steering))
        else:
            if (key == '\x03'):
                break

        if status == 100 :
            print(msg)
            status = 0


        control_linear_vel = makeSimpleProfile(control_linear_vel, target_linear_vel, (LIN_VEL_STEP_SIZE/2.0))

        control_steering = makeSimpleProfile(control_steering, target_steering, (STEERING_STEP_SIZE/2.0))

        
    

    # if os.name != 'nt':
    #     termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)