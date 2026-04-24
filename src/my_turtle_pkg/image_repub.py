import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

class ImageRepublisher(Node):
    def __init__(self):
        super().__init__('image_republisher')

        # 🔥 QoS 설정
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )

        self.bridge = CvBridge()

        # 원본 이미지 구독
        self.subscription = self.create_subscription(
            Image,
            '/image_raw',
            self.callback,
            qos_profile
        )

        # 다시 발행
        self.publisher = self.create_publisher(
            Image,
            '/image_repub',
            qos_profile
        )

    def callback(self, msg):
        # ROS → OpenCV
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        self.get_logger().info("Image received & republished")

        # OpenCV → ROS
        new_msg = self.bridge.cv2_to_imgmsg(cv_image, encoding='bgr8')

        self.publisher.publish(new_msg)


def main(args=None):
    rclpy.init(args=args)
    node = ImageRepublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
