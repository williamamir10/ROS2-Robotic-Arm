# Robotic Arm – ROS 2, Gazebo & Hardware Control

## 1. Project Overview

A 4-DOF robotic arm controlled using ROS 2 Jazzy.

The project integrates:
- URDF/Xacro robot description.
- Gazebo simulation.
- RViz2 visualization.
- ROS 2 JointTrajectory control.
- Python trajectory GUI.
- Arduino Uno hardware bridge.
- Two physical servo motors.

**Note:** The simulation supports four joints. The current physical prototype uses two servos connected to joint1 and joint2. Joints 3 and 4 are simulated only.

## 2. Robot Dimensions

| Component | Dimension |
|---|---:|
| Base | 8 cm |
| Link 1 | 12 cm |
| Link 2 | 15 cm |
| Link 3 | 9 cm |
| End Effector | 6 cm |

## 3. Software Requirements

- Ubuntu 24.04
- ROS 2 Jazzy
- Gazebo
- RViz2
- Python 3
- pyserial
- Arduino IDE

## 4. Workspace Structure

```text
dms_lab2_ws/
├── src/
│   ├── arm_description/
│   │   ├── urdf/
│   │   ├── launch/
│   │   ├── config/
│   │   ├── rviz/
│   │   └── worlds/
│   └── arm_control/
│       └── arm_control/
│           ├── trajectory_demo.py
│           ├── trajectory_gui.py
│           └── hardware_bridge.py
├── firmware/
│   └── arduino/
│       └── arm_servos.ino
├── README.md
└── .gitignore
```

## 5. Build Instructions

```bash
source /opt/ros/jazzy/setup.bash
cd ~/dms_lab2_ws
colcon build --symlink-install
source install/setup.bash
```

## 6. Running the Project

Open three terminals.

### Terminal 1 – Simulation

```bash
source /opt/ros/jazzy/setup.bash
cd ~/dms_lab2_ws
source install/setup.bash
ros2 launch arm_description simulation.launch.py
```

### Terminal 2 – Hardware Bridge

```bash
source /opt/ros/jazzy/setup.bash
cd ~/dms_lab2_ws
source install/setup.bash
ros2 run arm_control hardware_bridge
```

### Terminal 3 – Trajectory GUI

```bash
source /opt/ros/jazzy/setup.bash
cd ~/dms_lab2_ws
source install/setup.bash
ros2 run arm_control trajectory_gui
```

Move the GUI sliders to control the simulated arm and the two physical servos.

## 7. Hardware Connections

### Arduino Uno

| Component | Arduino Pin |
|---|---|
| Servo 1 Signal | D9 |
| Servo 2 Signal | D10 |
| Servo Power | External regulated 5V supply |
| Ground | Common GND |

**Important:** Use a suitable external power supply for the servos. Do not power the servos from the Arduino 5V pin. Connect the external supply ground to Arduino GND.

### Serial Configuration

| Parameter | Value |
|---|---|
| Serial Port | /dev/ttyACM0 |
| Baud Rate | 115200 |
| Communication | USB Serial |
| Message Format | CSV |
| Number of Servo Angles | 2 |

Example message:

```text
90,116
```

Each message ends with a newline character (`\n`).

## 8. ROS 2 Communication

The hardware bridge subscribes to:

```text
/arm_controller/joint_trajectory
```

Message type:

```text
trajectory_msgs/msg/JointTrajectory
```

The bridge converts joint positions from radians to servo angles in degrees and sends commands to the Arduino.

## 9. Arduino Firmware

Firmware location:

```text
firmware/arduino/arm_servos.ino
```

Upload the firmware to the Arduino Uno using Arduino IDE.

## 10. Troubleshooting

- If the serial port cannot be accessed, add your user to the `dialout` group:

```bash
sudo usermod -aG dialout $USER
```

Log out and log in again for the change to take effect.

- Check the Arduino serial port:

```bash
ls /dev/ttyACM*
```

- Ensure the Arduino and servo power supply share a common ground.
- Make sure no other application is using the Arduino serial port.
- Source the ROS 2 workspace in every terminal before running ROS 2 commands.

## 11. Project Status

- [x] URDF robot model
- [x] Four revolute joints
- [x] Gazebo simulation
- [x] RViz2 visualization
- [x] JointTrajectory control
- [x] Python GUI
- [x] Arduino serial communication
- [x] Two physical servo motors
- [x] Integrated simulation and hardware control
