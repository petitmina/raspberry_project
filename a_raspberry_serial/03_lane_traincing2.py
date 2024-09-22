import cv2
import numpy as np
import serial
import time

# 아두이노와 직렬 연결 (포트 확인 필요)
arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
time.sleep(2)  # 직렬 통신 안정화 대기

# 카메라 초기화
cap = cv2.VideoCapture(0)  # 웹캠을 사용하는 경우, 0은 기본 카메라

def send_command(command):
    arduino.write(command.encode())  # 아두이노에 명령 전송

def process_image(frame):
    # 이미지를 그레이스케일로 변환
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 가우시안 블러 적용 (노이즈 제거)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # 캐니 엣지 검출
    edges = cv2.Canny(blur, 50, 150)

    # 관심 영역(ROI) 설정 (이미지 아래쪽에 차선이 있을 것으로 가정)
    height, width = edges.shape
    mask = np.zeros_like(edges)
    roi = np.array([[(0, height), (width // 2, height // 2), (width, height)]], dtype=np.int32)
    cv2.fillPoly(mask, roi, 255)
    cropped_edges = cv2.bitwise_and(edges, mask)

    # 허프 변환으로 선 검출
    lines = cv2.HoughLinesP(cropped_edges, 1, np.pi/180, 100, minLineLength=50, maxLineGap=50)

    return lines

def detect_lane_position(lines, frame):
    # 차선 방향을 검출하고 차가 중앙에 있는지 확인
    left_lines = []
    right_lines = []
    
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            slope = (y2 - y1) / (x2 - x1) if (x2 - x1) != 0 else 0  # 기울기 계산
            
            # 왼쪽 차선일 경우 (기울기가 음수)
            if slope < 0 and x1 < frame.shape[1] // 2:
                left_lines.append(line)
                cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
            # 오른쪽 차선일 경우 (기울기가 양수)
            elif slope > 0 and x1 >= frame.shape[1] // 2:
                right_lines.append(line)
                cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
    
    return left_lines, right_lines

def control_vehicle(left_lines, right_lines, frame):
    width = frame.shape[1]
    center_of_lane = width // 2

    if len(left_lines) > 0 and len(right_lines) > 0:
        # 차선 중앙 계산 (왼쪽과 오른쪽 차선의 중간값)
        left_x = np.mean([line[0][0] for line in left_lines])
        right_x = np.mean([line[0][0] for line in right_lines])
        lane_center = (left_x + right_x) // 2

        # 차량이 차선 중앙에 있는지 확인
        if lane_center < center_of_lane - 10:
            send_command('l')  # 왼쪽으로 이동
            print("Move left")
        elif lane_center > center_of_lane + 10:
            send_command('r')  # 오른쪽으로 이동
            print("Move right")
        else:
            send_command('f')  # 직진
            print("Move forward")
    else:
        send_command('s')  # 차선을 인식하지 못한 경우 멈춤
        print("Stop")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 이미지 처리 및 차선 검출
    lines = process_image(frame)

    # 왼쪽과 오른쪽 차선 검출
    left_lines, right_lines = detect_lane_position(lines, frame)

    # 차량 제어 (차선 중앙 유지)
    control_vehicle(left_lines, right_lines, frame)

    # 결과 이미지를 화면에 표시 (디버깅용)
    cv2.imshow('Lane Detection', frame)

    # ESC 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
