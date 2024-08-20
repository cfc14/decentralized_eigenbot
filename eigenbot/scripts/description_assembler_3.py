#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 2 13:59:15 2019

@author: jwhitman@cmu.edu
Julian Whitman
This file reads in modules from xml and then writes an xacro for ros use.

Then it launches rviz after a keypress (to save from having to type the command)


TODO: reads and import the same files multiple times, could check for repeats.

"""
import xml.etree.ElementTree as ET
import subprocess
import sys
import os

def description_assemble(graph_nodes, graph_edges, graph_nodes_serials):
#if True:
    print('Assembling with graph_nodes_serials')
    print(graph_nodes_serials)

    # uses https://docs.python.org/2/library/xml.etree.elementtree.html
    # edges have form # [from node, to node, port, mount] 


    #  catkin_path = subprocess.check_output(['catkin', 'locate']) # get path of ROS workspace
    # catkin_path = '~/catkin_ws'
    cwd = os.getcwd()
    catkin_path = cwd[:cwd.rfind('_ws') + len('_ws')]
    eigenbot_path = catkin_path + '/src/eigenbot'

    #catkin_path = catkin_path[0:-1] # remove the \n from end of string
    print("eigenbot path:" + eigenbot_path)

    # preallocations:
    input_ports = []
    fnames = []
    output_ports = []
    M_nums = []
    treeList = list()

    for module_num in range(len(graph_nodes)):
        module_name = graph_nodes[module_num]

        mod_path = 'description/' + module_name + '.xml'
        tree = ET.parse(os.path.join(eigenbot_path, mod_path))
        treeList.append(tree)
        root = tree.getroot()

        # find the file name field
        fname = root.find('filename').text
        fnames.append(fname)

        # find the input port field
        input_port = root.find('input_port').text
        input_ports.append(input_port)

        ports = root.find('output_ports')
        output_ports.append(ports)
        #    for child in ports:
        #        print(child.tag, child.attrib, child.text

        M_num = 'M' + str(module_num) + '_S' + str(graph_nodes_serials[module_num])
        M_nums.append(M_num)
        print("file: " + fname + ", input port: " + input_port + ', Label: ' + M_num)
        
    parent_rigid_bodies = []
    child_rigid_bodies = []
    mount_xyz = []
    mount_rpy = []
    for edge in graph_edges:
        # from node, to node, port, mount
        from_node, to_node, active_port, active_mount  = edge
        port = output_ports[from_node][active_port] # from xml ports listing
        child_module = graph_nodes[to_node]

        parent_rigid_body = port.find('parent').text + M_nums[from_node]
        parent_rigid_bodies.append(parent_rigid_body)

        child_rigid_body = input_ports[to_node] + M_nums[to_node]
        child_rigid_bodies.append(child_rigid_body)

        mounts = port.findall('mount')

        mount = mounts[active_mount]
        xyz = mount.find('xyz').text
        rpy = mount.find('rpy').text
        # xyz = xyz.split(" ")
        # xyz_n = []
        # xyz_n = [float(xyz[i]) for i in range(len(xyz))]
        # xyz_n = [xyz_n[i]  for i in range(3)]
        # xyz = [str(xyz_n[i]) for i in range(len(xyz))]
        # xyz = " ".join(xyz)
        mount_xyz.append(xyz)
        mount_rpy.append(rpy)
        print("attach " + str(child_rigid_body) + " on " 
            + str(parent_rigid_body) + " at (" + xyz + '), (' + rpy + ")")

    # keep the last module's first output port
    # last_output = node_ports[-1][0].find('parent').text + M_num_parent

    # after reading in all the modules and ports, we can now write the file
    f = open(os.path.join(eigenbot_path, 'urdf/autoXACRO.xacro'), 'w')
    f.write('<?xml version="1.0"?> \n')
    f.write('<robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="modular_robot_compiled">  \n\n')
    f.write('<xacro:property name="M_PI" value="3.1415926535897931" /> \n')
    for module_num in range(len(graph_nodes)):	
        f.write('<!--' + 'Include files for, then joint to attach, module type ' + graph_nodes[module_num] + '-->\n')
        M_num = M_nums[module_num]

        # write file name to include
        fname = fnames[module_num]
        f.write('<xacro:include filename="../urdf/' + fname + '"/>\n')

        # invoke the file with the module number ID as name
        dot_index = fname.find('.') # returns first instance of the dot
        xacro_name = fname[0:dot_index] 
        f.write('<xacro:' + xacro_name + ' module_label="' + M_num + '"/>\n\n')

    for edge_num in range(len(graph_edges)):
        # from_node, to_node, active_mount, active_port = graph_edges[edge_num]
    	# write joints between the module and its child
    	f.write('<joint name="connection_' + str(edge_num) + '_attachment" type="fixed">' + "\n")
    	f.write('  <origin' + "\n")
    	f.write('    xyz="' + str(mount_xyz[edge_num]) + '"\n')
    	f.write('    rpy="' + str(mount_rpy[edge_num]) + '"\n')
    	f.write('  />' + "\n")
    	f.write('  <parent link="' + parent_rigid_bodies[edge_num] + '"/>' + "\n")
    	f.write('  <child link="' + child_rigid_bodies[edge_num] + '"/>' + "\n")
    	f.write('</joint>' + "\n")
    	f.write('\n')

    f.write('</robot>' + "\n")
    f.close()



  # run some commands to make the package. 


    # compile xacro to urdf
    urdf_path = eigenbot_path+'/urdf/'
    p = subprocess.Popen('rosrun xacro xacro --inorder -o ' + urdf_path + 'autoXACRO.urdf ' + urdf_path + 'autoXACRO.xacro', shell=True, cwd="/")
    p.wait()

    # next read the newly created urdf to extract all the joint names, so that they can be used for moveit config files
    urdf_tree = ET.parse(urdf_path + 'autoXACRO.urdf')
    urdf_root = urdf_tree.getroot()
    joint_list = urdf_root.findall('joint')
    moving_joint_list= []
    joint_parent_list = []
    joint_child_list = []
    for joint in joint_list:
        joint_parent_list.append(joint.find('parent').get('link'))
        joint_child_list.append( joint.find('child').get('link') )
        if joint.get('type')=='continuous' or joint.get('type')=='revolute' or joint.get('type')=='prismatic':
            moving_joint_list.append(joint.get('name'))

    print("Joints found: " + str(moving_joint_list))

##  raw_input("Press enter to continue...")
#  input("Press enter to continue...")
#
#  # Launch moveit
#  #print("launching moveit in rviz"
#  #p= subprocess.Popen('roslaunch eigenbot_moveit_config demo.launch', cwd=catkin_path) #  shell=True,
#
#  # launch rviz demo: This process can cause issues with hidden roscores so be careful if enabling it.
#  print("launching rviz demo")
#  p= subprocess.Popen('roslaunch eigenbot rviz_test.launch', shell=True, cwd=catkin_path)
#  #p.wait()
#

if __name__== "__main__":



# car test
  graph_nodes = ['Eigenbody',
     'Wheel_module', 
     'Wheel_module',
      'Wheel_module', 
      'Wheel_module',
      ]
  graph_nodes_serials = [str(foo) for foo in range(len(graph_nodes))]
  graph_edges = [
    [0, 1, 0, 0], # from node, to node, port, mount 
    [0, 2, 2, 0 ],
    [0, 3, 3, 4 ],
    [0, 4, 5, 4 ]
    ]

# # car test
#   graph_nodes = ['Eigenbody',     'Wheel_module', 

#       ]
#   graph_nodes_serials = [str(foo) for foo in range(len(graph_nodes))]
#   graph_edges = [    [0, 1, 0, 2 ], # from node, to node, port, mount 

#     ]


# # hexapod test
#   graph_nodes = ['Eigenbody',
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
#   graph_nodes_serials = [str(foo) for foo in range(len(graph_nodes))]
#   graph_edges = [
#     [0, 1, 0, 2 ], # from node, to node, port, mount 
#     [0, 2, 1, 2 ],
#     [0, 3, 2, 2 ],
#     [0, 4, 3, 2 ],
#     [0, 5, 4, 2 ],
#     [0, 6, 5, 2 ],
#         [1, 7, 0, 6 ],
#         [2, 8, 0, 6 ],
#         [3, 9, 0, 6 ],
#         [4, 10, 0, 6 ],
#         [5, 11, 0, 6 ],
#         [6, 12, 0, 6 ],
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



  description_assemble(graph_nodes, graph_edges, graph_nodes_serials)
  # import urdf_loader_test