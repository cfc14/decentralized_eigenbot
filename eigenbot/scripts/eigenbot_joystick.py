# initialize joystick
# assemble urdf, drop in
import vrjoystick

from description_assembler_3 import description_assemble 
import numpy as np
import pybullet as p
import pybullet_data
import time
import os
pi= np.pi
def wrap_to_pi(angle):
    return np.remainder(angle + np.pi,  np.pi*2) - np.pi

joy = vrjoystick.init_joystick()


# car test
robot_name = 'car'
module_types = ['Eigenbody',  'Wheel_module', 
 'Wheel_module',  'Wheel_module',  'Wheel_module',
  ]
module_serials = [str(foo) for foo in range(len(module_types))]
graph_edges = [
[0, 1, 0, 0], # from node, to node, port, mount 
[0, 2, 2, 0 ],
[0, 3, 3, 4 ],
[0, 4, 5, 4 ]
]


# hexapod test
robot_name = 'hexapod'
module_types = ['Eigenbody',
            'Bendy_module', 
            'Bendy_module',
            'Bendy_module', 
            'Bendy_module',
            'Bendy_module',
            'Bendy_module',
        'Bendy_module', 
        'Bendy_module',
        'Bendy_module', 
        'Bendy_module',
        'Bendy_module',
        'Bendy_module',
            'Bendy_module', 
            'Bendy_module',
            'Bendy_module', 
            'Bendy_module',
            'Bendy_module',
            'Bendy_module',
        'Static_90deg_module',
        'Static_90deg_module',
        'Static_90deg_module',
        'Static_90deg_module',
        'Static_90deg_module',
        'Static_90deg_module',
            'Foot_module',
            'Foot_module',
            'Foot_module',
            'Foot_module',
            'Foot_module',
            'Foot_module',
      ]
module_serials = [str(foo) for foo in range(len(module_types))]
# graph_edges = [
#     [0, 1, 0, 4 ], # from node, to node, port, mount 
#     [0, 2, 1, 4 ],
#     [0, 3, 2, 4 ],
#     [0, 4, 3, 0 ],
#     [0, 5, 4, 0 ],
#     [0, 6, 5, 0 ],
#         [1, 7, 0, 2 ],
#         [2, 8, 0, 2 ],
#         [3, 9, 0, 2 ],
#         [4, 10, 0, 2 ],
#         [5, 11, 0, 2 ],
#         [6, 12, 0, 2 ],
#         [7, 13, 0, 0 ],
#         [8, 14, 0, 0 ],
#         [9, 15, 0, 0 ],
#         [10, 16, 0, 0 ],
#         [11, 17, 0, 0 ],
#         [12, 18, 0, 0 ],
#         [13, 19, 0, 0 ],
#         [14, 20, 0, 0 ],
#         [15, 21, 0, 0 ],
#         [16, 22, 0, 0 ],
#         [17, 23, 0, 0 ],
#         [18, 24, 0, 0 ],
#         [19, 25, 0, 0 ],
#         [20, 26, 0, 0 ],
#         [21, 27, 0, 0 ],
#         [22, 28, 0, 0 ],
#         [23, 29, 0, 0 ],
#         [24, 30, 0, 0 ],
#     ]

graph_edges = [
    [0, 1, 0, 0 ], # from node, to node, port, mount 
    [0, 2, 1, 0 ],
    [0, 3, 2, 0 ],
    [0, 4, 3, 0 ],
    [0, 5, 4, 0 ],
    [0, 6, 5, 0 ],
        [1, 7, 0, 6 ],
        [2, 8, 0, 6 ],
        [3, 9, 0, 6 ],
        [4, 10, 0, 2 ],
        [5, 11, 0, 2 ],
        [6, 12, 0, 2 ],
        [7, 13, 0, 0 ],
        [8, 14, 0, 0 ],
        [9, 15, 0, 0 ],
        [10, 16, 0, 0 ],
        [11, 17, 0, 0 ],
        [12, 18, 0, 0 ],
        [13, 19, 0, 0 ],
        [14, 20, 0, 0 ],
        [15, 21, 0, 0 ],
        [16, 22, 0, 0 ],
        [17, 23, 0, 0 ],
        [18, 24, 0, 0 ],
        [19, 25, 0, 0 ],
        [20, 26, 0, 0 ],
        [21, 27, 0, 0 ],
        [22, 28, 0, 0 ],
        [23, 29, 0, 0 ],
        [24, 30, 0, 0 ],
    ]


