"""ROS 2 JointTrajectory to USB-serial bridge.

Protocol: one CSV line containing two integer servo angles in degrees.
Example: 90,116\\n
Only joint1 and joint2 are connected to physical servos.
"""

import math
import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory

try:
    import serial
except ImportError:
    serial = None

SERVO_JOINTS = ['joint1', 'joint2']


class HardwareBridge(Node):
    def __init__(self):
        super().__init__('arm_hardware_bridge')

        self.declare_parameter('serial_port', '/dev/ttyACM0')
        self.declare_parameter('baud_rate', 115200)
        self.declare_parameter('servo_zero_deg', [90.0, 90.0])
        self.declare_parameter('servo_direction', [1.0, 1.0])

        self.ser = None

        if serial is None:
            self.get_logger().error(
                'pyserial is missing. Install with: sudo apt install python3-serial'
            )
        else:
            port = self.get_parameter('serial_port').value
            baud = int(self.get_parameter('baud_rate').value)

            try:
                self.ser = serial.Serial(
                    port, baud, timeout=0.1, write_timeout=0.2
                )
                self.get_logger().info(
                    f'Connected to microcontroller on {port} at {baud} baud'
                )
            except Exception as exc:
                self.get_logger().error(
                    f'Could not open serial port {port}: {exc}'
                )

        self.sub = self.create_subscription(
            JointTrajectory,
            '/arm_controller/joint_trajectory',
            self.callback,
            10
        )

    def callback(self, msg):
        if not msg.points:
            self.get_logger().warning('Received trajectory without points')
            return

        target = dict(zip(msg.joint_names, msg.points[-1].positions))

        zeros = self.get_parameter('servo_zero_deg').value
        directions = self.get_parameter('servo_direction').value

        angles = []

        for i, joint in enumerate(SERVO_JOINTS):
            rad = float(target.get(joint, 0.0))
            deg = float(zeros[i]) + float(directions[i]) * math.degrees(rad)
            angles.append(max(0, min(180, round(deg))))

        line = ','.join(map(str, angles)) + '\n'

        self.get_logger().info(f'Servo command: {line.strip()}')

        if self.ser:
            try:
                self.ser.write(line.encode('ascii'))
            except Exception as exc:
                self.get_logger().error(f'Serial write failed: {exc}')


def main(args=None):
    rclpy.init(args=args)
    node = HardwareBridge()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    if node.ser:
        node.ser.close()

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
