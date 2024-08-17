from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import FindExecutable

def generate_launch_description():
    # Define paths
    pkg_share = FindPackageShare(package='isaac_turtlerbot4').find('isaac_turtlerbot4')
    
    # Process the xacro file to generate a URDF string
    urdf_file = Command([
        PathJoinSubstitution([FindExecutable(name='xacro')]), 
        ' ', PathJoinSubstitution([pkg_share, 'urdf', 'turtlebot4.urdf.xacro'])
    ])

    # Ignition Gazebo launch file
    ignition_gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('ros_ign_gazebo'), 'launch', 'ign_gazebo.launch.py'
            ])
        ])
    )

    # Node to spawn robot in Ignition Gazebo
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'turtlebot4',
            '-string', urdf_file,  # Use the generated URDF string
            '-z', '0.5'  # Adjust the z-height if needed
        ],
        output='screen'
    )

    return LaunchDescription([
        ignition_gazebo_launch,
        spawn_entity
    ])
