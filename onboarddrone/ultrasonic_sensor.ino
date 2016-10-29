#define pinoffset 2 //pin assignments aternate between trigger and echo for each sensor from this point
#define numOfSensors 4
#define maxDistance 400 //maximum distance to probe, in cm
#define microsecPerCm 58 //from datasheet, may need adjustment

int timeout = maxDistance * microsecPerCm;
String input;
String distances;
String output;
bool ready = false;

void setup() {
  input.reserve(200);  
  pinMode(2, OUTPUT);
  pinMode(3, INPUT);
  pinMode(4, OUTPUT);
  pinMode(5, INPUT);
  pinMode(6, OUTPUT);
  pinMode(7, INPUT);
  pinMode(8, OUTPUT);
  pinMode(9, INPUT);

  Serial.begin (115200); //shield can apparently do 230400, may be worth trying

  Serial.print("AT+IPR=115200\r\n"); //sets baud rate, don't care about output for now
  Serial.readStringUntil('\n');
  Serial.readStringUntil('\n');

  Serial.print("AT+CWMODE=1\r\n"); //sets wifi to station (client) mode, don't care about output for now
  Serial.readStringUntil('\n');
  Serial.readStringUntil('\n');
  
  while (!ready) //these loops unravel once connection process completes
  {
    Serial.print("AT+CWJAP=\"drone_net\",\"\"\r\n");
    input = Serial.readStringUntil('\n');
    if (input.startsWith("WIFI CONNECTED"))
    {
      while (!ready)
      {
        input = Serial.readStringUntil('\n');
        if (input.startsWith("WIFI GOT IP"))
        {
          while (!ready)
          {
            input = Serial.readStringUntil('\n');
            input = Serial.readStringUntil('\n');
            if (input.startsWith("OK"))
            {
              ready = true;
            }            
          }
        }
      }      
    }
  }

  ready = false;
  while (!ready)
  {
    Serial.print("AT+CIPSTART=\"UDP\",\"192.168.1.2\",5556\r\n");
    input = Serial.readStringUntil('\n');
    if (input.startsWith("CONNECT"))
    {
      while (!ready)
      {
        input = Serial.readStringUntil('\n');
        input = Serial.readStringUntil('\n');
        if (input.startsWith("OK"))
        {
          ready = true;
        }
      }
    }
  }  
}

void loop() {
  int distance[numOfSensors];
  distances = "";
  output = "AT+CIPSEND=";
  
  for (int i = pinoffset; i < numOfSensors; i+2)
  {
    digitalWrite(i, LOW);
    delayMicroseconds(2);
    digitalWrite(i, HIGH);
    delayMicroseconds(10);
    digitalWrite(i, LOW);
    distance[(i/2)-1] = pulseIn(i+1, HIGH, timeout) / microsecPerCm; //Timeout if pulse width exceeds max distance
    if (distance[(i/2)-1] == 0)
    {
      distance[(i/2)-1] = maxDistance; //recalculate above for different max distance
    }
    distances += distance[(i/2)-1] + " ";
    //distances += " ";   
  }

  output += distances.length() + "\r\n";
  Serial.print(output);  
  input = Serial.readStringUntil('>');
  Serial.print(distances);    
}
