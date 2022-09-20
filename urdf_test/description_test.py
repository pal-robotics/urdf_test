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

import os
import unittest

from launch import LaunchDescription
from launch_ros.actions import Node
import launch_testing


def generate_urdf_test_description(launch_file_action):
    # This is necessary to get unbuffered output from the process under test
    proc_env = os.environ.copy()
    proc_env['PYTHONUNBUFFERED'] = '1'

    # dut = device under test, aka the actual test
    dut_process = Node(package='urdf_test',
                       executable='test_urdf.py',
                       output='both',
                       env=proc_env,)
    return LaunchDescription([
        launch_file_action,
        dut_process,

        launch_testing.actions.ReadyToTest(),
    ]), {'dut_process': dut_process}


class TestDescriptionPublished(unittest.TestCase):

    def test_robot_description_output(self, proc_output, proc_info, dut_process):
        # This will match stderr from dut_process
        # stderr seems to be used even by rclpy.loginfo(), stdout will fail and not find anything

        proc_output.assertWaitFor(
            'Received robot_description', timeout=3, stream='stderr', process=dut_process)

        # Wait until process ends
        proc_info.assertWaitForShutdown(process=dut_process, timeout=2)


@launch_testing.post_shutdown_test()
class TestSuccessfulExit(unittest.TestCase):

    def test_exit_code(self, proc_info, dut_process):
        # Check that dut_process finishes with code 0
        launch_testing.asserts.assertExitCodes(proc_info, process=dut_process)
