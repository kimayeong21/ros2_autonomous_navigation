# 2초마다 ROS 표준 문자열 타입의 토픽이 발행되는 노드 (feat. 내가 직접 QOS 설정) 
# my_talker.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

class MyTalker(Node):
    def __init__(self):
        super().__init__('my_talker')

        my_qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )

        self.publisher_ = self.create_publisher(
            String, 
            'sensor_data', 
            qos_profile=my_qos_profile 
        )

        self.number = 1

        self.timer = self.create_timer(2.0, self.timer_callback)

    def timer_callback(self):
        msg = String()
        msg.data = f"Hello, This is my number {self.number}"
        self.get_logger().info(msg.data)
        self.publisher_.publish(msg)
        self.number += 1
        

def main(args=None):
    rclpy.init(args=args)
    node = MyTalker()
    try:
        rclpy.spin(node) 
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()