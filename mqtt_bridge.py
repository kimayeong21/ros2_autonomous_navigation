import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped

import json
import paho.mqtt.client as mqtt


class Bridge(Node):
    def __init__(self):
        super().__init__('bridge')

        # -------------------------------
        # ROS2 Publisher (목표 위치)
        # -------------------------------
        self.goal_pub = self.create_publisher(
            PoseStamped,
            '/goal_pose',
            10
        )

        # -------------------------------
        # ROS2 Subscriber (상태)
        # -------------------------------
        self.create_subscription(
            String,
            '/robot_status',
            self.status_callback,
            10
        )

        # -------------------------------
        # MQTT 설정
        # -------------------------------
        self.client = mqtt.Client()

        # 연결 이벤트
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        try:
            self.client.connect("127.0.0.1", 1883, 60)
            self.get_logger().info("MQTT 연결 성공")
        except Exception as e:
            self.get_logger().error(f"MQTT 연결 실패: {e}")

        # MQTT 루프 시작 (중요)
        self.client.loop_start()

        self.get_logger().info("🚀 Bridge Node Started")

    # -------------------------------
    # MQTT 연결 시 실행
    # -------------------------------
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.get_logger().info("MQTT 브로커 연결됨")
            client.subscribe("robot/task")
            self.get_logger().info("robot/task 구독 시작")
        else:
            self.get_logger().error(f"MQTT 연결 실패 코드: {rc}")

    # -------------------------------
    # MQTT → ROS2
    # -------------------------------
    def on_message(self, client, userdata, msg):
        try:
            payload = msg.payload.decode()
            self.get_logger().info(f"📩 MQTT 메시지 수신: {payload}")

            data = json.loads(payload)

            if data.get("type") == "goal":
                pose = PoseStamped()
                pose.header.frame_id = "map"

                pose.pose.position.x = float(data["x"])
                pose.pose.position.y = float(data["y"])
                pose.pose.orientation.w = 1.0

                self.goal_pub.publish(pose)
                self.get_logger().info("✅ ROS2 goal_pose 전송 완료")

        except Exception as e:
            self.get_logger().error(f"❌ MQTT 처리 오류: {e}")

    # -------------------------------
    # ROS2 → MQTT
    # -------------------------------
    def status_callback(self, msg):
        try:
            data = {
                "status": msg.data
            }

            self.client.publish("robot/status", json.dumps(data))
            self.get_logger().info(f"📤 MQTT 전송: {data}")

        except Exception as e:
            self.get_logger().error(f"❌ MQTT 전송 오류: {e}")


def main():
    rclpy.init()
    node = Bridge()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("종료 중...")

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
