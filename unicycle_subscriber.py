import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist,Pose2D
from math import cos, sin

class UnicycleSubscriber(Node):

    def __init__(self):
        super().__init__('unicycle_subscriber')
        self.subscription = self.create_subscription(Twist,'/cmd_vel',self.command_callback,10)
        self.pose_publisher = self.create_publisher(Pose2D,'/robot_pose',10)
        self.v=0.0
        self.omega=0.0
        self.x=0.0
        self.y=0.0
        self.theta=0.0
        self.last_time = self.get_clock().now()
        self.timer = self.create_timer(0.1,lambda: self.timer_callback())

    
    def command_callback(self,msg):
        self.v = msg.linear.x
        self.omega = msg.angular.z

        self.get_logger().info(f'Received command: linear_velocity={self.v}, angular_velocity={self.omega}')
    
    def update_pose(self,dt):
        self.x += self.v * dt * cos(self.theta)
        self.y += self.v * dt * sin(self.theta)
        self.theta += self.omega * dt
        pose_msg = Pose2D()
        pose_msg.x = self.x
        pose_msg.y = self.y
        pose_msg.theta = self.theta
        self.pose_publisher.publish(pose_msg)
        self.get_logger().info(f'Updated pose: x={self.x}, y={self.y}, theta={self.theta}')
    
    def timer_callback(self):
        current_time = self.get_clock().now()
        dt = (current_time - self.last_time).nanoseconds / 1e9
        self.last_time = current_time
        self.update_pose(dt)

def main():
    rclpy.init()

    node = UnicycleSubscriber()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__': 
    main()