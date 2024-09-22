import serial
import time

# 시리얼 포트 설정 (포트는 자신의 환경에 맞게 설정)
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
time.sleep(2)  # 연결이 안정화될 때까지 잠시 대기

try:
    while True:
        # 사용자 입력 받기
        user_input = input("a를 입력하면 모터가 작동하고, b를 입력하면 멈춥니다: ")

        if user_input == 'a':
            ser.write('a')  # Arduino로 'a' 전송
            print("모터가 작동 중입니다.")
        elif user_input == 'b':
            ser.write('b')  # Arduino로 'b' 전송
            print("모터가 멈췄습니다.")
        else:
            print("올바른 명령어를 입력하세요. (a 또는 b)")
finally:
    ser.close()  # 프로그램 종료 시 시리얼 포트 닫기
