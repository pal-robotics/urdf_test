cmake_minimum_required(VERSION 2.8.3)
project(urdf_test)

find_package(catkin REQUIRED COMPONENTS roscpp rostest)

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
include_directories(SYSTEM ${catkin_INCLUDE_DIRS})

add_rostest_gtest(${PROJECT_NAME} test/test_urdf.test src/test_urdf.cpp)
target_link_libraries(${PROJECT_NAME} ${catkin_LIBRARIES})

#############
## Install ##
#############

install(TARGETS ${PROJECT_NAME}
#   ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
#   LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
    RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(
    DIRECTORY test
    DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
