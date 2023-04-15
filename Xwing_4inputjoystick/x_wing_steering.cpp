#include <Arduino.h>
#include <Servo.h>

// Analog input pins
const int upPin = A0;
const int downPin = A1;
const int leftPin = A2;
const int rightPin = A3;

// Servo objects
Servo BRrudder;
Servo TRrudder;
Servo TLrudder;
Servo BLrudder;

// Servo pins
const int BottomRight1 = 3;
const int TopRight2 = 5;
const int TopLeft3 = 6;
const int BottomLeft4 = 9;


//Minimum value to be considered a valid input
const int lower_threshhold = 565;
const int rudder_delay = 15;

// Servos Degree limits
//Max degree limit
const int deg_H = 135;
//Min degree limit
const int deg_L = 45;

//Max analog input values all
const int MAX_U = 633;
const int MAX_D = 641;
const int MAX_L = 626;
const int MAX_R = 635;

// Create the AnalogSignals class
class AnalogSignals {
  private:
    const int movingWindowSize = 5;
    float Q = 0.5;  // Process noise covariance
    float R = 2;    // Measurement noise covariance

    // Variables for the moving average
    int window[4][5] = {0};

    // Variables for the Kalman filter
    float X[4] = {0};
    float P[4] = {1};

  public:
    int read(int pin) {
      return analogRead(pin);
    }

    int movingAverage(int pin) {
      int pinIndex = (pin - A0) % 4; // Determine the index for the current pin (0-3)

      // Shift the previous moving window values
      for (int i = movingWindowSize - 1; i > 0; i--) {
        window[pinIndex][i] = window[pinIndex][i - 1];
      }
      window[pinIndex][0] = read(pin);

      // Calculate the average of the moving window values
      int sum = 0;
      for (int i = 0; i < movingWindowSize; i++) {
        sum += window[pinIndex][i];
      }
      return sum / movingWindowSize;
    }

    int kalmanFilter(int pin, float smoothedValue) {
      int pinIndex = (pin - A0) % 4; // Determine the index for the current pin (0-3)

      float K = P[pinIndex] / (P[pinIndex] + R); // Calculate the Kalman gain
      X[pinIndex] = X[pinIndex] + K * (smoothedValue - X[pinIndex]); // Update the filtered value
      P[pinIndex] = (1 - K) * P[pinIndex] + Q; // Update the covariance matrix

      return static_cast<int>(X[pinIndex]);
    }
};

// Create an instance of the AnalogSignals class
AnalogSignals analogSignals;




void setup()
{
  //Serial test
  // Attach servos to pins
  BRrudder.attach(BottomRight1);
  TRrudder.attach(TopRight2);
  TLrudder.attach(TopLeft3);
  BLrudder.attach(BottomLeft4);

  // Set initial servo positions to 90 degrees
  BRrudder.write(90);
  TRrudder.write(90);
  TLrudder.write(90);
  BLrudder.write(90);
}

void loop() {
  // Apply the moving average on the analog input values
  int upValueAvg = analogSignals.movingAverage(upPin);
  int downValueAvg = analogSignals.movingAverage(downPin);
  int leftValueAvg = analogSignals.movingAverage(leftPin);
  int rightValueAvg = analogSignals.movingAverage(rightPin);

  // Apply the Kalman filter on the moving average values
  int upValueFiltered = analogSignals.kalmanFilter(upPin, upValueAvg);
  int downValueFiltered = analogSignals.kalmanFilter(downPin, downValueAvg);
  int leftValueFiltered = analogSignals.kalmanFilter(leftPin, leftValueAvg);
  int rightValueFiltered = analogSignals.kalmanFilter(rightPin, rightValueAvg);
  
    // Find the maximum value
    int maxValue = max(max(upValueFiltered, downValueFiltered), max(leftValueFiltered, rightValueFiltered));

    //Serial max value test
    

    // If the maximum value is greater than the lower threshhold, then we have a valid input
    if (maxValue > lower_threshhold ){

    // Set the servo positions

    //Dive
        if (maxValue == upValueFiltered)
        {
            BRrudder.write(map(upValueFiltered, lower_threshhold, MAX_U, deg_L, deg_H));
            TRrudder.write(map(upValueFiltered, lower_threshhold, MAX_U, deg_L, deg_H));
            TLrudder.write(map(upValueFiltered, lower_threshhold, MAX_U, deg_H, deg_L));
            BLrudder.write(map(upValueFiltered, lower_threshhold, MAX_U, deg_H, deg_L));
        }

        //Surface
        else if (maxValue == downValueFiltered)
        {
            BRrudder.write(map(downValueFiltered, lower_threshhold, MAX_D, deg_H, deg_L)); 
            TRrudder.write(map(downValueFiltered, lower_threshhold, MAX_D, deg_H, deg_L));
            TLrudder.write(map(downValueFiltered, lower_threshhold, MAX_D, deg_L, deg_H));                             
            BLrudder.write(map(downValueFiltered, lower_threshhold, MAX_D, deg_L, deg_H));
        }

        //Right
        else if (maxValue == rightValueFiltered)
        {
            BRrudder.write(map(rightValueFiltered, lower_threshhold, MAX_R, deg_H, deg_L));
            TRrudder.write(map(rightValueFiltered, lower_threshhold, MAX_R, deg_L, deg_H));
            TLrudder.write(map(rightValueFiltered, lower_threshhold, MAX_R, deg_L, deg_H));
            BLrudder.write(map(rightValueFiltered, lower_threshhold, MAX_R, deg_H, deg_L));
        }

        //Left
        else if (maxValue == leftValueFiltered)
        {
            BRrudder.write(map(leftValueFiltered, lower_threshhold, MAX_L, deg_L, deg_H)); // sets the servo position according to the scaled value
            TRrudder.write(map(leftValueFiltered, lower_threshhold, MAX_L, deg_H, deg_L));
            TLrudder.write(map(leftValueFiltered, lower_threshhold, MAX_L, deg_H, deg_L));
            BLrudder.write(map(leftValueFiltered, lower_threshhold, MAX_L, deg_L, deg_H));
        }
    }
    else {
       BRrudder.write(90);
       TRrudder.write(90);
       TLrudder.write(90);
       BLrudder.write(90); 
    }
    // Wait for the servo to settle
    delay(rudder_delay);
}