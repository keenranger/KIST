// 블루투스 통신을 하기 위해 SoftwareSerial 라이브러리를 사용함.
#include <SoftwareSerial.h>
#include "I2Cdev.h"
#include "MPU6050.h"
#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
#include "Wire.h"
#endif
MPU6050 accelgyro;
int16_t ax, ay, az;
int16_t gx, gy, gz;


SoftwareSerial BTSerial(4, 7); // SoftwareSerial(RX, TX), 통신을 하기 위한 RX,TX 연결 핀번호
byte buffer[1024];    // 데이터를 수신 받을 자료를 저장할 버퍼
int bufferPosition;   // 버퍼에 데이터를 저장할 때 기록할 위치

void setup() {
#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
  Wire.begin();
#elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
  Fastwire::setup(400, true);
#endif

  BTSerial.begin(115200); // 블루투스 모듈 초기화, 블르투스 연결
  Serial.begin(115200);   // 시리얼 모니터 초기화, pc와 연결
  bufferPosition = 0;   // 버퍼 위치 초기화

  Serial.println("Initializing I2C devices...");
  accelgyro.initialize();
  Serial.println("Testing device connections...");
  Serial.println(accelgyro.testConnection() ? "MPU6050 connection successful" : "MPU6050 connection failed");

}

void loop() {
  accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

  BTSerial.print(ax); BTSerial.print("\t");
  BTSerial.print(ay); BTSerial.print("\t");
  BTSerial.print(az); BTSerial.print("\t");
  BTSerial.print(gx); BTSerial.print("\t");
  BTSerial.print(gy); BTSerial.print("\t");
  BTSerial.println(gz);
}

