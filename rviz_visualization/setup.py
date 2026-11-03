import os
from glob import glob
from setuptools import setup

package_name = 'rviz_visualization'

setup(
    name=package_name,
    version='0.9.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # 런치 파일과 RViz2 설정 파일을 share/<pkg>/launch, share/<pkg>/config 로 설치
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.rviz')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='student',
    maintainer_email='mamon010903@gmail.com',
    description='9주차 RViz2 심화 시각화 - 커스텀 MarkerArray 발행 노드',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'custom_marker_publisher = rviz_visualization.custom_marker_publisher:main',
        ],
    },
)
