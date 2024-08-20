# eigenbot
Eigenbot module automatic model building

Contact: Julian Whitman
<jwhitman@cmu.edu>, Shuo

Each module will know its own urdf, and will provide its indentification number/name, which modules are attached to it as children, which ports children are on, and which orientation children are affixed.

Module's urdf.xacro should have their stl, inertial properties these are standard urdf parts.
They will also need additional non-standard properties about the ports and mounts. The ports are places where children modules can be attached, and the mounts are the different orientations that a child module can be affixed to a port. There may also include some other properties, like whether it can communicate wirelessly, or have a battery, for future-proofing.
This framework should allow the addition of arbitrary robots as "modules" to the system: if you take an existing urdf, and add a wrapper which defines the ports, then it can act as a module.


RUN ORDER 9/14/2020
roscore
rosrun eigenbot talker.py
python scripts/description_listener.py
roslaunch eigenbot rviz_no_slider.launch

(might need to change serial number of eigenbody frame in rviz_no_slider)


USAGE NOTES FROM CHARLIE

Usage notes:
1. Charge robot with any 25V supply at 0.5A-2A (0.5A charger supplied). Robot is safe to use while charging, will continue to charge while switched off. Minimum voltage is 20V.
2. Turn on robot,wait for orange glow on one side of robot to indicate wifi is available.
3. With your ROS PC, connect to WiFi SSID "eigenbot" and note your IP in the 10.10.10.x range. The ethernet cable also works, and will request an IP from the wired network's DHCP server.
4. Optional: Set local PC's ROS_MASTER_URI to 10.10.10.1, and ROS_IP to the address noted above.
5. Optional: Log in via ssh eigenbot@10.10.10.1 or ubuntu@10.10.10.1 (biorobotics lab members only)
6. The `rostopic list` command should show eigenbot/in, eigenbot/out, eigenbot/joint_cmd, eigenbot/joint_fb, and eigenbot/topology topics.
7. Make robot move: With legs in the pictured configuration, the eigenbot_driver package has a eigen_quadruped_walk.py script that demonstrates joint control.Known issues:
1. Eigen Modules all begin to miscommunicate after one hour, overwhelming real communication.
2. Eigen Modules will sometimes appear to disconnect, and sometimes actually disconnect.
3. Eigen Modules send garbage data sometimes, but it's mostly harmless.
4. Eigen Modules' feedback messages can be late or missed, so eigenbot/joint_fb may not always have all feedback values.
5. Torque/Effort commands are unimplemented in Eigen Module firmware. Disabling Torque/Effort loops is not implemented either.

Notes on using extra ros computer with eigenbot as master:
export ROS_MASTER_URI=http://10.10.10.1:11311 and export ROS_IP=10.10.10.x where x is your wifi ip should be all you need to get rostopic list to show the eigenbot topics

Julian notes that:
- use http in ROS_MASTER_URI not https
- might have to add 10.10.10.1 eigenbot to your computer etc/hosts, since the messages get published by the "http://eigenbot" address on the robot

RUN ORDER 9/10/2020

python scripts/eigenbot_joystick_ros.py 
then
roslaunch eigenbot rviz_no_slider.launch

## NEED TO UPDATE BELOW HERE ##

## Quickstart ##
A script that will subscribe to eigenbot/topology, listen for the next message of that type, then parse it, convert it to urdf, and open rviz, where rviz publishes joint states, is:
cd to folder eigenbot/eigenbot/script
chmod +x description_listener.py (only need to do this once)

rosrun eigenbot description_listener.py 

(you must have roscore running in the background)

## Eigenbot package ##

The program is been wrapped up by a ROS package "eigenbot" in order to better leverage tools in ROS to process urdf and visualize the robot. 

To use this eigenbot package, first create a ROS workspace and then put package "eigenbot" under the src of the workspace. Use catkin\_make to compile the package (although this package does not contain any C/C++ files, compliation in ROS workspace allows ROS to search for this package. Please refer to [ROS Tutorials](http://wiki.ros.org/ROS/Tutorials/CreatingPackage) for more information.

There are follows files and folders under eigenbot:

1. CMakeLists.txt   package.xml  | ROS indexing files. Do not need to modify. 

2. description  |  fold contains xml and text files to describe our robot modules

3. include     src   | folders contain C/C++ source code. Empty currently.    

4. launch | folder contains launch files to display robot in rviz and gazebo 

5. meshes | folder contains stl files  
 
6. script | folder contains python scripts. Now the main script for generate robot is in this folder

7. urdf  | folder contains script generated xacro and urdf files

8. urdf.rviz  | an rviz config file to display robot in rviz. It will be automatically read and used by launch/rviz\_test.launch

After package "eigenbot" is correctly configured(especially after the "source YOUR\_ROS\_WORKSPACE/devel/setup.bash" is executed). Following commands below can be used to start rviz, MoveIt, and gazebo.

There will be a program, run when the robot is turned on, which takes all the module arragement info, and copies the urdf onboard each module, and assembles them into a single full robot urdf which can be then dropped into Gazebo, RViz, etc.
The current xacro writer is in folder script description_assembler.py generates autoXACRO.xacro along with a variety of other config files.

