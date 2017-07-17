
#include <ros/ros.h>
#include <gtest/gtest.h>

namespace pal
{
TEST(TestURDFTest, testURDFParam)
{
  ros::NodeHandle nh;
  std::string test_string;
  ASSERT_TRUE(nh.getParam("robot_description", test_string));
  ASSERT_NE("", test_string);
}
}

int main(int argc, char **argv)
{
  ros::init(argc, argv, "");
  // ros::start();
  testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
