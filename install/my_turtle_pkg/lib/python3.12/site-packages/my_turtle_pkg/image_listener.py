import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

class ImageListener(Node):
    def __init__(self):
        super().__init__('image_listener')

        # 🔥 QoS 동일하게 맞추기
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )

        self.bridge = CvBridge()

        self.subscription = self.create_subscription(
            Image,
            '/image_repub',
            self.callback,
            qos_profile
        )

    def callback(self, msg):
        # ROS → OpenCV 변환
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        self.get_logger().info("Image received!")


def main(args=None):
    rclpy.init(args=args)
    node = ImageListener()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