# # hexapod test flipped joints
# robot_name = 'hexapod_mod'
# module_types = ['Eigenbody',
#             'Bendy_module', 
#             'Bendy_module',
#             'Bendy_module', 
#             'Bendy_module',
#             'Bendy_module',
#             'Bendy_module',
#         'Bendy_module', 
#         'Bendy_module',
#         'Bendy_module', 
#         'Bendy_module',
#         'Bendy_module',
#         'Bendy_module',
#             'Bendy_module', 
#             'Bendy_module',
#             'Bendy_module', 
#             'Bendy_module',
#             'Bendy_module',
#             'Bendy_module',
#         'Static_90deg_module',
#         'Static_90deg_module',
#         'Static_90deg_module',
#         'Static_90deg_module',
#         'Static_90deg_module',
#         'Static_90deg_module',
#             'Foot_module',
#             'Foot_module',
#             'Foot_module',
#             'Foot_module',
#             'Foot_module',
#             'Foot_module',
#       ]
# module_serials = [str(foo) for foo in range(len(module_types))]
# graph_edges = [
#     [0, 1, 0, 4 ], # from node, to node, port, mount 
#     [0, 2, 1, 4 ],
#     [0, 3, 2, 4 ],
#     [0, 4, 3, 4 ],
#     [0, 5, 4, 0 ],
#     [0, 6, 5, 0 ],
#         [1, 7, 0, 2 ],
#         [2, 8, 0, 2 ],
#         [3, 9, 0, 2 ],
#         [4, 10, 0, 6 ],
#         [5, 11, 0, 2 ],
#         [6, 12, 0, 2 ],
#         [7, 13, 0, 4 ],
#         [8, 14, 0, 0 ],
#         [9, 15, 0, 0 ],
#         [10, 16, 0, 0 ],
#         [11, 17, 0, 0 ],
#         [12, 18, 0, 0 ],
#         [13, 19, 0, 4 ],
#         [14, 20, 0, 0 ],
#         [15, 21, 0, 0 ],
#         [16, 22, 0, 0 ],
#         [17, 23, 0, 0 ],
#         [18, 24, 0, 0 ],
#         [19, 25, 0, 0 ],
#         [20, 26, 0, 0 ],
#         [21, 27, 0, 0 ],
#         [22, 28, 0, 0 ],
#         [23, 29, 0, 0 ],
#         [24, 30, 0, 0 ],
#     ]

# # wheel-hexapod test
# robot_name = 'hexapod-car'
# module_types = ['Eigenbody', # 0
#         'Wheel_module',# 1
#         'Bendy_module',  # 2
#             'Bendy_module',
#             'Bendy_module',
#             'Static_90deg_module',
#             'Foot_module',
#         'Bendy_module', # 7
#             'Bendy_module',
#             'Bendy_module',
#             'Static_90deg_module',
#             'Foot_module',
#         'Wheel_module', #12
#         'Bendy_module', # 13
#             'Bendy_module',
#             'Bendy_module',
#             'Static_90deg_module',
#             'Foot_module',
#         'Bendy_module', #18
#             'Bendy_module',
#             'Bendy_module',
#             'Static_90deg_module',
#             'Foot_module',
#       ]
# module_serials = [str(foo) for foo in range(len(module_types))]
# graph_edges = [# from node, to node, port, mount 
#     [0, 1, 0, 1], # wheel
#     [0, 2, 1, 4 ], # leg
#     [2, 3, 0, 2 ],
#     [3, 4, 0, 0 ],
#     [4, 5, 0, 0 ],
#     [5, 6, 0, 0 ],
#     [0, 7, 2, 4 ], # leg
#     [7, 8, 0, 2 ],
#     [8, 9, 0, 0 ],
#     [9, 10, 0, 0 ],
#     [10, 11, 0, 0 ],
#     [0, 12, 3, 3], # wheel
#     [0, 13, 4, 0 ], # leg
#     [13, 14, 0, 2 ],
#     [14, 15, 0, 0 ],
#     [15, 16, 0, 0 ],
#     [16, 17, 0, 0 ],
#     [0, 18, 5, 0 ], # leg
#     [18, 19, 0, 2 ],
#     [19, 20, 0, 0 ],
#     [20, 21, 0, 0 ],
#     [21, 22, 0, 0 ]   
#     ]


description_assemble(module_types, graph_edges, module_serials)


