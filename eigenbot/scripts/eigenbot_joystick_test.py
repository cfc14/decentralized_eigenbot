

import vrjoystick
import numpy as np
import time
import itertools
import os
pi= np.pi
def wrap_to_pi(angle):
    return np.remainder(angle + np.pi,  np.pi*2) - np.pi

def np2str(input, precision=2):
    return np.array2string(input,precision=2)

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
import rosnode

SEND_COMMANDS = False # if true, publishes ROS commands
SEND_COMMANDS = True # if true, publishes ROS commands



def joint_state_talker():

    joy = vrjoystick.init_joystick()

    cwd = os.path.dirname(os.path.realpath(__file__))

    lower_limits = [0]
    upper_limits = [2.5]
    num_joints = 1

    # collect joint serial numbers for use in ROS joint commands
    joint_serials =[u'14']
    print('joint serials: ' + str(joint_serials) )





### MAIN LOOP
    if SEND_COMMANDS:
        pub = rospy.Publisher('/eigenbot/joint_cmd', JointState, queue_size=1)
    ros_nodes = rosnode.get_node_names()
    print('Nodes running: ' + str(ros_nodes))
    if not ('/description_listener' in ros_nodes):
        # the "description_listener" makes the node
        rospy.init_node('description_listener') 

    joint_fb = rospy.wait_for_message("/eigenbot/joint_fb", JointState)
    print('Initial positions:')
    print(joint_fb.position)

    rate_hz = 20
    # rate_hz = 15
    rate = rospy.Rate(rate_hz) # 10hz
    dt = 1./rate_hz
    dt_sim = 1./240 # default of pybullet
    n_steps_per_rate = dt/dt_sim
    n_steps_per_rate = int(np.round(n_steps_per_rate))
    joint_state = JointState()
    t=0
    j_positions= np.zeros(num_joints)
    wave_phase = 0

    print(' ----------- starting main loop -----------')
    while not rospy.is_shutdown():

        # joint_state.header.stamp = 'Eigenbot joint state'
        joint_state.header.stamp = rospy.Time.now()



        axes, buttons, povs = vrjoystick.read(joy)

        # button 9-12 ends it all
        if np.any(buttons[8:]) :
            break


        forward_cmd = axes[1]
 
        j_positions += forward_cmd*dt*4

        j_positions = np.clip(j_positions, 
            np.array(lower_limits), np.array(upper_limits))
       

        t+=dt



        # get serial numbers out of joint name fields 
        joint_state.name = []
        # for joint_name in moving_joint_names:
            # joint_serial = joint_name[joint_name.find('_S')+2:]
        joint_serial = joint_serials[0]
        joint_state.name.append(joint_serial)
        # Note: eigenbot driver requires all pos, vel, effort to be same length.
        joint_state.position = j_positions
        joint_state.velocity = [float('nan')]*num_joints
        joint_state.effort = [float('nan')]*num_joints
        print(np2str(joint_state.position))
        if SEND_COMMANDS:
            pub.publish(joint_state)
        rate.sleep()

if __name__ == '__main__':
    try:
        joint_state_talker()
    except rospy.ROSInterruptException:
        pass

