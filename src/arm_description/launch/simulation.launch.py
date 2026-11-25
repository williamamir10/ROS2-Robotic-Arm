from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time')

    xacro_file = PathJoinSubstitution([
        FindPackageShare('arm_description'), 'urdf', 'robot_arm.urdf.xacro'
    ])

    world_file = PathJoinSubstitution([
        FindPackageShare('arm_description'), 'worlds', 'empty.sdf'
    ])

    rviz_file = PathJoinSubstitution([
        FindPackageShare('arm_description'), 'rviz', 'arm.rviz'
    ])

    robot_description = {
        'robot_description': Command(['xacro ', xacro_file])
    }

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('ros_gz_sim'),
                'launch',
                'gz_sim.launch.py'
            ])
        ]),
        launch_arguments={'gz_args': ['-r ', world_file]}.items()
    )

    # Automatically bridge Gazebo clock to ROS 2
    clock_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock'
        ],
        output='screen'
    )

    rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[
            robot_description,
            {'use_sim_time': use_sim_time}
        ],
        output='screen'
    )

    spawn = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-topic', 'robot_description',
            '-name', 'dms_robot_arm',
            '-allow_renaming', 'true'
        ],
        output='screen'
    )

    jsb = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'joint_state_broadcaster',
            '--controller-manager',
            '/controller_manager'
        ],
        output='screen'
    )

    arm = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'arm_controller',
            '--controller-manager',
            '/controller_manager'
        ],
        output='screen'
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_file],
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen'
    )

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true'),
        gazebo,
        clock_bridge,
        rsp,
        spawn,
        TimerAction(period=8.0, actions=[jsb]),
        TimerAction(period=10.0, actions=[arm]),
        TimerAction(period=12.0, actions=[rviz]),
    ])
