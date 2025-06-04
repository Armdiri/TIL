#include <DHT.h>
#define DATAPIN A0
DHT myDHT11(DATAPIN, DHT11);

void(* resetFunc) (void) = 0; //declare reset function @ address 0

void setup() {
  Serial.begin(9600);
  myDHT11.begin();
  pinMode(A1,INPUT);
  pinMode(2,INPUT); // 디지털소리 입력 신호
}

void loop() {
  float fTempC;
  float fTempF;
  float fHumid;
  float fHeatIndex;
  int fCds = 0;
  int fSound;
  int fDSound;
  float fDiscomfort;

  fTempC = myDHT11.readTemperature(false);
  fTempF = myDHT11.readTemperature(true);
  fHumid = myDHT11.readHumidity(false);
  fHeatIndex = myDHT11.computeHeatIndex(fTempC,fHumid,false);
  fDiscomfort = (1.8 * fTempC)-0.55*(1-(fHumid/100))*(1.8 * fTempC-26)+36; //1.8 x 기온 - 0.55 x (1 - 습도) x (1.8 x 기온 - 26) + 32 < 80

  Serial.print(fTempC);
  Serial.print(",");
  Serial.print(fTempF);
  Serial.print(",");
  Serial.print(fHumid);
  Serial.print(",");
  Serial.print(fHeatIndex);
  Serial.print(",");
  Serial.print(fDiscomfort);
  Serial.print(",");

  fCds = analogRead(A1);
  Serial.print(fCds);
  Serial.print(",");

  fSound = analogRead(A3);
  fDSound = digitalRead(2);
  Serial.print(fSound);
  Serial.println("");
  delay(3000);
}
