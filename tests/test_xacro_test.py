# Copyright (c) 2024 PAL Robotics S.L. All rights reserved.
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

import subprocess
import tempfile

import pytest
import xacro

from launch.actions import DeclareLaunchArgument
from urdf_test.xacro_test import (check_urdf,
                                  check_xacro_file,
                                  define_xacro_test,
                                  gen_choices_product)


@pytest.mark.parametrize(
    'choices,expected',
    [
        pytest.param(
            (
                {'a': [9, 8]},
            ),
            [{'a': 9}, {'a': 8}],
            id='single_dict',
        ),
        pytest.param(
            (
                {'a': [9, 8]},
                {'b': [1, 2]},
            ),
            [{'a': 9, 'b': 1}, {'a': 9, 'b': 2}, {'a': 8, 'b': 1}, {'a': 8, 'b': 2}],
            id='two_dicts',
        ),
        pytest.param(
            (
                {'a': [9, 8], 'c': '23'},
            ),
            [{'a': 9, 'c': '23'}, {'a': 8, 'c': '23'}],
            id='mixed_dict',
        ),
        pytest.param(
            (
                DeclareLaunchArgument('a', choices=[9, 8]),
            ),
            [{'a': 8}, {'a': 9}],
            id='single_dla',
        ),
        pytest.param(
            (
                (DeclareLaunchArgument('a', choices=[9, 8]),
                 DeclareLaunchArgument('b', choices=[1, 2])),
            ),
            [{'a': 8, 'b': 1}, {'a': 8, 'b': 2}, {'a': 9, 'b': 1}, {'a': 9, 'b': 2}],
            id='double_dla',
        ),
        pytest.param(
            (
                DeclareLaunchArgument('a', choices=[9, 8]),
                DeclareLaunchArgument('b', choices=[1, 2]),
            ),
            [{'a': 8, 'b': 1}, {'a': 8, 'b': 2}, {'a': 9, 'b': 1}, {'a': 9, 'b': 2}],
            id='two_dla',
        ),
        pytest.param(
            (
                {'c': '23'},
                DeclareLaunchArgument('b', choices=[1, 2]),
            ),
            [{'b': 1, 'c': '23'}, {'b': 2, 'c': '23'}],
            id='dla_and_dict',
        ),
    ],
)
def test_gen_choices(choices, expected):
    assert list(gen_choices_product(*choices)) == expected


def test_define_xacro_test():
    func = define_xacro_test('test.xacro', {'a': [9, 8]}, {'b': [1, 2]})
    assert callable(func)
    assert func.__name__ == 'test_urdf'
    mark, = func.pytestmark
    assert mark.name == 'parametrize'
    assert mark.args[0] == 'params'
    params = {p.id: p.values for p in mark.args[1]}
    assert params == {
        'a:=8 b:=1': ({'a': 8, 'b': 1},),
        'a:=8 b:=2': ({'a': 8, 'b': 2},),
        'a:=9 b:=1': ({'a': 9, 'b': 1},),
        'a:=9 b:=2': ({'a': 9, 'b': 2},)
    }


def test_check_urdf():
    good_xml = """
    <?xml version="1.0"?>
    <robot name="robot">
      <link name="my_link"/>
    </robot>
    """
    check_urdf(good_xml)

    bad_xml = """
    <?xml version="1.0"?>
    <robot name="robot">
      <link name="my_link"/>
    </robot2>
    """
    with pytest.raises(subprocess.CalledProcessError):
        check_urdf(bad_xml)


def test_check_xacro_file():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.xacro') as f:
        f.write("""
        <robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="robot">
          <xacro:arg name="link" default=""/>
          <xacro:property name="link" value="$(arg link)"/>
          <link name="base"/>
          <link name="link"/>
          <joint name="joint" type="floating">
            <parent link="base"/>
            <child link="${link}"/>
          </joint>
        </robot>
        """)
        f.flush()
        check_xacro_file(f.name, {'link': 'link'})

        with pytest.raises(subprocess.CalledProcessError):
            check_xacro_file(f.name, {'link2': 'link'})


def test_check_invalid_xacro_file():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.xacro') as f:
        f.write("""
        <robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="robot">
          <link name="base"/>
          <link name="link"/>
          <joint name="joint" type="floating">
            <parent link="base"/>
            <child link="${link}"/>
          </joint>
        </robot>
        """)
        f.flush()
        with pytest.raises(xacro.XacroException):
            check_xacro_file(f.name, {'link': 'link'})
