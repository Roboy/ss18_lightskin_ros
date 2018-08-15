#!/usr/bin/python

#python 3.6 is used

# importing Daniel's modules
#import sys
#print(sys.version)

import rospy
import numpy as np

from std_msgs.msg import Float32MultiArray
from std_msgs.msg import MultiArrayDimension

from threading import Thread


class myThread(Thread):
    #reconstruction_data_array = []
    reconstruction_data_array = np.arange(100).reshape((10, 10))

    def __init__(self):
        Thread.__init__(self, target=self.update_reconstruction_data_array, daemon=True)
        #self.reconstruction_data_array = np.arange(100).reshape((10, 10))

    def update_reconstruction_data_array(self):
        pass  # reconstruction_data_array should be numpy array


def main():
    thread1 = myThread()
    thread1.start()

    rospy.init_node('reconstruction_node', anonymous=True)  # node_name: reconstruction_node
    pub = rospy.Publisher('topic_name', Float32MultiArray, queue_size=10)    # topic_name: topic_name
    instance_multi_array = Float32MultiArray()

    instance_multi_array.layout.data_offset = 0

    temp_a = MultiArrayDimension()
    temp_b = MultiArrayDimension()

    temp_a.label = 'LED'
    temp_a.size = np.size(thread1.reconstruction_data_array, 0)
    temp_a.stride = np.size(thread1.reconstruction_data_array, 1) * np.size(thread1.reconstruction_data_array, 0)

    temp_b.label = 'Sensor'
    temp_b.size = np.size(thread1.reconstruction_data_array, 1)
    temp_b.stride = 1 * np.size(thread1.reconstruction_data_array, 1)

    instance_multi_array.layout.dim.append(temp_a)
    instance_multi_array.layout.dim.append(temp_b)

    temp_c = np.reshape(thread1.reconstruction_data_array, (1, thread1.reconstruction_data_array.size), 'C')

    instance_multi_array.data = temp_c[0]

    rate = rospy.Rate(1)

    rospy.loginfo("Node_Publishes")

    while not rospy.is_shutdown():
        # rospy.loginfo(instance_multi_array)
        pub.publish(instance_multi_array)
        rate.sleep()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
