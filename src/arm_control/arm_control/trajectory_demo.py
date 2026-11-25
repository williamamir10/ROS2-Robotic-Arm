import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

JOINTS = ['joint1', 'joint2', 'joint3', 'joint4']

class TrajectoryDemo(Node):
    def __init__(self):
        super().__init__('trajectory_demo')
        self.publisher = self.create_publisher(JointTrajectory, '/arm_controller/joint_trajectory', 10)
        self.timer = self.create_timer(2.0, self.publish_demo)
        self.sent = False

    def publish_demo(self):
        if self.sent:
            return
        msg = JointTrajectory()
        msg.joint_names = JOINTS
        point = JointTrajectoryPoint()
        point.positions = [0.0, 0.45, -0.65, 0.35]  # radians
        point.time_from_start.sec = 3
        msg.points = [point]
        self.publisher.publish(msg)
        self.get_logger().info('Published demo trajectory to /arm_controller/joint_trajectory')
        self.sent = True
        self.timer.cancel()

def main(args=None):
    rclpy.init(args=args)
    node = TrajectoryDemo()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
