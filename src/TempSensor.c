#define MIN_TEMP 17.5
#define MAX_TEMP 22.5

// how many samples we take
const int nb_samples = 10;

// by default, wait for 60 seconds between samples
unsigned long timer = 60000;

const int redLed = 2;
const int greenLed = 3;
const int blueLed = 4;

bool initalReadingDone = false;

void setup()
{
  pinMode(redLed, OUTPUT);
  pinMode(greenLed, OUTPUT);
  pinMode(blueLed, OUTPUT);
  Serial.begin(9600);
  
  while (!Serial.available())
  {
    digitalWrite(redLed, LOW);
    digitalWrite(greenLed, LOW);
    digitalWrite(blueLed, LOW);
    delay(100);
  }
  
  if (Serial.available())
  {
    digitalWrite(redLed, HIGH);
    digitalWrite(greenLed, HIGH);
    digitalWrite(blueLed, HIGH);
    float rectimer = Serial.parseFloat();
    if (rectimer > 0) {
      // we received it in seconds, we need to convert it in milliseconds
      timer = rectimer * 1000;
    }
  }
  Serial.print("Timer received: ");
  Serial.print(timer);
  Serial.println(" milliseconds");
  delay(30);
  Serial.flush();
}

void loop()
{
  if (!initalReadingDone) {
    // First sample
    float sensorValue = analogRead(A0) * 500 / 1023;
    update_leds(sensorValue);
    //Serial.print("First sample: ");
    Serial.println(sensorValue);
    delay(30);
    Serial.flush();
    initalReadingDone = true;
    return;
  }
  
  float avg_temp = 0;
  float added_temp = 0;
  for (int i = 0; i < nb_samples; i++)
  {
    float sensorValue = analogRead(A0);
    added_temp += (sensorValue * 500) / 1023;
    delay((float)timer / nb_samples);
  }
  avg_temp = added_temp / nb_samples;

  //int sensorReading = analogRead(A0);
  //avg_temp = map(sensorReading, 0, 1023, 15, 25);

  update_leds(avg_temp);
  Serial.println(avg_temp);
  Serial.flush();
}

void update_leds(float avg_temp)
{
  // blue: below min temperature
  if (avg_temp < MIN_TEMP) {
    digitalWrite(blueLed, HIGH);
  } else {
    digitalWrite(blueLed, LOW);
  }

  // red: max over temperature
  if (avg_temp > MAX_TEMP) {
    digitalWrite(redLed, HIGH);
  } else {
    digitalWrite(redLed, LOW);
  }

  // green: temperature's ok
  if (avg_temp >= MIN_TEMP && avg_temp <= MAX_TEMP) {
    digitalWrite(greenLed, HIGH);
  } else {
    digitalWrite(greenLed, LOW);
  }
}
