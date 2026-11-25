"""Simple Tkinter GUI publishing four joint targets in radians."""
import tkinter as tk
from tkinter import ttk
import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

JOINTS = ['joint1', 'joint2', 'joint3', 'joint4']

class GuiNode(Node):
    def __init__(self):
        super().__init__('arm_trajectory_gui')
        self.pub = self.create_publisher(JointTrajectory, '/arm_controller/joint_trajectory', 10)

    def send(self, values):
        msg = JointTrajectory()
        msg.joint_names = JOINTS
        point = JointTrajectoryPoint()
        point.positions = [float(v) for v in values]
        point.time_from_start.sec = 2
        msg.points = [point]
        self.pub.publish(msg)
        self.get_logger().info(f'Sent joint target (rad): {values}')

def main(args=None):
    rclpy.init(args=args)
    node = GuiNode()
    root = tk.Tk()
    root.title('DoMS Lab 2 - Robotic Arm Controller')
    root.geometry('460x390')
    ttk.Label(root, text='Set joint positions (radians)', font=('Arial', 14, 'bold')).pack(pady=12)
    sliders = []
    for name in JOINTS:
        frame = ttk.Frame(root, padding=6)
        frame.pack(fill='x')
        ttk.Label(frame, text=name, width=10).pack(side='left')
        var = tk.DoubleVar(value=0.0)
        scale = tk.Scale(frame, variable=var, from_=-1.57, to=1.57, resolution=0.01, orient='horizontal', length=300)
        scale.pack(side='left', fill='x', expand=True)
        sliders.append(var)
    def send():
        node.send([v.get() for v in sliders])
    ttk.Button(root, text='Send trajectory', command=send).pack(pady=18)
    ttk.Label(root, text='The same topic is consumed by Gazebo and the hardware bridge.').pack()
    def on_close():
        root.destroy()
    root.protocol('WM_DELETE_WINDOW', on_close)
    try:
        root.mainloop()
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
