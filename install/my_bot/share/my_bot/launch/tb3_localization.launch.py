import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    nav2_bringup_dir = get_package_share_directory('nav2_bringup')
    turtlebot3_gazebo_dir = get_package_share_directory('turtlebot3_gazebo')

    # 👉 여기에 네 map.yaml 경로 넣기
    map_file_path = os.path.expanduser('~/map.yaml')

    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    map_yaml_file = LaunchConfiguration('map', default=map_file_path)

    # 🔥 Gazebo 실행
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(turtlebot3_gazebo_dir, 'launch', 'turtlebot3_world.launch.py')
        ),
        launch_arguments={
            'use_sim_time': use_sim_time
        }.items()
    )

    # 🔥 Localization (Nav2)
    localization_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_bringup_dir, 'launch', 'localization_launch.py')
        ),
        launch_arguments={
            'map': map_yaml_file,
            'use_sim_time': use_sim_time,
            'params_file': os.path.join(nav2_bringup_dir, 'params', 'nav2_params.yaml')
        }.items()
    )

    # 🔥 RViz 실행
    rviz_config_dir = os.path.join(
        nav2_bringup_dir,
        'rviz',
        'nav2_default_view.rviz'
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_dir],
        parameters=[{'use_sim_time': True}],
        output='screen'
    )

    return LaunchDescription([

        DeclareLaunchArgument(
            'map',
            default_value=map_file_path,
            description='Full path to map yaml file'
        ),

        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation time'
        ),

        gazebo_launch,
        localization_launch,
        rviz_node
    ])
