#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

#define SERVOMIN  0 // This is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX  2000 // This is the 'maximum' pulse length count (out of 4096)
#define USMIN  600 // This is the rounded 'minimum' microsecond length based on the minimum pulse of 150
#define USMAX  2400 // This is the rounded 'maximum' microsecond length based on the maximum pulse of 600
#define BUTTON_PIN 8

uint8_t servonum = 0;
unsigned long debounceDuration = 50; // millis
unsigned long lastTimeButtonStateChanged = 0;
byte lastButtonState = LOW;
int time_midpoint_us = 0.5*(USMIN + USMAX);

void setup() 
{
  Serial.begin(9600);
  //Serial.println("16 channel PWM test!");

  // amke sure pullup resistor enabled
  pinMode(BUTTON_PIN, INPUT_PULLUP);

  bool status = pwm.begin();
  //Serial.println(status);
  pwm.setOscillatorFrequency(27000000);
  pwm.setPWMFreq(50);  
  
  // turn off to start
  turn_off_servo();

  // get an accurate measurement of what stae the button is in
  lastButtonState = digitalRead(BUTTON_PIN);
  //Serial.print("initial value for lastButtonState = ");
  //Serial.println(lastButtonState);

  delay(10);
}

void turn_off_servo()
{
  pwm.setPWM(servonum, 0, 4096);
}

void loop() 
{

  byte buttonState = digitalRead(BUTTON_PIN);
  
  // choose a 0 = rotate clockwise or 1 = rotate counterclockwise
  int random_num = random(0, 1);
  
  if (millis() - lastTimeButtonStateChanged > debounceDuration)
  {
    if (buttonState != lastButtonState) 
    {
      lastTimeButtonStateChanged = millis();
      lastButtonState = buttonState;
      
      if (buttonState == HIGH) 
      {
        //Serial.println("Button released");
        turn_off_servo();
      }
      else if (buttonState == LOW)
      {
        //Serial.println("Button pressed");

        // Send a signal to the RPi that the button
	// was pressed so that in addition to R2D2
	// turning, he will also play a sound. I'm sending
	// the number 18 b/c I need to send something and it
	// was in an online example I am following
	Serial.write(18);

        int random_time_us;
        if (random_num == 0)
        {
          // choose a random value to rotate in time
          random_time_us = random(USMIN, time_midpoint_us);
        }
        else if (random_num == 1)
        {
          // choose a random value to counterrotate in time
          random_time_us = random(time_midpoint_us, USMAX);
        }

        pwm.writeMicroseconds(servonum, random_time_us);
        delay(10);
      }
    }
  }
}
