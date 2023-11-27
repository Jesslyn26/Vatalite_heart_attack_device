import urequests
from machine import SoftI2C, Pin
from sh1106 import SH1106_I2C

i2c= SoftI2C(scl=Pin(17), sda=Pin(16))
oled = SH1106_I2C(128, 64, i2c)
i2c.scan()

def send_notification():
    webhook_key = "evYXz13yB6lDfczx-WBgnrR98nHjGans6byiabyhMf2"
    url = f"https://maker.ifttt.com/trigger/is_it_heart_attack/with/key/{webhook_key}"
    response = urequests.request("GET", url)
    if response.status_code == 200:
        print("Notification sent successfully!")
    else:
        print("Failed to send notification.")
       
    response.close()

        
def send_sms(address, name):
    webhook_key = "evYXz13yB6lDfczx-WBgnrR98nHjGans6byiabyhMf2"
    url = f"https://maker.ifttt.com/trigger/detected_heart_attack/with/key/{webhook_key}"
    payload = {'value1': address, 'value2': name}
    response = urequests.post(url, json=payload)
    
    if response.status_code == 200:
        print("SMS sent successfully")
        oled.fill(0)
        oled.text("SMS sent!!", 0, 0,500)
        oled.show()
    else:
        print("Error sending SMS")
     
    response.close()
        
    
    