import time
from math import sin, pi
import numpy as np
import matplotlib.pyplot as plt
import rospy
from sensor_msgs.msg import JointState
def wave(): #period, amplitude, y_offset, x_offset=0):
  period = 2
  amplitude = 1.5 #10000
  offset = 3.14159 #-2000
  period2 = 2
  amplitude2 = 1.5 #5000 
  offset2 = 3.14159 #-2000
  t_start = time.time()
  rospy.init_node('scripted_motion')
  rate = rospy.Rate(100)
  pub = rospy.Publisher('titan/joint', JointState, queue_size=1)  
  while not rospy.is_shutdown():
      t_now = time.time()
      t_elapsed= time.time() - t_start      
      set_pos = offset + amplitude * sin((2.0*pi*t_elapsed)/period)
      #s.write(bytes("01P{}R\n".format(set_pos).encode("ascii")))
      #plt.scatter(t_now, set_pos, c='red', marker='o')      
      set_pos2 = offset2 + amplitude2 * sin((2.0*pi*t_elapsed)/period2)
      #s.write(bytes("03P{}R\n".format(set_pos2).encode("ascii")))
      #plt.scatter(t_now, set_pos2, c='blue', marker='o')      
      js = JointState()
      js.name = ['0A', '0B']
      js.position = [set_pos, set_pos2]
      js.velocity = [float('nan'), float('nan')]
      js.effort = [float('nan'), float('nan')]
      pub.publish(js)      #plt.draw()
      #plt.pause(0.005)
      #time.sleep(0.005)
      rate.sleep()

if __name__ == "__main__":
  wave()