n_chassis_ports = 6
limb_types = [None]*n_chassis_ports
wheel_joint_ids = [None]*n_chassis_ports
leg_joint_ids = [None]*n_chassis_ports
leg_joint_orns = [None]*n_chassis_ports
open_set = [list() for i in range(n_chassis_ports)]
limb_info = []
for edge in graph_edges:
    if module_types[edge[0]] == 'Eigenbody':
        open_set[edge[2]].append(edge[1:4]) # a child to open
for chassis_port in range(n_chassis_ports):
    joints_ids_branch = []
    joint_orn_branch = []

    while len(open_set[chassis_port])>0:
        edge_popped = open_set[chassis_port].pop()
        child_index, child_port, child_mount = edge_popped
        child_type = module_types[child_index]
        if module_types[child_index] == 'Wheel_module':
            limb_types[chassis_port] = 'wheel_limb'
            wheel_joint_ids[chassis_port] = module_serials[child_index]
        elif module_types[child_index] == 'Foot_module':
            limb_types[chassis_port] = 'foot_limb'
            #   track which joints are in the leg
            leg_joint_ids[chassis_port] = joints_ids_branch
            leg_joint_orns[chassis_port] = joint_orn_branch
        else:
            if module_types[child_index] == 'Bendy_module':
                joints_ids_branch.append(module_serials[child_index])
                joint_orn_branch.append(child_mount)

            for edge in graph_edges:
                if edge[0] == child_index:
                    open_set[chassis_port].append(edge[1:4])
                    
    
print('limb_types' ,limb_types) 
print('wheel_joint_ids', wheel_joint_ids)
print('leg_joint_ids', leg_joint_ids)        
print('leg_joint_orns', leg_joint_orns)        

# keep track of which orientation the joint axes are in
# This appears to work properly for the first and possibly second joint on each leg,
# but fails for the last joint. Not sure why.
leg_joint_orns_cumulative = [None]*n_chassis_ports
leg_joint_multiplier = [None]*n_chassis_ports
for i in range(6):
    if leg_joint_orns[i] is not None:
        leg_joint_orns_cumulative[i] = wrap_to_pi(np.cumsum(leg_joint_orns[i])*np.pi/4)
        leg_joint_multiplier[i] = []
        for j in range(len(leg_joint_orns[i])):
            if np.abs(leg_joint_orns_cumulative[i][j])<= np.pi/2 :
                leg_joint_multiplier[i].append(1)
            else:
                leg_joint_multiplier[i].append(-1)


# for i in range(6):
#     if leg_joint_orns[i] is not None:
#         leg_joint_orns_cumulative[i] = np.cumsum(leg_joint_orns[i])*np.pi/4
#         leg_joint_multiplier[i] = []
#         for j in range(len(leg_joint_orns[i])):
#             if j==0:
#                 addition = 0
#             else:
#                 addition = -2
#             orn_wrapped = np.round(
#                 wrap_to_pi(leg_joint_orns_cumulative[i][j]+addition)/(np.pi/4)
#                 )
#             if np.abs(orn_wrapped)<= 2 :
#                 leg_joint_multiplier[i].append(1)
#             else:
#                 leg_joint_multiplier[i].append(-1)
                      



print('leg_joint_orns_cumulative', leg_joint_orns_cumulative)        
print('leg_joint_multiplier', leg_joint_multiplier)        



cwd = os.path.dirname(os.path.realpath(__file__))

# setup world
physicsClient = p.connect(p.GUI)# p.DIRECT for non-graphical version
p.configureDebugVisualizer(p.COV_ENABLE_GUI,0,physicsClientId=physicsClient)
p.resetDebugVisualizerCamera(1,0,-65,[0,0,0],physicsClientId=physicsClient) # I like this view

p.resetSimulation(physicsClient) # remove all objects from the world and reset the world to initial conditions. (not needed here but kept for example)
p.setGravity(0,0,-9.81,physicsClientId=physicsClient)
planeId = p.loadURDF(os.path.join(pybullet_data.getDataPath(), "plane100.urdf"),physicsClientId=physicsClient)



# add robot
urdf_name = '/home/cobracommander/catkin_ws/src/eigenbot/urdf/autoXACRO.urdf'
startOrientation = p.getQuaternionFromEuler([0,-np.pi/2,0])
    # os.path.join(cwd, urdf_name),

robotID = p.loadURDF(urdf_name,
    basePosition=[0,0,0.5], baseOrientation=startOrientation,
                               flags= (p.URDF_MAINTAIN_LINK_ORDER | 
                               p.URDF_USE_SELF_COLLISION | 
                               p.URDF_ENABLE_CACHED_GRAPHICS_SHAPES), # "The following flags can be combined using a bitwise  OR, |"
                               physicsClientId=physicsClient)

