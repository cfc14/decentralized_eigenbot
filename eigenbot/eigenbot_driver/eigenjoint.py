#!/usr/bin/env python
#
# Software License Agreement (BSD License)
#
# Copyright (c) 2019, Charles Hart
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following
# disclaimer in the documentation and/or other materials provided
# with the distribution.
# * Neither the names of the authors nor the names of their
# affiliated organizations may be used to endorse or promote products derived
# from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import rospy
from std_msgs.msg import String
from control_msgs.msg import JointJog
from sensor_msgs.msg import JointState

VERSION="0.1a"

class eigen_joints():
  def __init__(self):
    rospy.init_node('eigen_joints')
    self.jsPub = rospy.Publisher('eigenbot/joint_states', JointState, queue_size=1)

    rospy.Subscriber('joint_states', JointState, self.eigenJSCB)

    self.serialPub = rospy.Publisher('eigenbot/in', String, queue_size=1)

    off1 = rospy.get_param('~off1',0)
    off2 = rospy.get_param('~off2',0)
    off3 = rospy.get_param('~off3',0)
    off4 = rospy.get_param('~off4',0)
    self.offsets = [off1, off2, off3, off4]

    print("EigenBot Joint Controller v{} running.".format(VERSION))
    print("Ready to accept commands on {}, reporting on {}."
          .format('joint_states', 'eigenbot/joint_states'))

  def eigenJSCB(self, msg):
    commands = msg.position
    print("got pos:{} for {}".format(msg.position, msg.name))
    mod_ids = ['0'+x[-3] for x in msg.name]
    for i in range(len(commands)):
      if "bendy" in msg.name[i]:
        k_ratio = (4096 * -1) / (2 * 3.141592653589)
      else:
        k_ratio = (4096 * 4) / (2 * 3.141592653589)
      pos = int(k_ratio * commands[i]) + self.offsets[i]
      pos_cmd = mod_ids[i] + "P" + str(pos) + "R\n"
      print("Sending {}".format(pos_cmd))
      self.serialPub.publish(String(pos_cmd))
    

  def eigenJogCB(self, msg):
    pass
    #print("got cmd msg \"{}\"".format(msg))
    

  def run(self):
    while not rospy.is_shutdown():
      pass

if __name__ == "__main__":
  joints = eigen_joints()
  joints.run()

#eof
