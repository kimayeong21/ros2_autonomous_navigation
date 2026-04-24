# my_turtle_pkg/launch/custom_waffle.launch.py
import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    
    # 파라미터가 저장된 파일 경로 찾기 
    config_path = PathJoinSubstitution([
        FindPackageShare('my_turtle_pkg'), 'config', 'waffle_params.yaml'
    ])
	
		# 런치파일 인자 정의하기 
    color_arg = DeclareLaunchArgument(
        'robot_color', default_value='blue'
    )
    speed_arg = DeclareLaunchArgument(
        'target_speed', default_value='0.1',
        description='User desired speed'
    )

    waffle_node = Node(
        package='my_turtle_pkg',
        executable='circle_node',
        namespace='kyh',
        name='waffle_driver',
        output='screen',
        # 야밀 파일에 정의된 파마리터와 직접 정의한 파라미터 혼용 가능!
        parameters=[
            config_path,  
            {'robot_color': LaunchConfiguration('robot_color') },
            {'my_speed': LaunchConfiguration('target_speed') }
        ]
    )

    pkg_gazebo_ros = FindPackageShare(package='turtlebot3_gazebo').find('turtlebot3_gazebo')
    start_gazebo_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'turtlebot3_world.launch.py')
        )
    )

    return LaunchDescription([
        start_gazebo_cmd, 
        color_arg,
        speed_arg,
        waffle_node
    ])
