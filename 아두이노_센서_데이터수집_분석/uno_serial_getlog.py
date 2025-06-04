#!pip install pyserial
import serial
import csv
from datetime import datetime
import time

# 시리얼 포트 설정 (아두이노가 연결된 포트로 변경 필요)
SERIAL_PORT = '/dev/cu.usbserial-14110'  # macOS의 경우
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
            while True:
                if ser.in_waiting:
                    data = ser.readline().decode('utf-8').strip()
                    csv_writer.writerow([data])
                    print(f"{data}")
                    csvfile.flush()
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