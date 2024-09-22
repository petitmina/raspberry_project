#define int ENA = 9; // 모터 A 속도 제어
#define int ENB = 10; // 모터 A 속도 제어
#define int IN1 = 7;  // 모터 A 제어 핀 1
#define int IN2 = 6;  // 모터 A 제어 핀 2
#define int IN3 = 5;  // 모터 B 제어 핀 1
#define int IN4 = 4; // 모터 B 제어 핀 2

void setup(){
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  // 모터 속도를 기본값으로 설정
  analogWrite(ENA, 255);  // 모터 A 최대 속도
  analogWrite(ENB, 255);  // 모터 B 최대 속도
}

// 모터 제어 함수
void moveForward() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
}

void moveBackward() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
}

void turnLeft() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
}

void turnRight() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
}

void stopMotors() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
}

void loop(){
  // 예시로 앞, 뒤, 좌, 우로 이동하고 멈추는 코드
  moveForward();  // 앞으로 이동
  delay(2000);    // 2초간 이동
  stopMotors();   // 멈춤
  delay(1000);    // 1초 대기

  moveBackward(); // 뒤로 이동
  delay(2000);    // 2초간 이동
  stopMotors();   // 멈춤
  delay(1000);    // 1초 대기

  turnLeft();     // 왼쪽으로 회전
  delay(1000);    // 1초간 이동
  stopMotors();   // 멈춤
  delay(1000);    // 1초 대기

  turnRight();    // 오른쪽으로 회전
  delay(1000);    // 1초간 이동
  stopMotors();   // 멈춤
  delay(1000);    // 1초 대기
  }
