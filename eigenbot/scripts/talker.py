#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String

def talker():
    pub = rospy.Publisher('/eigenbot/topology', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(1) # hz
    while not rospy.is_shutdown():
        time_now = rospy.get_rostime().secs  
        #hello_str = "hello world %s" % str(time_now)[:-1]      
	   #hello_str = "hello world %s" % rospy.get_time()

# random test robot
        # message_str = '''{"id": "2B", "type": "8", "orientation": "1", "children": ["01", "3A", "FF", "3B", "3C", "3D" , "FF"]},
        #      {"id": "01", "type": "3", "orientation": "1", "children": ["02"]}, 
        #      {"id": "02", "type": "3", "orientation": "1", "children": ["03"]}, 
        #      {"id": "03", "type": "10", "orientation": "1", "children": ["FF"]}, 
        #      {"id": "3A", "type": "3", "orientation": "5", "children": ["42", "FF"]}, 
        #      {"id": "42", "type": "1", "orientation": "1", "children": ["FF", "FF"]}, 
        #      {"id": "3B", "type": "3", "orientation": "5", "children": ["43", "FF"]}, 
        #      {"id": "43", "type": "1", "orientation": "5", "children": ["FF", "FF"]}, 
        #      {"id": "3C", "type": "3", "orientation": "5", "children": ["44", "FF"]}, 
        #      {"id": "44", "type": "1", "orientation": "1", "children": ["FF", "FF"]}, 
        #      {"id": "3D", "type": "3", "orientation": "5", "children": ["45", "FF"]}, 
        #      {"id": "45", "type": "1", "orientation": "5", "children": ["FF", "FF"]}'''

# hexapod
        # message_str = '''{"id": "00", "type": "8", "orientation": "1", 
        #             "children": ["11", "21", "31", "41", "51", "61", "FF"]},
        #       {"id": "11", "type": "3", "orientation": "1", "children": ["12"]}, 
        #      {"id": "12", "type": "3", "orientation": "3", "children": ["0D"]}, 
        #      {"id": "0D", "type": "3", "orientation": "1", "children": ["1A"]}, 
        #      {"id": "1A", "type": "0D", "orientation": "5", "children": ["1B"]}, 
        #      {"id": "1B", "type": "10", "orientation": "1", "children": ["FF"]}, 
        #       {"id": "21", "type": "3", "orientation": "1", "children": ["22"]}, 
        #      {"id": "22", "type": "3", "orientation": "3", "children": ["23"]}, 
        #      {"id": "23", "type": "3", "orientation": "1", "children": ["2A"]}, 
        #      {"id": "2A", "type": "0D", "orientation": "5", "children": ["2B"]}, 
        #      {"id": "2B", "type": "10", "orientation": "1", "children": ["FF"]}, 
        #       {"id": "31", "type": "3", "orientation": "1", "children": ["32"]}, 
        #      {"id": "32", "type": "3", "orientation": "3", "children": ["33"]}, 
        #      {"id": "33", "type": "3", "orientation": "1", "children": ["3A"]}, 
        #      {"id": "3A", "type": "0D", "orientation": "5", "children": ["3B"]}, 
        #      {"id": "3B", "type": "10", "orientation": "1", "children": ["FF"]}, 
        #       {"id": "41", "type": "3", "orientation": "1", "children": ["42"]}, 
        #      {"id": "42", "type": "3", "orientation": "3", "children": ["43"]}, 
        #      {"id": "43", "type": "3", "orientation": "1", "children": ["4A"]}, 
        #      {"id": "4A", "type": "0D", "orientation": "1", "children": ["4B"]}, 
        #      {"id": "4B", "type": "10", "orientation": "1", "children": ["FF"]}, 
        #       {"id": "51", "type": "3", "orientation": "1", "children": ["52"]}, 
        #      {"id": "52", "type": "3", "orientation": "3", "children": ["53"]}, 
        #      {"id": "53", "type": "3", "orientation": "1", "children": ["5A"]}, 
        #      {"id": "5A", "type": "0D", "orientation": "1", "children": ["5B"]}, 
        #      {"id": "5B", "type": "10", "orientation": "1", "children": ["FF"]}, 
        #       {"id": "61", "type": "3", "orientation": "1", "children": ["62"]}, 
        #      {"id": "62", "type": "3", "orientation": "3", "children": ["63"]}, 
        #      {"id": "63", "type": "3", "orientation": "1", "children": ["6A"]},
        #      {"id": "6A", "type": "0D", "orientation": "1", "children": ["6B"]}, 
        #      {"id": "6B", "type": "10", "orientation": "1", "children": ["FF"]}'''

# car
        message_str = '''{"id": "00", "type": "8", "orientation": "1", 
                    "children": ["11", "FF", "31", "41", "FF", "61", "FF"]},
             {"id": "11", "type": "1", "orientation": "1", "children": ["FF"]}, 
             {"id": "31", "type": "1", "orientation": "1", "children": ["FF"]},
             {"id": "41", "type": "1", "orientation": "5", "children": ["FF"]},
             {"id": "61", "type": "1", "orientation": "5", "children": ["FF"]}'''

# car with gripper
        message_str = '''{"id": "00", "type": "8", "orientation": "1", 
                    "children": ["11", "FF", "31", "41", "FF", "61", "71"]},
             {"id": "11", "type": "1", "orientation": "1", "children": ["FF"]}, 
             {"id": "31", "type": "1", "orientation": "1", "children": ["FF"]},
             {"id": "41", "type": "1", "orientation": "5", "children": ["FF"]},
             {"id": "61", "type": "1", "orientation": "5", "children": ["FF"]},
             {"id": "71", "type": "0D", "orientation": "1", "children": ["72"]},
             {"id": "72", "type": "3", "orientation": "1", "children": ["73"]},
             {"id": "73", "type": "5", "orientation": "3", "children": ["FF"]}'''


# hexapod, no 90 deg
        message_str = '''{"id": "00", "type": "8", "orientation": "1", 
                    "children": ["11", "21", "31", "41", "51", "61", "FF"]},
              {"id": "11", "type": "3", "orientation": "1", "children": ["12"]}, 
             {"id": "12", "type": "3", "orientation": "3", "children": ["0D"]}, 
             {"id": "0D", "type": "3", "orientation": "1", "children": ["1B"]}, 
             {"id": "1B", "type": "10", "orientation": "1", "children": ["FF"]}, 
              {"id": "21", "type": "3", "orientation": "1", "children": ["22"]}, 
             {"id": "22", "type": "3", "orientation": "3", "children": ["23"]}, 
             {"id": "23", "type": "3", "orientation": "1", "children": ["2B"]}, 
             {"id": "2B", "type": "10", "orientation": "1", "children": ["FF"]}, 
              {"id": "31", "type": "3", "orientation": "1", "children": ["32"]}, 
             {"id": "32", "type": "3", "orientation": "3", "children": ["33"]}, 
             {"id": "33", "type": "3", "orientation": "1", "children": ["3B"]}, 
             {"id": "3B", "type": "10", "orientation": "1", "children": ["FF"]}, 
              {"id": "41", "type": "3", "orientation": "1", "children": ["42"]}, 
             {"id": "42", "type": "3", "orientation": "3", "children": ["43"]}, 
             {"id": "43", "type": "3", "orientation": "1", "children": ["4B"]}, 
             {"id": "4B", "type": "10", "orientation": "1", "children": ["FF"]}, 
              {"id": "51", "type": "3", "orientation": "1", "children": ["52"]}, 
             {"id": "52", "type": "3", "orientation": "3", "children": ["53"]}, 
             {"id": "53", "type": "3", "orientation": "1", "children": ["5B"]}, 
             {"id": "5B", "type": "10", "orientation": "1", "children": ["FF"]}, 
              {"id": "61", "type": "3", "orientation": "1", "children": ["62"]}, 
             {"id": "62", "type": "3", "orientation": "3", "children": ["63"]}, 
             {"id": "63", "type": "3", "orientation": "1", "children": ["6B"]},
             {"id": "6B", "type": "10", "orientation": "1", "children": ["FF"]}'''

# test robot
        # message_str = '''{"id": "8C", "type": "1", "orientation": "0", "children": ["FF", "FF", "FF"]},
        #    {"id": "06", "type": "1", "orientation": "0", "children": ["FF", "FF", "FF"]},
        #    {"id": "E0", "type": "3", "orientation": "0", "children": ["FF", "FF", "FF"]},
        #    {"id": "00", "type": "14", "orientation": "0", "children": ["FF", "5A", "FF", "8C", "06", "FF", "0B", "FF"]},
        #    {"id": "5A", "type": "3", "orientation": "0", "children": ["05", "FF", "FF"]},
        #    {"id": "0B", "type": "3", "orientation": "0", "children": ["E0", "FF", "FF"]},
        #    {"id": "BB", "type": "0D", "orientation": "0", "children": ["C0", "FF", "FF"]},
        #    {"id": "C0", "type": "3", "orientation": "0", "children": ["29", "FF", "FF"]},
        #    {"id": "29", "type": "0", "orientation": "0", "children": ["FF", "FF", "FF"]},
        #    {"id": "05", "type": "2", "orientation": "0", "children": ["BB", "FF", "FF"]},'''

# message from actual car

        message_str = '''
          {"id": "07", "type": "1", "orientation": "1", "children": ["FF", "FF", "FF"]},
          {"id": "8C", "type": "1", "orientation": "1", "children": ["FF", "FF", "FF"]},
          {"id": "06", "type": "1", "orientation": "5", "children": ["FF", "FF", "FF"]},
          {"id": "D2", "type": "1", "orientation": "5", "children": ["FF", "FF", "FF"]},
          {"id": "00", "type": "08", "orientation": "0", "children": ["FF", "07", "FF", "8C", "06", "FF", "D2", "FF"]},'''

        # message from actual lwl
        # message_str = '''
        #   {"id": "06", "type": "1", "orientation": "0", "children": ["FF","FF", "FF"]},
        #   {"id": "B4", "type": "0D", "orientation": "0", "children": ["FF", "FF", "FF"]},
        #   {"id": "C7", "type": "10", "orientation": "0", "children": ["FF", "FF", "FF"]},
        #   {"id": "42", "type": "10", "orientation": "0", "children": ["FF", "FF", "FF"]},
        #   {"id": "29", "type": "0", "orientation": "0", "children": ["FF", "FF", "FF"]},
        #   {"id": "0B", "type": "3", "orientation": "0", "children": ["E0", "FF", "FF"]},
        #   {"id": "36", "type": "2", "orientation": "0", "children": ["88", "FF", "FF"]},
        #   {"id": "04", "type": "2", "orientation": "0", "children": ["01", "FF", "FF"]},
        #   {"id": "5A", "type": "3", "orientation": "0", "children": ["05", "FF", "FF"]},
        #   {"id": "E0", "type": "3", "orientation": "0", "children": ["E9", "FF", "FF"]},
        #   {"id": "88", "type": "2", "orientation": "0", "children": ["0C", "FF", "FF"]},
        #   {"id": "01", "type": "2", "orientation": "0", "children": ["03", "FF", "FF"]},
        #   {"id": "03", "type": "2", "orientation": "0", "children": ["47", "FF", "FF"]},
        #   {"id": "C0", "type": "3", "orientation": "0", "children": ["BB", "FF", "FF"]},
        #   {"id": "B6", "type": "0D", "orientation": "0", "children": ["C7", "FF", "FF"]},
        #   {"id": "47", "type": "0D", "orientation": "0", "children": ["42", "FF", "FF"]},
        #   {"id": "BB", "type": "0D", "orientation": "0", "children": ["29", "FF", "FF"]},
        #   {"id": "00", "type": "14", "orientation": "0", "children": ["FF", "0B", "FF", "36", "04", "06", "5A", "FF"]},
        #   {"id": "05", "type": "2", "orientation": "0", "children": ["C0", "FF", "FF"]},
        #   {"id": "E9", "type": "2", "orientation": "0", "children": ["B6", "FF", "FF"]},
        #   {"id": "0C", "type": "3", "orientation": "0", "children": ["B4", "FF", "FF"]},'''
# message from actual lwl
        message_str = '''
          {"id": "06", "type": "1", "orientation": "0", "children": ["FF",   "FF", "FF"]},
          {"id": "B4", "type": "0D", "orientation": "0", "children": ["FF", "FF", "FF"]},
          {"id": "C7", "type": "10", "orientation": "0", "children": ["FF", "FF", "FF"]},
          {"id": "42", "type": "10", "orientation": "0", "children": ["FF", "FF", "FF"]},
          {"id": "29", "type": "0", "orientation": "0", "children": ["FF", "FF", "FF"]},
          {"id": "0B", "type": "3", "orientation": "0", "children": ["E0", "FF", "FF"]},
          {"id": "36", "type": "2", "orientation": "0", "children": ["88", "FF", "FF"]},
          {"id": "04", "type": "2", "orientation": "0", "children": ["01", "FF", "FF"]},
          {"id": "5A", "type": "3", "orientation": "0", "children": ["05", "FF", "FF"]},
          {"id": "E0", "type": "3", "orientation": "0", "children": ["E9", "FF", "FF"]},
          {"id": "88", "type": "2", "orientation": "0", "children": ["0C", "FF", "FF"]},
          {"id": "01", "type": "2", "orientation": "0", "children": ["03", "FF", "FF"]},
          {"id": "03", "type": "2", "orientation": "0", "children": ["47", "FF", "FF"]},
          {"id": "C0", "type": "3", "orientation": "0", "children": ["BB", "FF", "FF"]},
          {"id": "B6", "type": "0D", "orientation": "0", "children": ["C7", "FF", "FF"]},
          {"id": "47", "type": "0D", "orientation": "0", "children": ["42", "FF", "FF"]},
          {"id": "BB", "type": "0D", "orientation": "0", "children": ["29", "FF", "FF"]},
          {"id": "00", "type": "08", "orientation": "0", "children": ["FF", "0B", "FF", "36", "04", "06", "5A", "FF"]},
          {"id": "05", "type": "2", "orientation": "0", "children": ["C0", "FF", "FF"]},
          {"id": "E9", "type": "2", "orientation": "0", "children": ["B6", "FF", "FF"]},
          {"id": "0C", "type": "3", "orientation": "0", "children": ["B4", "FF", "FF"]},'''

        # hand-corrected, from actual lwl
        message_str = '''
          {"id": "06", "type": "1", "orientation": "0", "children": ["FF",   "FF", "FF"]},
          {"id": "B4", "type": "0D", "orientation": "0", "children": ["FF", "FF", "FF"]},
          {"id": "C7", "type": "10", "orientation": "0", "children": ["FF", "FF", "FF"]},
          {"id": "42", "type": "10", "orientation": "0", "children": ["FF", "FF", "FF"]},
          {"id": "29", "type": "10", "orientation": "0", "children": ["FF", "FF", "FF"]},
          {"id": "0B", "type": "3", "orientation": "0", "children": ["E0", "FF", "FF"]},
          {"id": "36", "type": "3", "orientation": "0", "children": ["88", "FF", "FF"]},
          {"id": "04", "type": "3", "orientation": "0", "children": ["01", "FF", "FF"]},
          {"id": "5A", "type": "3", "orientation": "0", "children": ["05", "FF", "FF"]},
          {"id": "E0", "type": "3", "orientation": "0", "children": ["E9", "FF", "FF"]},
          {"id": "88", "type": "3", "orientation": "0", "children": ["0C", "FF", "FF"]},
          {"id": "01", "type": "3", "orientation": "0", "children": ["03", "FF", "FF"]},
          {"id": "03", "type": "3", "orientation": "0", "children": ["47", "FF", "FF"]},
          {"id": "C0", "type": "3", "orientation": "0", "children": ["BB", "FF", "FF"]},
          {"id": "B6", "type": "0D", "orientation": "0", "children": ["C7", "FF", "FF"]},
          {"id": "47", "type": "0D", "orientation": "0", "children": ["42", "FF", "FF"]},
          {"id": "BB", "type": "0D", "orientation": "0", "children": ["29", "FF", "FF"]},
          {"id": "00", "type": "08", "orientation": "0", "children": ["FF", "0B", "FF", "36", "04", "06", "5A", "FF"]},
          {"id": "05", "type": "3", "orientation": "0", "children": ["C0", "FF", "FF"]},
          {"id": "E9", "type": "3", "orientation": "0", "children": ["B6", "FF", "FF"]},
          {"id": "0C", "type": "3", "orientation": "0", "children": ["B4", "FF", "FF"]},'''

# hexapod car
        # message_str = '''{"id": "00", "type": "8", "orientation": "1", 
        #             "children": ["11", "21", "31", "41", "51", "61", "FF"]},
        #       {"id": "11", "type": "3", "orientation": "1", "children": ["12"]}, 
        #      {"id": "12", "type": "3", "orientation": "3", "children": ["0D"]}, 
        #      {"id": "0D", "type": "3", "orientation": "1", "children": ["1A"]}, 
        #      {"id": "1A", "type": "0D", "orientation": "5", "children": ["1B"]}, 
        #      {"id": "1B", "type": "10", "orientation": "1", "children": ["FF"]}, 
        #       {"id": "21", "type": "3", "orientation": "1", "children": ["22"]}, 
        #      {"id": "22", "type": "3", "orientation": "3", "children": ["23"]}, 
        #      {"id": "23", "type": "3", "orientation": "1", "children": ["2A"]}, 
        #      {"id": "2A", "type": "0D", "orientation": "5", "children": ["2B"]}, 
        #      {"id": "2B", "type": "10", "orientation": "1", "children": ["FF"]}, 
        #         {"id": "31", "type": "1", "orientation": "8", "children": ["FF"]},
        #       {"id": "41", "type": "3", "orientation": "1", "children": ["42"]}, 
        #      {"id": "42", "type": "3", "orientation": "3", "children": ["43"]}, 
        #      {"id": "43", "type": "3", "orientation": "1", "children": ["4A"]}, 
        #      {"id": "4A", "type": "0D", "orientation": "1", "children": ["4B"]}, 
        #      {"id": "4B", "type": "10", "orientation": "1", "children": ["FF"]}, 
        #       {"id": "51", "type": "3", "orientation": "1", "children": ["52"]}, 
        #      {"id": "52", "type": "3", "orientation": "3", "children": ["53"]}, 
        #      {"id": "53", "type": "3", "orientation": "1", "children": ["5A"]}, 
        #      {"id": "5A", "type": "0D", "orientation": "1", "children": ["5B"]}, 
        #      {"id": "5B", "type": "10", "orientation": "1", "children": ["FF"]}, 
        #         {"id": "61", "type": "1", "orientation": "6", "children": ["FF"]}'''
# real hexapod from Nick 11/12/2020
# types: 0A=foot, 0E=body, 03=bendy, 0D=static90
        # message_str = '''
        # {"id": "29", "type": "0A", "orientation": "01", "children": ["FF", "FF", "FF"]},
        # {"id": "5B", "type": "0A", "orientation": "01", "children": ["FF", "FF", "FF"]},
        # {"id": "C5", "type": "0A", "orientation": "01", "children": ["FF", "FF", "FF"]},
        # {"id": "C7", "type": "0A", "orientation": "01", "children": ["FF", "FF", "FF"]},
        # {"id": "42", "type": "0A", "orientation": "01", "children": ["FF", "FF", "FF"]},
        # {"id": "8E", "type": "0A", "orientation": "01", "children": ["FF", "FF", "FF"]},
        # {"id": "00", "type": "0E", "orientation": "00", "children": ["C0", "05", "B9", "5A", "02", "04", "FF", "FF"]},
        # {"id": "C0", "type": "03", "orientation": "00", "children": ["0C", "FF", "FF"]},
        # {"id": "05", "type": "03", "orientation": "00", "children": ["79", "FF", "FF"]},
        # {"id": "B9", "type": "03", "orientation": "00", "children": ["03", "FF", "FF"]},
        # {"id": "5A", "type": "03", "orientation": "00", "children": ["E9", "FF", "FF"]},
        # {"id": "02", "type": "03", "orientation": "00", "children": ["1D", "FF", "FF"]},
        # {"id": "04", "type": "03", "orientation": "00", "children": ["66", "FF", "FF"]},
        # {"id": "0C", "type": "03", "orientation": "03", "children": ["BB", "FF", "FF"]},
        # {"id": "79", "type": "03", "orientation": "03", "children": ["C6", "FF", "FF"]},
        # {"id": "03", "type": "03", "orientation": "03", "children": ["B4", "FF", "FF"]},
        # {"id": "E9", "type": "03", "orientation": "03", "children": ["B6", "FF", "FF"]},
        # {"id": "1D", "type": "03", "orientation": "03", "children": ["47", "FF", "FF"]},
        # {"id": "66", "type": "03", "orientation": "03", "children": ["F9", "FF", "FF"]},
        # {"id": "BB", "type": "0D", "orientation": "07", "children": ["36", "FF", "FF"]},
        # {"id": "C6", "type": "0D", "orientation": "07", "children": ["0B", "FF", "FF"]},
        # {"id": "B4", "type": "0D", "orientation": "07", "children": ["0A", "FF", "FF"]},
        # {"id": "B6", "type": "0D", "orientation": "07", "children": ["01", "FF", "FF"]},
        # {"id": "47", "type": "0D", "orientation": "07", "children": ["53", "FF", "FF"]},
        # {"id": "F9", "type": "0D", "orientation": "07", "children": ["88", "FF", "FF"]},
        # {"id": "36", "type": "03", "orientation": "03", "children": ["29", "FF", "FF"]},
        # {"id": "0B", "type": "03", "orientation": "03", "children": ["5B", "FF", "FF"]},
        # {"id": "0A", "type": "03", "orientation": "03", "children": ["C5", "FF", "FF"]},
        # {"id": "01", "type": "03", "orientation": "03", "children": ["C7", "FF", "FF"]},
        # {"id": "53", "type": "03", "orientation": "03", "children": ["42", "FF", "FF"]},
        # {"id": "88", "type": "03", "orientation": "03", "children": ["8E", "FF", "FF"]},'''

# real hexapod from Nick 11/16/2020
# types: 0A=foot, 0E=body, 03=bendy, 0D=static90
        message_str = '''
            {"id": "29", "type": "0A", "orientation": "01", "children": ["FF", "FF", "FF"]},
            {"id": "5B", "type": "0A", "orientation": "01", "children": ["FF", "FF", "FF"]},
            {"id": "C5", "type": "0A", "orientation": "01", "children": ["FF", "FF", "FF"]},
            {"id": "C7", "type": "0A", "orientation": "01", "children": ["FF", "FF", "FF"]},
            {"id": "42", "type": "0A", "orientation": "01", "children": ["FF", "FF", "FF"]},
            {"id": "8E", "type": "0A", "orientation": "01", "children": ["FF", "FF", "FF"]},
            {"id": "00", "type": "0E", "orientation": "00", "children": ["C0", "05", "B9", "5A", "02", "04", "FF", "FF"]},
            {"id": "C0", "type": "03", "orientation": "01", "children": ["0C", "FF", "FF"]},
            {"id": "05", "type": "03", "orientation": "01", "children": ["79", "FF", "FF"]},
            {"id": "B9", "type": "03", "orientation": "01", "children": ["03", "FF", "FF"]},
            {"id": "5A", "type": "03", "orientation": "01", "children": ["E9", "FF", "FF"]},
            {"id": "02", "type": "03", "orientation": "01", "children": ["1D", "FF", "FF"]},
            {"id": "04", "type": "03", "orientation": "01", "children": ["66", "FF", "FF"]},
            {"id": "0C", "type": "03", "orientation": "03", "children": ["BB", "FF", "FF"]},
            {"id": "79", "type": "03", "orientation": "03", "children": ["C6", "FF", "FF"]},
            {"id": "03", "type": "03", "orientation": "03", "children": ["B4", "FF", "FF"]},
            {"id": "E9", "type": "03", "orientation": "03", "children": ["B6", "FF", "FF"]},
            {"id": "1D", "type": "03", "orientation": "03", "children": ["47", "FF", "FF"]},
            {"id": "66", "type": "03", "orientation": "03", "children": ["F9", "FF", "FF"]},
            {"id": "BB", "type": "0D", "orientation": "07", "children": ["36", "FF", "FF"]},
            {"id": "C6", "type": "0D", "orientation": "07", "children": ["0B", "FF", "FF"]},
            {"id": "B4", "type": "0D", "orientation": "07", "children": ["0A", "FF", "FF"]},
            {"id": "B6", "type": "0D", "orientation": "07", "children": ["01", "FF", "FF"]},
            {"id": "47", "type": "0D", "orientation": "07", "children": ["53", "FF", "FF"]},
            {"id": "F9", "type": "0D", "orientation": "07", "children": ["88", "FF", "FF"]},
            {"id": "0B", "type": "03", "orientation": "03", "children": ["5B", "FF", "FF"]},
            {"id": "0A", "type": "03", "orientation": "03", "children": ["C5", "FF", "FF"]},
            {"id": "01", "type": "03", "orientation": "03", "children": ["C7", "FF", "FF"]},
            {"id": "53", "type": "03", "orientation": "03", "children": ["42", "FF", "FF"]},
            {"id": "88", "type": "03", "orientation": "03", "children": ["8E", "FF", "FF"]},
            {"id": "36", "type": "03", "orientation": "03", "children": ["29", "FF", "FF"]},'''


        rospy.loginfo(message_str)
        pub.publish(message_str)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass


#Created on Sun May 12 10:48:59 2019
#by Julian Whitman
#
#This file publishes fake assembly info for testing purposes.

# based on  http://wiki.ros.org/ROS/Tutorials/WritingPublisherSubscriber%28python%29
# note: make sure to run chmod +x talker.py first to make it executable
# license removed for brevity
