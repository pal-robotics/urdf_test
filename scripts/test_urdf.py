#!/usr/bin/env python3
# Copyright (c) 2022 PAL Robotics S.L. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy
from rclpy.qos import QoSProfile


from std_msgs.msg import String


class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('robot_description_subscriber')
        self.robot_description_received = False

        qos_profile = QoSProfile(
            depth=1,
            durability=DurabilityPolicy.TRANSIENT_LOCAL)
        self.subscription = self.create_subscription(
            String,
            'robot_description',
            self.listener_callback,
            qos_profile)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('Received robot_description')
        print('Received robot_description')
        self.robot_description_received = True


def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    while not minimal_subscriber.robot_description_received:
        rclpy.spin_once(minimal_subscriber)

    rclpy.shutdown()
    exit(0)


if __name__ == '__main__':
    main()