num_joints_total = p.getNumJoints(robotID,physicsClientId=physicsClient)
moving_joint_inds = []
joint_names = []
moving_joint_names = []
moving_joint_types = []
moving_joint_limits = []
moving_joint_centers = []
moving_joint_max_torques = []
moving_joint_max_velocities = []
# getJointInfo 8 9 are jointLowerLimit and jointUpperLimit 

# collect joint info
for j_ind in range(num_joints_total):
    j_info = p.getJointInfo(robotID, j_ind, physicsClientId=physicsClient)
    joint_names.append(j_info[1])
    if j_info[2] != (p.JOINT_FIXED):
        moving_joint_inds.append(j_ind)
        j_limits = [j_info[8], j_info[9]]
        j_center = (j_info[8] + j_info[9])/2
        if j_limits[1]<=j_limits[0]:
            j_limits = [-np.inf, np.inf]
            j_center = 0
        moving_joint_limits.append(j_limits)
        moving_joint_centers.append(j_center)

        moving_joint_names.append(j_info[1])
        moving_joint_max_torques.append(j_info[10])
        moving_joint_max_velocities.append(j_info[11])
        moving_joint_types.append(j_info[2])
num_joints = len(moving_joint_inds)

print('Moving joints:')
print('moving_joint_names')
print(moving_joint_names)
print('moving_joint_limits') # NOTE: if limits[1]<limits[0] then pybullet ignores the limits.
print(moving_joint_limits) # NOTE: if limits[1]<limits[0] then pybullet ignores the limits.
print('moving_joint_centers')
print(moving_joint_centers)
print('moving_joint_max_torques')
print(moving_joint_max_torques)
print('moving_joint_max_velocities')
print(moving_joint_max_velocities)
print('moving_joint_types')
print(moving_joint_types)

lower_limits = []
upper_limits = []
for m in moving_joint_limits:
    lower_limits.append(m[0])
    upper_limits.append(m[1])

joint_serials =[]
for mj_bytes in moving_joint_names:
    mj = mj_bytes.decode('utf-8')
    print(mj)
    serial_index = mj.find('_S')
    joint_serial = mj[serial_index+2:]
    joint_serials.append(joint_serial)
print('joint serials: ' + str(joint_serials) )


# set to a centered initial joint angle
for i in range(num_joints):
    center = moving_joint_centers[i]
    jind = moving_joint_inds[i]
    p.resetJointState( bodyUniqueId=robotID, 
        jointIndex = jind,
        targetValue=center, physicsClientId=physicsClient )

# parameters for alternating tripod
amplitude_max = pi/8
amplitudes = amplitude_max*np.ones([3,6])

period = 1.5
# phase_offsets_back = np.array([[1/2,-1/2,1/2,-1/2,1/2,-1/2], # forward
#     [0,1,0,1,0,1], [1,0,1,0,1,0]])*np.pi
# phase_offsets_forward = np.array([[-1/2,1/2,-1/2,1/2,-1/2,1/2], # back
#     [0,1,0,1,0,1], [1,0,1,0,1,0]])*np.pi
# phase_offsets_right = np.array([[1/2,-1/2,1/2,1/2,-1/2,1/2], # turn right
#     [0,1,0,1,0,1], [1,0,1,0,1,0]])*np.pi
# phase_offsets_left = np.array([[-1/2,1/2,-1/2,-1/2,1/2,-1/2], # turn left
#     [0,1,0,1,0,1], [1,0,1,0,1,0]])*np.pi
const_offsets = np.array([[-1,0,1,-1,0,1], 
    [0,0,0,0,0,0], [0,0,0,0,0,0]])*np.pi/4
phase_offsets = np.array([[0.5,-0.5,0.5,-0.5,0.5,-0.5], # forward # NOTE: python2 needs to force float division
    [0,1,0,1,0,1], [1,0,1,0,1,0]])*np.pi 

# main loop:
t=0
dt=1./240
j_positions= np.zeros(num_joints)
wave_phase = 0


# logID = p.startStateLogging(p.STATE_LOGGING_VIDEO_MP4, fileName=robot_name+'.mp4')
while True:

    axes, buttons, povs = vrjoystick.read(joy)
    forward_cmd = axes[1]
    turn_cmd = axes[0]

