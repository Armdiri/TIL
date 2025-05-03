# 아두이노를 이용한 데이터 수집 

### 주제 
- 수험생이 공부하기 좋은 최적의 장소를 찾기 
- 온도 : 베타파가 고루게 분포되는 20~23도가 최적
- 습도 : 40~60%
- 불쾌지수 : 1.8 x 기온 - 0.55 x (1 - 습도) x (1.8 x 기온 - 26) + 32 < 80
- 조도 : 300~500 lux
- 소음 : 50~70 dB

### 진행과정
- 대상선정 : 집, 공부방, 도서관, 야외 2~3군데 지정 데이터 수집 
- 로그데이터를 csv 로 저장 
- 데이터분석을 통한 최적의 장소 추출 

### 아두이노 세팅 
   ![회로도](과제설계.drawio.png)

### 아두이노 코딩 
- 온습도센서 DHT11 : 라이브러리 설치 DFRobot_DHT11 
```c
#include <DFRobot_DHT11.h>
DFRobot_DHT11 DHT;
#define DHT11_PIN 10

void setup() {
  Serial.begin(9600);
}

void loop() {
  DHT.read(DHT11_PIN);
  Serial.print("온도 : ")
  Serial.print(DHT.temperature);
  Serial.print("습도 : ");
  Serial.print(DHT.humidity);
  delay(1000);
}
```

- 조도센서 KY-018 코딩
```c
#define cds A0
float val = 0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  val = analogRead(cds);
  Serial.print(val);
  delay(1000);
}
```

- 고감도 소리센서 
```c
int sensor = A0;
int val;

void setup() {
  Serial.begin(9600);
  pinMode(sensor.INPUT);
}

void loop() {
  val = analogRead(sensor);
  Serial.println(val);
  delay(1000);
}
```

- 센서 데이터를 파이썬으로 읽어서 CSV 파일로 저장함 
```python 
import serial
import csv
from datetime import datetime
import time

# 시리얼 포트 설정 (아두이노가 연결된 포트로 변경 필요)
SERIAL_PORT = '/dev/tty.usbmodem14101'  # macOS의 경우
BAUD_RATE = 9600  # 아두이노의 Serial.begin() 값과 동일하게 설정

# CSV 파일 이름 설정 (현재 시간을 포함)
CSV_FILENAME = f'arduino_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'

def main():
    try:
        # 시리얼 포트 열기
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"시리얼 포트 {SERIAL_PORT}에 연결되었습니다.")
        
        # CSV 파일 열기
        with open(CSV_FILENAME, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            
            # 헤더 작성 (필요에 따라 수정)
            csv_writer.writerow(['Timestamp', 'Data'])
            
            print(f"데이터를 {CSV_FILENAME}에 저장 중...")
            print("프로그램을 종료하려면 Ctrl+C를 누르세요.")
            
            while True:
                if ser.in_waiting:
                    # 시리얼 데이터 읽기
                    data = ser.readline().decode('utf-8').strip()
                    
                    # 현재 시간과 데이터를 CSV에 기록
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    csv_writer.writerow([timestamp, data])
                    
                    # 콘솔에 출력 (옵션)
                    print(f"{timestamp}: {data}")
                    
                    # 파일 버퍼 플러시
                    csvfile.flush()
                
                # CPU 사용량을 줄이기 위한 작은 지연
                time.sleep(0.01)
                
    except serial.SerialException as e:
        print(f"시리얼 포트 오류: {e}")
    except KeyboardInterrupt:
        print("\n프로그램을 종료합니다.")
    finally:
        if 'ser' in locals():
            ser.close()
            print("시리얼 포트가 닫혔습니다.")

if __name__ == "__main__":
    main()
```