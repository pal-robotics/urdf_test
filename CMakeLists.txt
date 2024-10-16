cmake_minimum_required(VERSION 3.5)
project(urdf_test)

find_package(ament_cmake_auto REQUIRED)
ament_auto_find_build_dependencies()

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()

  ament_add_pytest_test(test_xacro_test tests/test_xacro_test.py)
endif()


install(PROGRAMS
  scripts/test_urdf.py
  DESTINATION lib/${PROJECT_NAME}
)

# Install Python modules
ament_python_install_package(${PROJECT_NAME})

ament_auto_package()
