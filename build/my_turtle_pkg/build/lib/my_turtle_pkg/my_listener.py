# my_listener.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

class MyListener(Node):
    def __init__(self):
        super().__init__('my_listener')

        my_qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )

        self.subscriber_ = self.create_subscription(
            String, 
            'sensor_data', 
            self.listener_callback,
            qos_profile=my_qos_profile 
        )

    def listener_callback(self, msg):
        data = f"Hello, This is my number {msg.data}"
        self.get_logger().info(data)

def main(args=None):
    rclpy.init(args=args)
    node = MyListener()
    try:
        rclpy.spin(node) 
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()