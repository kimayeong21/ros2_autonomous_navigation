import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
from geometry_msgs.msg import Twist


class EmergencyStop(Node):
    def __init__(self):
        super().__init__('emergency_stop')

        # 🔥 비상정지 신호 구독
        self.sub = self.create_subscription(
            Bool,
            '/emergency_stop',
            self.callback,
            10
        )

        # 🔥 cmd_vel 퍼블리셔
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)

        self.get_logger().info("🚨 Emergency Stop Node Ready")

    def callback(self, msg):
        if msg.data:
            self.get_logger().warn("🚨 EMERGENCY STOP!")

            stop = Twist()
            stop.linear.x = 0.0
            stop.angular.z = 0.0

            # 계속 보내야 확실히 멈춤
            for _ in range(10):
                self.pub.publish(stop)


def main(args=None):
    rclpy.init(args=args)
    node = EmergencyStop()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
