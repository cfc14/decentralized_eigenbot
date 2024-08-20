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
from time import sleep

VERSION="0.1a"

class Node():
  def __init__(self, _id, _type, _orient):
    self.id = _id
    self.type = _type
    self.orient = _orient 
    self.children = []
  

class eigen_topology():
  def __init__(self):
    rospy.init_node('eigen_topology')
    # publish a string like id@orient:(id_a@orient:(id_a_a@orient:(),()),(id_a_b@orient:(),())),()
    self.topoPub = rospy.Publisher('eigenbot/topology', String, queue_size=1)
    
    # serial string message interface
    self.serialPub = rospy.Publisher('eigenbot/in', String, queue_size=1)
    rospy.Subscriber('eigenbot/out', String, self.eigenBusCB)

    wait_time = rospy.get_param('~wait',10)

    self.topology = {}
    self.nodes = []
    self.topostring = ""

    print("EigenBot Topology Mapper Tool v{} running.".format(VERSION))
    print("Ready to query eigenbot modules on {}, listen on {}, report on {}."
          .format('eigenbot/in', 'eigenbot/out', 'eigenbot/topology'))
    for i in range(wait_time, 0, -1):
      print("{}...".format(i))
      sleep(1)


  def stringify(self):
    s = ""
    for node in self.topology:
      # check for the children of each node in the topology
      child_a = self.topology[node][2]
      child_b = self.topology[node][3]
      if child_a and child_a in self.topology:
        s += child_a
        print("{} is a child of {}".format(child_a, node))
      if child_b and child_b in self.topology:
        s += child_b
        print("{} is a child of {}".format(child_b, node))
    return s + "TODO - make a single stringified tree of nodes"


  def eigenBusCB(self, msg):
    print("got msg data {} \"{}\"".format(len(msg.data), msg.data))
    # check for topology status messages
    if msg.data[0] == '.' and msg.data[3] == 'S' and len(msg.data) > 6: 
      # Get the ID, orientation, type, and children of each module.
      eigen_id = msg.data[1:3]
      mod_type = msg.data[4]
      orient = msg.data[6]
      child_a = msg.data[8:10]
      child_b = msg.data[11:13]

      self.topology[eigen_id] = ('type', orient, child_a, child_b)
      if len(msg.data) == 13 and msg.data not in self.topostring:
        self.topostring += msg.data

    if msg.data[0] == 'H' and msg.data[1:3] not in self.topology:
      self.topostring = ""
      eigen_id = msg.data[1:3]
      self.topology[eigen_id] = ('type', 'orient', 'child_a', 'child_b')
        
    
    
  def run(self):
    while not rospy.is_shutdown():
      # request topology status every 3 seconds
      self.serialPub.publish(String("FFO\n")) 

      # publish the topology
      if len(self.topostring) > 0:
        self.topoPub.publish(String(self.topostring))

      rospy.sleep(3.)

      # TODO: periodically remove disconnected or non-responsive modules


if __name__ == "__main__":
  topo = eigen_topology()
  topo.run()

#eof
