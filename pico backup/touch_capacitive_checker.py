from machine import SoftI2C, Pin
import utime
from sh1106 import SH1106_I2C
import main

i2c= SoftI2C(scl=Pin(17), sda=Pin(16))
oled = SH1106_I2C(128, 64, i2c)
i2c.scan()
touch_pin = Pin(6, Pin.IN)

def check_button():
    # Set the GPIO pin number
    user_fine = True

    # Start the timer
    start_time = utime.time()

    # Wait for touch within the timeout period
    while utime.time() - start_time < 10:
        # Check the touch status
        if Pin.value(touch_pin) == 1:
            # Touch detected
            user_fine = True
            print("Sorry wrong alert...")
            break

    # Timeout reached without touch
    if utime.time() - start_time >= 10:
        print()
        print("No touch is detected within 30 seconds.")
        user_fine = False
        
    return user_fine

def check_for_response():
    
    while True:
        # Read the state of the touch sensor
        # Check if touch is detected
        if Pin.value(touch_pin) == 1:
            print()
            print("Touch detected!")
            utime.sleep(5)
            if Pin.value(touch_pin) == 1:
                
                oled.fill(0)
                oled.text("Welcome back!!!", 0, 0,500)
                oled.show()
                utime.sleep(2)
                main.main(True,[],[], 5)
                
            else:
                pass
                utime.sleep(0.50)
                

