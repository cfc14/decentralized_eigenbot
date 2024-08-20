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
import serial, struct

VERSION="0.1a"

class eigenbot_driver():
  def __init__(self):
    rospy.init_node('eigenbot_driver')
    self.treePub = rospy.Publisher('eigenbot/out', String, queue_size=1)

    eigenPort = rospy.get_param('~port', '/dev/ttyUSB0')
    eigenBaud = rospy.get_param('~baud', 115200)
    self.eigenSerial = serial.Serial(port=eigenPort, baudrate=eigenBaud, timeout=1.0)

    rospy.Subscriber('eigenbot/in', String, self.eigenCmdCB)

    print("EigenBot Driver v{} running.".format(VERSION))
    print("Connected to {} port at {} baud.".format(eigenPort, eigenBaud))
    print("Ready to accept commands on {}, responding on {}."
          .format('eigenbot/in', 'eigenbot/out'))

  def eigenCmdCB(self, msg):
    #print("got cmd msg \"{}\"".format(msg))
    if msg.data[-1] != '\n':
      msg.data += '\n'
    self.eigenSerial.write(msg.data)

  def run(self):
    while not rospy.is_shutdown():
      line = self.eigenSerial.readline()
      if len(line) > 0:
        #print("{}: got {}, {}".format(rospy.Time.now(), len(line), line))
        self.treePub.publish(String(line[:-1]))

if __name__ == "__main__":
  driver = eigenbot_driver()
  driver.run()

#eof
