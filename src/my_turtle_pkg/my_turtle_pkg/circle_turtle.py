# my_turtle_pkg/my_turtle_pkg/circle_turtle.py
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class CircleTurtle(Node):
    def __init__(self):
        super().__init__('circle_turtle_node') 
        
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # declare parameter 
        self.declare_parameter('max_velocity', 0.25) # 상한선
        self.declare_parameter('my_speed', 0.1) # 실제 움직이는 속도
        self.declare_parameter('robot_color', 'blue') # 그냥 넣어본 거

        self.timer = self.create_timer(0.5, self.timer_callback)

    def timer_callback(self):
        limit_vel = self.get_parameter('max_velocity').value 
        target_vel = self.get_parameter('my_speed').value    
        color = self.get_parameter('robot_color').value

        if target_vel > limit_vel:
            final_vel = limit_vel
            state_msg = "Do not break the limit!"
        else:
            final_vel = target_vel
            state_msg = "Go Go Go!"


        self.get_logger().info(
            f'[{color}] target_vel:{target_vel} | limit_vel:{limit_vel} -> final_vel:{final_vel} ({state_msg})'
        )

        msg = Twist()
        
        # 리니어X 는 앞으로 가는 속도, 앵귤러Z 는 반시계방향 회전
        msg.linear.x = float(final_vel) 
        msg.angular.z = 0.2 
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = CircleTurtle()
    try:
        rclpy.spin(node) 
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
