# urdf_test

Provides a utility to test that a robot_description is loaded and published correctly from a launch file.

To use it include a launch_test in your package's CMakeLists.txt
```cmake
	add_launch_test(
	  test/test_description.launch.py
	  TARGET "pmb2_description_${laser_model}_${courier_rgbd_sensors}" # With TARGET set test name
      ARGS "laser_model:=${laser_model}" "courier_rgbd_sensors:=${courier_rgbd_sensors}" # You can use variables to test different configurations
	)
```

And in the launch.py file include the description generator and the Test classes:
```python
from urdf_test.description_test import (generate_urdf_test_description,
                                        TestDescriptionPublished, TestSuccessfulExit)
from launch_pal.include_utils import include_launch_py_description

# Ignore unused import warnings for the Test Classes
__all__ = ('TestDescriptionPublished', 'TestSuccessfulExit')


def generate_test_description():
    return generate_urdf_test_description(
        include_launch_py_description(
            'pmb2_description', ['launch', 'robot_state_publisher.launch.py']),
    )
```

# xacro_test

As a faster alternative, the xacro can get checked directly.
`define_xacro_test` takes a xacro file path and a number of `DeclareLaunchArgument` arguments,
which are used to form the test matrix (cartesian product).


```python
from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from pmb2_description.launch_arguments import PMB2Args

from urdf_test.xacro_test import define_xacro_test

xacro_file_path = Path(
    get_package_share_directory('pmb2_description'),
    'robots',
    'pmb2.urdf.xacro',
)

test_xacro = define_xacro_test(xacro_file_path, PMB2Args.laser_model, PMB2Args.add_on_module)
```
