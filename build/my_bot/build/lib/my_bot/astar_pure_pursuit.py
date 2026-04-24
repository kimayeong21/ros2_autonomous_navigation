import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, PoseStamped, PoseWithCovarianceStamped
from nav_msgs.msg import OccupancyGrid
import numpy as np
import heapq
from math import atan2, sqrt, sin, pi


class AStarPurePursuit(Node):
    def __init__(self):
        super().__init__('astar_pure_pursuit')

        # 📌 상태 변수
        self.map_data = None
        self.map_width = 0
        self.map_height = 0
        self.resolution = 0.05
        self.origin = [0.0, 0.0]

        self.current_pose = [0.0, 0.0]
        self.current_yaw = 0.0
        self.goal_pose = None

        self.path = []
        self.index = 0

        # 📌 Subscriber
        self.create_subscription(OccupancyGrid, '/map', self.map_callback, 10)
        self.create_subscription(PoseWithCovarianceStamped, '/amcl_pose', self.pose_callback, 10)
        self.create_subscription(PoseStamped, '/goal_pose', self.goal_callback, 10)

        # 📌 Publisher
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        self.timer = self.create_timer(0.3, self.control_loop)

        self.get_logger().info("🔥 A* + Pure Pursuit 시작!")

    def map_callback(self, msg):
        self.map_width = msg.info.width
        self.map_height = msg.info.height
        self.resolution = msg.info.resolution
        self.origin = [msg.info.origin.position.x, msg.info.origin.position.y]
        self.map_data = np.array(msg.data).reshape((self.map_height, self.map_width))

    def pose_callback(self, msg):
        self.current_pose = [msg.pose.pose.position.x, msg.pose.pose.position.y]
        q = msg.pose.pose.orientation
        self.current_yaw = atan2(2*(q.w*q.z + q.x*q.y), 1-2*(q.y*q.y + q.z*q.z))

    def goal_callback(self, msg):
        self.goal_pose = [msg.pose.position.x, msg.pose.position.y]
        self.get_logger().info(f"🎯 목표 설정: {self.goal_pose}")
        self.plan_path()

    def world_to_grid(self, x, y):
        gx = int((x - self.origin[0]) / self.resolution)
        gy = int((y - self.origin[1]) / self.resolution)
        return gy, gx

    def grid_to_world(self, gy, gx):
        x = gx * self.resolution + self.origin[0]
        y = gy * self.resolution + self.origin[1]
        return [x, y]

    def plan_path(self):
        if self.map_data is None:
            return

        start = self.world_to_grid(*self.current_pose)
        goal = self.world_to_grid(*self.goal_pose)

        path = self.astar(self.map_data, start, goal)

        if path:
            self.path = [self.grid_to_world(p[0], p[1]) for p in path]
            self.index = 0
            self.get_logger().info(f"🔥 경로 생성 완료! {len(self.path)}개 포인트")
        else:
            self.get_logger().warn("❌ 경로 생성 실패")

    def astar(self, grid, start, goal):
        open_list = []
        heapq.heappush(open_list, (0, start))
        came_from = {}
        cost = {start: 0}

        while open_list:
            _, current = heapq.heappop(open_list)

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                return path[::-1]

            for dx, dy in [(0,1),(1,0),(-1,0),(0,-1)]:
                nx, ny = current[0]+dx, current[1]+dy

                if not (0 <= nx < grid.shape[0] and 0 <= ny < grid.shape[1]):
                    continue
                if grid[nx][ny] != 0:
                    continue

                new_cost = cost[current] + 1
                if (nx, ny) not in cost or new_cost < cost[(nx, ny)]:
                    cost[(nx, ny)] = new_cost
                    priority = new_cost + sqrt((nx-goal[0])**2 + (ny-goal[1])**2)
                    heapq.heappush(open_list, (priority, (nx, ny)))
                    came_from[(nx, ny)] = current

        return None

    def control_loop(self):
        if not self.path or self.index >= len(self.path):
            return

        target = self.path[self.index]

        dx = target[0] - self.current_pose[0]
        dy = target[1] - self.current_pose[1]
        distance = sqrt(dx**2 + dy**2)

        if distance < 0.2:
            self.index += 1
            return

        angle = atan2(dy, dx)
        alpha = angle - self.current_yaw

        if alpha > pi: alpha -= 2*pi
        elif alpha < -pi: alpha += 2*pi

        cmd = Twist()
        cmd.linear.x = 0.2
        cmd.angular.z = 0.5 * alpha

        self.cmd_pub.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = AStarPurePursuit()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
