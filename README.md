# ROS2 Autonomous Navigation

## 📌 프로젝트 소개

ROS2 기반 TurtleBot3를 이용한 자율주행 로봇 프로젝트입니다.  
SLAM을 통해 맵을 생성하고, Navigation2를 활용하여 목표 지점까지 자동 이동합니다.
---
## 🚀 주요 기능
- SLAM 기반 맵 생성
- Navigation2 자율주행
- 키보드 수동 주행 (teleop)
- 맵 저장 및 재사용
- Pure Pursuit 기반 경로 추종
- 객체 감지 기반 비상 정지 기능
---
## ⚙️ 사용 기술
- ROS2 (Jazzy)
- TurtleBot3 (Waffle Pi)
- Gazebo Simulation
- SLAM Toolbox
- Navigation2
---
## 실행 방법

1. Gazebo 실행
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py

2. SLAM 실행 (맵 생성)
ros2 launch slam_toolbox online_async_launch.py use_sim_time:=true

3. 키보드 주행
ros2 run turtlebot3_teleop teleop_keyboard

4. 맵 저장
ros2 run nav2_map_server map_saver_cli -f ~/map

5. 자율주행
ros2 launch my_bot tb3_localization.launch.py/
ros2 launch nav2_bringup navigation_launch.py use_sim_time:=true autostart:=true

📂 프로젝트 구조
my_bot/
 ├── launch/
 ├── my_bot/
 │   ├── pure_pursuit.py
 │   ├── emergency_stop.py
 │   └── ...

🎯 결과
맵 생성 및 저장 성공
목표 지점 자동 이동 구현
객체 감지 시 정지 기능 구현
