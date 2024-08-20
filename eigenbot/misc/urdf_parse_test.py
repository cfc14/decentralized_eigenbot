'''
Parse urdf info joint names, limits, using ROS package and not using pybullet

'''

# http://wiki.ros.org/urdfdom_py
# install with: sudo apt install ros-kinetic-urdfdom-py

# Load the urdf_parser_py manifest, you use your own package
# name on the condition but in this case, you need to depend on
# urdf_parser_py.
import roslib; roslib.load_manifest('urdfdom_py')
import rospy
import json
import numpy as np
# Import the module

from urdf_parser_py.urdf import URDF




robot = URDF.from_xml_file('/home/cobracommander/catkin_ws/src/eigenbot/urdf/autoXACRO.urdf')

try:
    print('Root is: ' + str(robot.get_root()))


    num_joints_total = len(robot.joints)
    moving_joint_inds = []
    joint_names = []
    moving_joint_names = []
    moving_joint_types = []
    moving_joint_limits = []
    moving_joint_centers = []
    moving_joint_max_torques = []
    moving_joint_max_velocities = []

    for j in range(num_joints_total):
        joint = robot.joints[j]
        if (joint.type == 'continuous') or (joint.type == 'revolute'):
            moving_joint_inds.append(j)
            moving_joint_names.append(joint.name)
            moving_joint_types.append(joint.type)

            joint_limit_upper = np.inf
            joint_limit_lower = -np.inf
            moving_joint_centers.append(0)
            if joint.limit is not None:
                if joint.limit.lower is not None:
                    joint_limit_lower = joint.limit.lower
                if joint.limit.upper is not None:
                    joint_limit_upper = joint.limit.upper
                if joint.limit.lower is not None and joint.limit.upper is not None:
                    moving_joint_centers[-1] = (joint_limit_lower+joint_limit_upper)/2

                if joint.limit.effort is not None:
                    moving_joint_max_torques.append(joint.limit.effort)
                else:
                    moving_joint_max_torques.append(100)
                if joint.limit.velocity is not None:
                    moving_joint_max_velocities.append(joint.limit.velocity)
                else:
                    moving_joint_max_velocities.append(100)

            moving_joint_limits.append([joint_limit_lower,joint_limit_upper])
    num_joints = len(moving_joint_inds)
    print('Moving joints:' + str(num_joints))
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

except:
    print('Error parsing URDF')