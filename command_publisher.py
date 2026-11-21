
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class CommandPublisher(Node):

    def __init__(self):
        super().__init__('command_publisher')

        self.publisher = self.create_publisher(Twist,'/cmd_vel',10)
        self.timer = self.create_timer(1.0,self.send_command)

    def send_command(self):
        msg = Twist()

        msg.linear.x = 1.0
        msg.angular.z = 0.5

        self.publisher.publish(msg)

        self.get_logger().info('Published velocity command')


def main():
    rclpy.init()

    node = CommandPublisher()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