# for test
    # amplitudes[0,0:3] = amplitude_max*np.ones(3)*(forward_cmd)
    # amplitudes[0,3:6] = amplitude_max*np.ones(3)*(forward_cmd)

    # amplitudes = amplitude_max*np.ones(6)*np.linalg.norm(axes[0:2])
    # amplitudes = np.clip(amplitudes, 0, amplitude_max)

    # good for car
    amplitudes[0,0:3] = amplitude_max*np.ones(3)*(-forward_cmd+turn_cmd)
    amplitudes[0,3:6] = amplitude_max*np.ones(3)*(-forward_cmd-turn_cmd)
    amplitudes = np.clip(amplitudes, -amplitude_max, amplitude_max)

    if np.linalg.norm(axes[0:2])>0.01:
        wave_phase += dt

    # if forward_cmd>0.01:
    #     phase_offsets = phase_offsets_forward
    # elif forward_cmd<-0.01:
    #     phase_offsets = phase_offsets_back
    # elif turn_cmd>0.01:
    #     phase_offsets = phase_offsets_right
    # elif turn_cmd<-0.01:
    #     phase_offsets = phase_offsets_left

    if buttons[0]:
        phase_offsets[0,0] += np.pi/4
        print(phase_offsets)
        time.sleep(1)

    if buttons[1]:
        phase_offsets[0,1] += np.pi/4
        time.sleep(1)
        print(phase_offsets)

    if buttons[2]:
        phase_offsets[0,2] += np.pi/4
        time.sleep(1)
        print(phase_offsets)

    if buttons[3]:
        phase_offsets[0,3] += np.pi/4
        time.sleep(1)
        print(phase_offsets)

    # j_velocities = np.ones(num_joints)*axes[0]

    # given a joystick command, convert it into wheel velocities setpoints

    j_velocities = np.zeros(num_joints)
    for i in range(n_chassis_ports):
        if wheel_joint_ids[i] is not None:
            if i<3:
                cmd = -(-forward_cmd + turn_cmd)
            elif i>=3:
                cmd = -(forward_cmd + turn_cmd)

            index_of_wheel = joint_serials.index(wheel_joint_ids[i])
            j_velocities[index_of_wheel] = cmd*moving_joint_max_velocities[index_of_wheel]


    # given a joystick command, convert it into leg position setpoints
    for i in range(6):
        leg_angles_i = amplitudes[:,i]*np.sin(wave_phase*2*pi/period - phase_offsets[:,i]) + const_offsets[:,i]
        leg_angles_i[1:] = np.clip(leg_angles_i[2:], 0, np.inf) # convert up-down motion to up-flat motion
        leg_angles_i[2] = -leg_angles_i[2]
        if leg_joint_ids[i] is not None:
            # leg_cmd.append(leg_angles[i][:len(leg_joint_ids[i])])
            for j in range(len(leg_joint_ids[i])):
                leg_joint_id = leg_joint_ids[i][j]
                index_of_joint = joint_serials.index(leg_joint_id)
                j_positions[index_of_joint] = leg_angles_i[j] * leg_joint_multiplier[i][j]
                # j_positions[index_of_joint] = leg_angles_i[j]

    j_positions += j_velocities*dt



    # velocity control: take the action and convert directly into velocity 
    # j_velocities = np.clip(j_velocities, 
    #     -np.array(moving_joint_max_velocities), np.array(moving_joint_max_velocities))
    # p.setJointMotorControlArray(robotID, moving_joint_inds, 
    #     controlMode=p.VELOCITY_CONTROL,
    #     targetVelocities = j_velocities,
    #     forces = moving_joint_max_torques, physicsClientId=physicsClient)

    # test to check specific joint angles
    # j_pos = moving_joint_centers[:]

    j_positions = np.clip(j_positions, 
        np.array(lower_limits), np.array(upper_limits))

    p.setJointMotorControlArray(robotID, moving_joint_inds, 
        controlMode=p.POSITION_CONTROL,
        targetPositions = j_positions,
        forces = moving_joint_max_torques, physicsClientId=physicsClient)

    p.stepSimulation(physicsClientId=physicsClient)
    t+=dt

    linkWorldPosition, linkWorldOrientationQuat= p.getBasePositionAndOrientation(bodyUniqueId=robotID,physicsClientId= physicsClient)
    # print(linkWorldPosition)
    time.sleep(dt)


    # keys = p.getKeyboardEvents()
    # if p.KEY_WAS_TRIGGERED:
    #     time.sleep(10)
    if np.any(buttons[8:]) :
        break

# p.stopStateLogging(logID)