#include <Arduino.h>
#include <Servo.h>

// Functions
void Dive (int rudder_delay);
void Surface (int rudder_delay);
void Right (int rudder_delay);
void Left (int rudder_delay);
void Stall (int rudder_delay);


int x_key = A1;
int y_key = A2;
int x_pos;
int y_pos;
int x_pos_diff;
int y_pos_diff;
// Constants
//  Delay between rudder movements
const int rudder_delay = 15;
//  Servo Positions
const int pos_H = 525;
const int pos_L = 475;
const int pos_max = 1023;
const int pos_min = 0;
const int pos_default = 505;
// Servo Degrees
const int deg_H = 135;
const int deg_L = 45;
const int deg_default = 90;





Servo servo1, servo2, servo3, servo4; // create servo object to control a servo


void setup() {
    Serial.begin(9600);
    pinMode(x_key, INPUT);
    pinMode(y_key, INPUT);
    servo1.attach(3), servo2.attach(5), servo3.attach(6), servo4.attach(9);
    // Servo 1: bottom right, Servo 2: top right, Servo 3: top left, Servo 4: bottom left

}
void loop () {
    // Analog Read
    x_pos = analogRead(x_key);
    y_pos = analogRead(y_key);
    Serial.print("X: ");
    Serial.print(x_pos);
    Serial.print(" Y: ");
    Serial.println(y_pos);
    // Default: X: 504 Y: 505
    // UP: 1023, Down: 0, Left: 1023, Right: 0
    x_pos_diff = abs(pos_default - x_pos);
    y_pos_diff = abs(pos_default - y_pos);
    //difference between default and current position to determine direction (not needed for Gav's controller)
    if ((y_pos_diff > x_pos_diff)) {
        if (y_pos > pos_H) {
            Dive(rudder_delay);
        }

        if (y_pos < pos_L) {
            Surface(rudder_delay);
        }
    }

    if ( (x_pos_diff > y_pos_diff)) {
        if (x_pos < pos_L) {
            Right(rudder_delay);
        }

        if (x_pos > pos_H) {
            Left(rudder_delay);
        }
    }

    if (y_pos < pos_H && y_pos > pos_L && x_pos < pos_H && x_pos > pos_L) {
     
            Stall(rudder_delay);
    }

}
    void Dive (int rudder_delay) {
        servo1.write(map(y_pos, pos_H, pos_max, deg_L, deg_H)); // sets the servo position according to the scaled value
        servo2.write(map(y_pos, pos_H, pos_max, deg_L, deg_H));
        servo3.write(map(y_pos, pos_H, pos_max, deg_H, deg_L));
        servo4.write(map(y_pos, pos_H, pos_max, deg_H, deg_L));
        delay(rudder_delay);
    }
    
    void Surface (int rudder_delay) {
        servo1.write(map(y_pos, pos_min, pos_L, deg_L, deg_H)); // sets the servo position according to the scaled value
        servo2.write(map(y_pos, pos_min, pos_L, deg_L, deg_H));
        servo3.write(map(y_pos, pos_min, pos_L, deg_H, deg_L));                             
        servo4.write(map(y_pos, pos_min, pos_L, deg_H, deg_L));
        delay(rudder_delay);
    }
                                                                                               
    void Right (int rudder_delay) {
        servo1.write(map(x_pos, pos_min, pos_L, deg_L, deg_H)); // sets the servo position according to the scaled value
        servo2.write(map(x_pos, pos_min, pos_L, deg_H, deg_L));
        servo3.write(map(x_pos, pos_min, pos_L, deg_H, deg_L));
        servo4.write(map(x_pos, pos_min, pos_L, deg_L, deg_H));
        delay(rudder_delay);
    }

    void Left (int rudder_delay) {
        servo1.write(map(x_pos, pos_H, pos_max, deg_L, deg_H)); // sets the servo position according to the scaled value
        servo2.write(map(x_pos, pos_H, pos_max, deg_H, deg_L));
        servo3.write(map(x_pos, pos_H, pos_max, deg_H, deg_L));
        servo4.write(map(x_pos, pos_H, pos_max, deg_L, deg_H));
        delay(rudder_delay);
    }

    void Stall (int rudder_delay) {
        servo1.write(deg_default); // sets the servo position according to the scaled value
        servo2.write(deg_default);
        servo3.write(deg_default);
        servo4.write(deg_default);
        delay(rudder_delay);
    }


