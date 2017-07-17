cmake_minimum_required(VERSION 2.8.3)
project(urdf_test)

find_package(catkin REQUIRED COMPONENTS roscpp)

###################################
## catkin specific configuration ##
###################################
catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES urdf_test
#  CATKIN_DEPENDS other_catkin_pkg
#  DEPENDS system_lib
)

###########
## Build ##
###########

#############
## Install ##
#############

#############
## Testing ##
#############

if(CATKIN_ENABLE_TESTING)
  find_package(rostest REQUIRED)
  add_rostest_gtest(test_urdf test/test_urdf.test test/test_urdf.cpp)
  target_link_libraries(test_urdf ${catkin_LIBRARIES})
endif()
