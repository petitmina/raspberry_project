import cv2
import numpy as np
import serial
import time

# 아두이노와 직렬 연결 (라즈베리파이의 직렬 포트를 확인하고 수정)
arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
time.sleep(2)  # 직렬 통신 안정화 대기

# 카메라 초기화
cap = cv2.VideoCapture(0)  # 웹캠을 사용하는 경우, 0은 기본 카메라

def send_command(command):
    arduino.write(command.encode())  # 명령을 아두이노로 전송

def process_image(frame):
    # 이미지를 그레이스케일로 변환
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 가우시안 블러 적용 (노이즈 제거)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # 캐니 엣지 검출
    edges = cv2.Canny(blur, 50, 150)

    # 관심 영역(ROI) 설정 (이미지 아래 부분에만 차선이 있을 것으로 가정)
    height, width = edges.shape
    mask = np.zeros_like(edges)
    roi = np.array([[(0, height), (width // 2, height // 2), (width, height)]], dtype=np.int32)
    cv2.fillPoly(mask, roi, 255)
    cropped_edges = cv2.bitwise_and(edges, mask)

    # 허프 변환으로 선 검출
    lines = cv2.HoughLinesP(cropped_edges, 1, np.pi/180, 100, minLineLength=50, maxLineGap=50)

    return lines

def detect_lane_direction(lines, frame):
    # 차선 방향 계산
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            # 검출된 차선을 화면에 그리기
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)

        # 기울기 분석을 통해 차량이 이동해야 할 방향 결정
        # 예를 들어, 차선이 왼쪽으로 기울면 왼쪽으로 회전
        left_lines = [line for line in lines if line[0][0] < frame.shape[1] // 2]
        right_lines = [line for line in lines if line[0][0] >= frame.shape[1] // 2]

        if len(left_lines) > len(right_lines):
            send_command('l')  # 왼쪽으로 회전
            print("Turn left")
        elif len(right_lines) > len(left_lines):
            send_command('r')  # 오른쪽으로 회전
            print("Turn right")
        else:
            send_command('f')  # 앞으로 직진
            print("Move forward")
    else:
        send_command('s')  # 차선을 인식하지 못하면 멈춤
        print("Stop")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 이미지 처리 및 차선 검출
    lines = process_image(frame)
    
    # 차선 방향에 따라 명령 전송
    detect_lane_direction(lines, frame)

    # 결과 이미지를 화면에 표시 (디버깅용)
    cv2.imshow('Lane Detection', frame)

    # ESC 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
