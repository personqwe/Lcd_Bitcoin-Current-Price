import smbus
import time
from RPLCD.i2c import CharLCD
import requests

API_KEY = "#####################################################"

def get_bitcoin_price():
    url = f"https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=KRW&api_key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    bitcoin_price = data["KRW"]
    return bitcoin_price


def display_bitcoin_price():
    # I2C 인터페이스 설정 (I2C 버스 번호는 Raspberry Pi 모델에 따라 다를 수 있습니다)
    bus = smbus.SMBus(1)

    # LCD 초기화 (0x27은 대부분의 16x2 I2C LCD 모듈에서 기본 주소이며, 주소가 0x3F인 경우도 있습니다.)
    lcd = CharLCD('PCF8574', 0x3F)

    while True:
        try:
            # 비트코인 가격 정보 가져오기
            bitcoin_price = get_bitcoin_price()

            # LCD에 가격 표시
            lcd.clear()
            lcd.write_string("Bitcoin Price:")
            lcd.cursor_pos = (1, 0)
            lcd.write_string(f"{bitcoin_price:.2f} KRW")  # 소수점 2자리까지 표시

        except Exception as e:
            # 오류 처리: API 호출 중에 문제가 발생한 경우 예외 처리
            lcd.clear()
            lcd.write_string("Price Error")

        # 1초마다 가격 업데이트
        time.sleep(1)

if __name__ == "__main__":
    display_bitcoin_price()