#!/usr/bin/env bash
# 9주차 실습 자동 실행 스크립트 (WSL2 + ROS 2)
# 빌드 -> 런치 -> 실행화면 캡처 -> topic echo 로그 -> 노드 종료 후 잔상 제거 캡처
DIR="$(cd "$(dirname "$0")" && pwd)"
OUT="$DIR/results"; mkdir -p "$OUT"
exec > >(tee "$OUT/run_log.txt") 2>&1
echo "=== 환경 ==="; grep PRETTY /etc/os-release; ls /opt/ros
DISTRO=$(ls /opt/ros | head -1)
source /opt/ros/$DISTRO/setup.bash
echo "ROS_DISTRO=$ROS_DISTRO"
# WSLg + Ubuntu 26.04: Qt 가 Wayland 로 뜨면 OGRE 렌더 창 생성 실패 -> X11(xcb) 강제
export QT_QPA_PLATFORM=xcb

WS=~/ros2_ws
mkdir -p $WS/src
rm -rf $WS/src/rviz_visualization
cp -r "$DIR/rviz_visualization" $WS/src/
cd $WS
echo "=== colcon build ==="
colcon build --symlink-install --packages-select rviz_visualization 2>&1 | tee "$OUT/build_log.txt"
source install/setup.bash

capture() { powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$(wslpath -w "$DIR/capture_window.ps1")" -Title "RViz" -Out "$(wslpath -w "$OUT/$1")"; }

echo "=== ros2 launch ==="
set -m  # 잡 컨트롤: 백그라운드 프로세스가 SIGINT를 무시하지 않도록
ros2 launch rviz_visualization rviz_advanced.launch.py > "$OUT/launch_log.txt" 2>&1 &
LPID=$!
sleep 20
echo "=== 노드/토픽 확인 ==="
ros2 node list | tee "$OUT/node_list.txt"
ros2 topic info /visual_markers -v | tee "$OUT/topic_info.txt"
timeout 6 ros2 topic hz /visual_markers > "$OUT/topic_hz.txt" 2>&1
ros2 topic echo /visual_markers --once > "$OUT/topic_echo.txt" 2>&1
echo "=== 실행화면 캡처 ==="
capture 01_rviz_markers.png
sleep 2
capture 02_rviz_markers_animated.png
echo "=== 마커 노드 강제 종료 (Ctrl+C 와 동일한 SIGINT) ==="
pkill -INT -f "lib/rviz_visualization/custom_marker_publisher"
sleep 1.5
echo "--- 노드 종료 로그 ---"
sed 's/\x1b\[[0-9;]*m//g' "$OUT/launch_log.txt" | grep -a "custom_marker_publisher" | tail -3 | tee "$OUT/kill_log.txt"
capture 03_after_node_killed.png
ros2 node list --no-daemon | tee "$OUT/node_list_after_kill.txt"
echo "=== 종료 ==="
kill -INT $LPID 2>/dev/null; sleep 2; pkill -f rviz2
echo "=== git/gh 확인 ==="
git config --global user.name; git config --global user.email; which gh git
echo DONE
