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

import itertools
import subprocess

import pytest
import xacro

from collections.abc import Iterable, Sequence


def check_urdf(urdf, check=True, stdout=subprocess.DEVNULL, **kwargs):
    """Run check_urdf on the given URDF string. Output is redirected to /dev/null by default."""
    return subprocess.run(['check_urdf', "/dev/stdin"],
                          check=check,
                          text=True, input=urdf,
                          stdout=stdout,
                          **kwargs)


def check_xacro_file(xacro_file_path, mappings, check=True, **kwargs):
    """Process the given xacro file with the given mappings and run check_urdf on the result."""
    urdf = xacro.process_file(xacro_file_path, mappings=mappings).toxml()
    return check_urdf(urdf, check=check, **kwargs)


def _choices_from_dict(arg):
    # one list per key
    for k, v in arg.items():
        if isinstance(v, str) or not isinstance(v, Iterable):
            yield [(k, v)]
        else:
            yield [(k, c) for c in v]


def _gen_choices_list(*choices):
    """Normalize the choices into lists of tuples."""
    for args in choices:
        # if it's not a list/tuple, make it a list
        if not isinstance(args, Sequence):
            args = [args]

        for arg in args:
            if isinstance(arg, dict):
                yield from _choices_from_dict(arg)
            else:
                # assume launch.actions.DeclareLaunchArgument
                yield [(arg.name, c) for c in sorted(arg.choices)]


def gen_choices_product(*choices):
    """
    Generate the cartesian product of the choices as a list of dictionaries.

    Each choice is a DeclareLaunchArgument (or similar) object, a dictionary or a list of those.
    Each DeclareLaunchArgument yield on list of tuples, one per choice.
    Each dictionary yields one list of tuples per key, one per element in the value.

    Examples
    --------
    gen_choices_product(DeclareLaunchArgument(name="a", choices=[9, 8]),
                        DeclareLaunchArgument(name="b", choices=[7, 6])) yields
        {'a': 9, 'b': 7}, {'a': 9, 'b': 6}, {'a': 8, 'b': 7}, {'a': 8, 'b': 6}

    gen_choices_product({"c": [1, 2], "d": [3, 4]}) yields
        {'c': 1, 'd': 3}, {'c': 1, 'd': 4}, {'c': 2, 'd': 3}, {'c': 2, 'd': 4}
    which is the same as gen_choices_product({"c": [1, 2]}, {"d": [3, 4]})

    """
    for c in itertools.product(*_gen_choices_list(*choices)):
        yield dict(c)


def parametrize_choices(*choices):
    """Generate pytest parameters for the cartesian product of the choices with pretty ids."""
    for choice in gen_choices_product(*choices):
        yield pytest.param(choice, id=' '.join(f"{k}:={v}" for k, v in choice.items()))


def define_xacro_test(xacro_file_path, *choices):
    """Generate a pytest test that checks the given xacro file for the given choices."""
    @pytest.mark.parametrize("params", parametrize_choices(*choices))
    def test_urdf(params):
        check_xacro_file(xacro_file_path, params)
    return test_urdf
