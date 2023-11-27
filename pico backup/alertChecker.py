from machine import SoftI2C, Pin
import RPi.GPIO as GPIO
import utime
import ifttt_send_message
import touch_capacitive_checker
import map_location
from sh1106 import SH1106_I2C
import main

i2c= SoftI2C(scl=Pin(17), sda=Pin(16))
oled = SH1106_I2C(128, 64, i2c)
i2c.scan()

# Assigning the vibrator pins 
vibration_pin = 15
GPIO.setmode(GPIO.BCM)
GPIO.setup(vibration_pin, GPIO.OUT)

# Function for the vibrator to vibrate
def vibrate():
    GPIO.output(vibration_pin, GPIO.HIGH)
    utime.sleep(0.5)
    GPIO.output(vibration_pin, GPIO.LOW)
    
    
    
# Function to check if it is a possibl3e heart attack or not
def alertCheck(HR,spo2, Hr,Spo2s):
    if (HR > 100 or  HR < 90):
        if (spo2 < 95):
            print("heart attack is identified")
            vibrate()
            oled.fill(0)
            oled.text("Are you having a ", 0, 0,500)
            oled.text("heart attack ???",0,10,500)
            oled.show()
            utime.sleep(5)
            oled.fill(0)
            
            oled.text("Please press the ", 0, 0,500)
            oled.text("button if you ",0,10,500)
            oled.text("are not having a",0,20,500)
            oled.text("heart attack...",0,30,500)
            oled.show()
            
            ifttt_send_message.send_notification()
            is_user_fine = touch_capacitive_checker.check_button()
            
            if is_user_fine == False:
                oled.fill(0)
                oled.text("Getting location...", 0, 0,500)
                oled.show()
                
                latitude,longitude = map_location.get_lat_long()
                address = map_location.get_address(latitude,longitude)
                
                oled.fill(0)
                oled.text("Sending SMS...", 0, 0,500)
                oled.show()
                utime.sleep(2)
                
                name = 'Jesslyn'
                sending_SMS = ifttt_send_message.send_sms(address,name)
                print("SMS sent !")
                utime.sleep(2)
                
                oled.fill(0)
                oled.text("Power off...", 0, 0,500)
                oled.show()
                oled.fill(0)
            
                touch_capacitive_checker.check_for_response()
                
                
                
            else:
                oled.fill(0)
                oled.text("Sorry it was a", 0, 0,500)
                oled.text("false alarm...",0,10,500)
                oled.show()
                utime.sleep(5)
                
                
                main.main(True,[],[], 5)
                
            
    else:
        pass
            