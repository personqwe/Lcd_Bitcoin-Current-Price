[](https://git.huconn.com/topst-project/bitcoin-current-price)

[Cryptocurrency Prices, Portfolio, Forum, Rankings](https://www.cryptocompare.com/)

Cryptocurrency API를 사용하여 현재 비트코인 가격을 가져왔습니다.

해당 홈페이지에 접속하여 회원 가입 후 API를 발급받아야 합니다.

GND = GND pin

VCC - 5V pin

SDA = GPIO SDA I2C pin

SCL = GPIO SCL I2C pin

VSCode 설치 방법:

1. 다음 명령어를 실행하세요: wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
2. packages.microsoft.gpg 파일을 /etc/apt/trusted.gpg.d/ 디렉토리에 복사합니다: sudo install -o root -g root -m 644 packages.microsoft.gpg /etc/apt/trusted.gpg.d/
3. 다음 명령어를 실행하여 /etc/apt/sources.list.d/vscode.list 파일을 만듭니다: sudo sh -c 'echo "deb [arch=arm64] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
4. 패키지 목록을 업데이트합니다: sudo apt update
5. VSCode를 설치합니다: sudo apt install code
6. 

실행 방법:

다음 명령어를 입력하세요:
code --no-sandbox --user-data-dir=/path/to/alternate/user/data/dir

진행 방법:

- pip을 설치하려면 다음 명령을 실행하십시오.

```
sudo apt install python3-pip

```

- I2C 통신을 위해 smbus를 설치하십시오.

```jsx
pip install smbus
```

- http통신을 위한 requests와 LCD제어를 위한 RPLCD를 설치하십시오

```
pip install requests
pip install RPLCD
```

```python
import smbus
import time
from RPLCD.i2c import CharLCD
import requests

API_KEY = "#####################################################"
#이전에 발급받은 API를 사용
def get_bitcoin_price():
    url = f"https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=KRW&api_key={API_KEY}"
#원화가 아닌 달러로 하려면 KRW를 USD로 변경
    response = requests.get(url)
    data = response.json()
    bitcoin_price = data["KRW"] #json데이터의 구조는 홈페이지에서 확인
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
```

![Alt text](image.png)