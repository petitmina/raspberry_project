int motorPin = 9;

void setup() {
  // put your setup code here, to run once:
  pinMode(motorPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available() > 0){
    char command = Serial.read();

    if(command == 'a'){
      digitalWrite(motorPin, HIGH);
    }
    else if(command = 'b'){
      digitalWrite(motorPin, Low);
    }
  }
}
