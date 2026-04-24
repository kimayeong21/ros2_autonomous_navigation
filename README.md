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

## ▶️ 실행 방법

### 1. Gazebo 실행
```bash
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
