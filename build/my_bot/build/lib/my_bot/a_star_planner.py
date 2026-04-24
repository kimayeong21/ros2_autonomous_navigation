import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PointStamped
import heapq

class AStarPlanner(Node):
    def __init__(self):
        super().__init__('astar_planner')

        self.subscription = self.create_subscription(
            PointStamped,
            '/clicked_point',
            self.goal_callback,
            10
        )

        # 간단한 맵 (테스트용)
        self.grid_map = [
            [0,0,0,0,1,0],
            [1,1,1,0,1,0],
            [0,0,0,0,0,0],
            [0,1,1,1,1,0],
            [0,0,0,0,0,0]
        ]

        self.start = (0,0)

        self.get_logger().info("🔥 A* Planner Ready")

    class NodeA:
        def __init__(self, parent=None, pos=None):
            self.parent = parent
            self.pos = pos
            self.g = 0
            self.h = 0
            self.f = 0

        def __lt__(self, other):
            return self.f < other.f

        def __eq__(self, other):
            return self.pos == other.pos

    def astar(self, maze, start, end):
        open_list = []
        closed_list = []

        start_node = self.NodeA(None, start)
        end_node = self.NodeA(None, end)

        heapq.heappush(open_list, start_node)

        while open_list:
            current = heapq.heappop(open_list)
            closed_list.append(current)

            if current == end_node:
                path = []
                while current:
                    path.append(current.pos)
                    current = current.parent
                return path[::-1]

            for move in [(0,1),(0,-1),(1,0),(-1,0)]:
                pos = (current.pos[0]+move[0], current.pos[1]+move[1])

                if pos[0]<0 or pos[1]<0 or pos[0]>=len(maze) or pos[1]>=len(maze[0]):
                    continue

                if maze[pos[0]][pos[1]] != 0:
                    continue

                node = self.NodeA(current, pos)

                if node in closed_list:
                    continue

                node.g = current.g + 1
                node.h = (pos[0]-end_node.pos[0])**2 + (pos[1]-end_node.pos[1])**2
                node.f = node.g + node.h

                heapq.heappush(open_list, node)

        return None

    def goal_callback(self, msg):
        goal = (int(msg.point.x), int(msg.point.y))

        path = self.astar(self.grid_map, self.start, goal)

        self.get_logger().info(f"🔥 Path: {path}")


def main(args=None):
    rclpy.init(args=args)
    node = AStarPlanner()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
