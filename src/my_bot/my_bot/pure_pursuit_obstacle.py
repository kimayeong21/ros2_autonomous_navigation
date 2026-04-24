import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, PoseWithCovarianceStamped
from sensor_msgs.msg import LaserScan
from math import atan2, sqrt, sin, pi
from rcl_interfaces.msg import SetParametersResult


class PurePursuitObstacle(Node):
    def __init__(self):
        super().__init__('pure_pursuit_node')

        self.declare_parameter('goal_x', 0.0)
        self.declare_parameter('goal_y', 0.0)

        self.add_on_set_parameters_callback(self.parameter_callback)

        self.goal_x = self.get_parameter('goal_x').value
        self.goal_y = self.get_parameter('goal_y').value

        self.lookahead_distance = 0.5
        self.linear_velocity = 0.2
        self.goal_tolerance = 0.2

        self.path = [[self.goal_x, self.goal_y]]
        self.current_waypoint_index = 0

        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)

        self.create_subscription(
            PoseWithCovarianceStamped,
            '/amcl_pose',
            self.pose_callback,
            10
        )

        # 🔥 LiDAR 구독
        self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )

        self.min_distance = 999.0

        self.current_x = 0.0
        self.current_y = 0.0
        self.current_yaw = 0.0
        self.is_localized = False

        self.timer = self.create_timer(0.3, self.control_loop)

    def scan_callback(self, msg):
        self.min_distance = min(msg.ranges)

    def parameter_callback(self, params):
        for param in params:
            if param.name == 'goal_x':
                self.goal_x = param.value
            if param.name == 'goal_y':
                self.goal_y = param.value

        self.path = [[self.goal_x, self.goal_y]]
        self.current_waypoint_index = 0

        return SetParametersResult(successful=True)

    def pose_callback(self, msg):
        self.current_x = msg.pose.pose.position.x
        self.current_y = msg.pose.pose.position.y

        q = msg.pose.pose.orientation
        self.current_yaw = atan2(
            2.0 * (q.w * q.z + q.x * q.y),
            1.0 - 2.0 * (q.y * q.y + q.z * q.z)
        )

        self.is_localized = True

    def control_loop(self):
        if not self.is_localized:
            return

        # 🔥 장애물 회피
        if self.min_distance < 0.5:
            cmd = Twist()
            cmd.angular.z = 0.5  # 회전
            self.publisher_.publish(cmd)
            self.get_logger().info("🚧 Obstacle Detected!")
            return

        goal_x, goal_y = self.path[0]

        dx = goal_x - self.current_x
        dy = goal_y - self.current_y
        distance = sqrt(dx**2 + dy**2)

        if distance < self.goal_tolerance:
            self.stop_robot()
            return

        target_angle = atan2(dy, dx)
        alpha = target_angle - self.current_yaw

        if alpha > pi:
            alpha -= 2*pi
        elif alpha < -pi:
            alpha += 2*pi

        angular = self.linear_velocity * (2.0 * sin(alpha)) / self.lookahead_distance

        cmd = Twist()
        cmd.linear.x = self.linear_velocity
        cmd.angular.z = max(min(angular, 1.0), -1.0)

        self.publisher_.publish(cmd)

    def stop_robot(self):
        self.publisher_.publish(Twist())


def main(args=None):
    rclpy.init(args=args)
    node = PurePursuitObstacle()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
