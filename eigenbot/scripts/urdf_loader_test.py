import numpy as np
import pybullet as p
import pybullet_data
import time
import os
cwd = os.path.dirname(os.path.realpath(__file__))

# setup world
physicsClient = p.connect(p.GUI)# p.DIRECT for non-graphical version
p.configureDebugVisualizer(p.COV_ENABLE_GUI,0,physicsClientId=physicsClient)

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
        moving_joint_types.append(j_info[2])
num_joints = len(moving_joint_inds)

print('Moving joints:')
print(moving_joint_names)
print(moving_joint_limits) # NOTE: if limits[1]<limits[0] then pybullet ignores the limits.
print(moving_joint_centers)
print(moving_joint_max_torques)
print(moving_joint_types)


# set to a centered initial joint angle
for i in range(num_joints):
    center = moving_joint_centers[i]
    jind = moving_joint_inds[i]
    p.resetJointState( bodyUniqueId=robotID, 
        jointIndex = jind,
        targetValue=center, physicsClientId=physicsClient )



# main loop:
t=0
while True:


    j_velocities = np.ones(num_joints)*np.sin(t*1)*np.pi/4


    # velocity control: take the action and convert directly into velocity 
    # p.setJointMotorControlArray(robotID, moving_joint_inds, 
    #     controlMode=p.VELOCITY_CONTROL,
    #     targetVelocities = j_velocities,
    #     forces = moving_joint_max_torques, physicsClientId=physicsClient)

    # test to check specific joint angles
    j_pos = moving_joint_centers[:]

    p.setJointMotorControlArray(robotID, moving_joint_inds, 
        controlMode=p.POSITION_CONTROL,
        targetPositions = j_pos + j_velocities,
        forces = moving_joint_max_torques, physicsClientId=physicsClient)

    p.stepSimulation(physicsClientId=physicsClient)
    t+=1./240

    linkWorldPosition, linkWorldOrientationQuat= p.getBasePositionAndOrientation(bodyUniqueId=robotID,physicsClientId= physicsClient)
    # print(linkWorldPosition)
    time.sleep(1./240)


    # keys = p.getKeyboardEvents()
    # if p.KEY_WAS_TRIGGERED:
    #     time.sleep(10)