import processing.serial.*;

Serial myPort;
int[] values = new int[4];

void setup() {
  size(800, 600);
  println(Serial.list());
  myPort = new Serial(this, Serial.list()[0], 9600);
  myPort.bufferUntil('\n');
}

void draw() {
  background(255);
  float barWidth = width / 8.0;
  for (int i = 0; i < 4; i++) {
    float xPos = (i * 2 + 1) * barWidth;
    float barHeight = map(values[i], 0, 1023, 0, height);
    rect(xPos, height - barHeight, barWidth, barHeight);
  }
}

void serialEvent(Serial myPort) {
  String data = myPort.readStringUntil('\n');
  if (data != null) {
    data = data.trim();
    String[] parts = split(data, ' ');
    if (parts.length == 4) {
      for (int i = 0; i < 4; i++) {
        values[i] = int(parts[i]);
      }
    }
  }
}