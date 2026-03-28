from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='stanley_controller',
            executable='stanley_node',
            name='stanley_controller',
            output='screen'
        ),
        Node(
            package='stanley_controller',
            executable='path_publisher',
            name='path_publisher',
            output='screen'
        )
    ])
