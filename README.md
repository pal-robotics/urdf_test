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

