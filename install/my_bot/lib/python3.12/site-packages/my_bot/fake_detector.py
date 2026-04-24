import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool


class FakeDetector(Node):
    def __init__(self):
        super().__init__('fake_detector')

        self.pub = self.create_publisher(Bool, '/emergency_stop', 10)

        self.timer = self.create_timer(5.0, self.detect)

    def detect(self):
        msg = Bool()
        msg.data = True

        self.get_logger().info("🔥 객체 감지됨 → 정지!")
        self.pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = FakeDetector()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
