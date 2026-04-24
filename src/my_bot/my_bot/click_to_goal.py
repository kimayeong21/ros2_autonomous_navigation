import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PointStamped
from rcl_interfaces.srv import SetParameters
from rclpy.parameter import Parameter


class ClickToGoal(Node):
    def __init__(self):
        super().__init__('click_to_goal')

        self.subscription = self.create_subscription(
            PointStamped,
            '/clicked_point',
            self.callback,
            10
        )

        # 🔥 pure_pursuit 노드 파라미터 변경용 클라이언트
        self.client = self.create_client(
            SetParameters,
            '/pure_pursuit_node/set_parameters'
        )

        self.get_logger().info("🔥 Click To Goal Node Started")

    def callback(self, msg):
        x = msg.point.x
        y = msg.point.y

        self.get_logger().info(f"Clicked Goal: x={x}, y={y}")

        # 서비스 준비 대기
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for pure_pursuit_node service...')

        # 요청 생성
        req = SetParameters.Request()
        req.parameters = [
            Parameter('goal_x', Parameter.Type.DOUBLE, x).to_parameter_msg(),
            Parameter('goal_y', Parameter.Type.DOUBLE, y).to_parameter_msg()
        ]

        # 서비스 호출
        self.client.call_async(req)


def main(args=None):
    rclpy.init(args=args)
    node = ClickToGoal()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
