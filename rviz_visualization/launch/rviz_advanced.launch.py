#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
강의명: 오토모티브SW프로그래밍
주차: 9주차
파일명: rviz_advanced.launch.py
설명: 커스텀 마커 발행 노드(custom_marker_publisher)와
      사전 구성된 RViz2 시각화 화면을 동시에 실행하는 ROS 2 Python 런치 파일
"""

import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, LogInfo
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    """
    ROS 2 런치 디스크립션 생성 함수
    """

    # -------------------------------------------------------------------------
    # 1. 파일 경로 탐색
    #    - launch 파일이 위치한 폴더의 상위 폴더(install/share/rviz_visualization) 기준
    #      config/integrated_view.rviz 경로 획득 (setup.py data_files로 함께 설치됨)
    # -------------------------------------------------------------------------
    launch_dir = os.path.dirname(os.path.abspath(__file__))
    package_dir = os.path.dirname(launch_dir)
    rviz_config_path = os.path.join(package_dir, 'config', 'integrated_view.rviz')

    # -------------------------------------------------------------------------
    # 2. 런치 인자(Launch Arguments) 선언
    # -------------------------------------------------------------------------
    frame_id_arg = DeclareLaunchArgument(
        'frame_id',
        default_value='base_link',
        description='마커 기준 좌표계 (기본값: base_link)'
    )

    publish_rate_arg = DeclareLaunchArgument(
        'publish_rate',
        default_value='10.0',
        description='마커 발행 주기(Hz)'
    )

    obstacle_dist_arg = DeclareLaunchArgument(
        'obstacle_distance',
        default_value='4.0',
        description='전방 가상 장애물 초기 거리(m)'
    )

    # -------------------------------------------------------------------------
    # 3. 커스텀 마커 퍼블리셔 노드 선언
    # -------------------------------------------------------------------------
    marker_node = Node(
        package='rviz_visualization',
        executable='custom_marker_publisher',
        name='custom_marker_publisher',
        output='screen',
        emulate_tty=True,
        parameters=[{
            'frame_id': LaunchConfiguration('frame_id'),
            'publish_rate': LaunchConfiguration('publish_rate'),
            'obstacle_distance': LaunchConfiguration('obstacle_distance')
        }]
    )

    # -------------------------------------------------------------------------
    # 3-1. odom -> base_link 정적 TF 발행
    #      (TF 트리에 base_link 프레임이 존재해야 RViz2 Global Status 경고가 사라짐)
    # -------------------------------------------------------------------------
    static_tf_node = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='odom_to_base_link',
        arguments=['--frame-id', 'odom', '--child-frame-id', 'base_link'],
        output='screen'
    )

    # -------------------------------------------------------------------------
    # 4. RViz2 시각화 프로세스 실행 선언
    # -------------------------------------------------------------------------
    rviz_process = ExecuteProcess(
        cmd=['rviz2', '-d', rviz_config_path],
        output='screen'
    )

    # -------------------------------------------------------------------------
    # 5. 런치 시작 로그 메시지
    # -------------------------------------------------------------------------
    start_log = LogInfo(
        msg='[오토모티브SW프로그래밍 9주차] RViz2 심화 시각화 시스템을 가동합니다.'
    )

    # -------------------------------------------------------------------------
    # 6. 실행 디스크립션 반환
    # -------------------------------------------------------------------------
    return LaunchDescription([
        frame_id_arg,
        publish_rate_arg,
        obstacle_dist_arg,
        start_log,
        static_tf_node,
        marker_node,
        rviz_process
    ])
