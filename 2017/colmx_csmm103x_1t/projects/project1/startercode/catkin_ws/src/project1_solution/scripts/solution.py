#!/usr/bin/env python  
import rospy

from std_msgs.msg import Int16
from project1_solution.msg import TwoInts

def callback(twoints, publisher):
    rospy.loginfo(rospy.get_caller_id() + '%d+%d=%d' % (twoints.a, twoints.b,twoints.a + twoints.b))
    publisher.publish(twoints.a + twoints.b)

def subscriber_setup(publisher):
    rospy.Subscriber('two_ints', TwoInts, callback, callback_args=publisher)

def sum_publisher():
    pub = rospy.Publisher('sum', Int16, queue_size=10)
    return pub
    

if __name__ == '__main__':
    try:

        # initialization setup
        rospy.init_node('two_ints_subscribe_publish_sum', anonymous=True)
        rate = rospy.Rate(0.5) 

        publisher = sum_publisher()
        subscriber_setup(publisher)

        # spin() simply keeps python from exiting until this node is stopped
        rospy.spin()

    except rospy.ROSInterruptException:
        pass

    
