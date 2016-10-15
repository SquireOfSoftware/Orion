#define trigPin 13
#define echoPin 12
#define led 11
#define led2 10

void setup() {
  Serial.begin (9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(led, OUTPUT);
  pinMode(led2, OUTPUT);
}

void loop() {
  long duration, distance;
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH, 23200); //Timeout if pulse corresponds to distance > 4m
  distance = duration / 58; //WILL REQUIRE CALIBRATION  
  if (distance == 0)
  {
    distance = 400;
  }  
  Serial.print(distance);
  Serial.println(" cm");
  
  delay(500);
}
