from setuptools import setup
package_name = 'arm_control'
setup(
    name=package_name, version='0.0.1', packages=[package_name],
    data_files=[('share/ament_index/resource_index/packages', ['resource/' + package_name]), ('share/' + package_name, ['package.xml'])],
    install_requires=['setuptools'], zip_safe=True,
    maintainer='Student', maintainer_email='student@example.com',
    description='DoMS Lab 2 robotic arm control nodes', license='Apache-2.0',
    entry_points={'console_scripts': [
        'trajectory_demo = arm_control.trajectory_demo:main',
        'trajectory_gui = arm_control.trajectory_gui:main',
        'hardware_bridge = arm_control.hardware_bridge:main',
    ]},
)
