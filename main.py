from machine import SoftI2C, Pin
import alertChecker
from max30102 import MAX30102, spocalc
import utime
from sh1106 import SH1106_I2C
from time import sleep
import time
import wifi_iotc
import iotcentral
import touch_capacitive_checker
import gc

# assigning pins for the oled
i2c= SoftI2C(scl=Pin(17), sda=Pin(16))
oled = SH1106_I2C(128, 64, i2c)
i2c.scan()
    

# fucntion use to check if the device is properly worn of not
def dataCheck(sensor_check):
    #read the value of the red light
    red_check = sensor_check.pop_red_from_storage()
    
    #compare if the value is below 5000 or not.
    #Value will be above 5000 if it is worn
    if (red_check <=5000):
        available = False
    else:
        available = True
        
    return available
        

def main (is_first_reading, Spo2s,Hr, no_pulse):
    #assigning the pins for the sensor (MAX30102)
    my_SDA_pin = 12 
    my_SCL_pin = 13 
    global sensor
    heart_rate_i2c = SoftI2C(sda=Pin(my_SDA_pin),scl=Pin(my_SCL_pin))
    heart_rate_i2c.scan()
    sensor = MAX30102(heart_rate_i2c)
    
    #setting up sensor 
    sensor.setup_sensor()
    
    #settihng up the library to calculate heart rate and oxygen level
    spo2calc = spocalc.spo2Calc    
    
    
    while (True):
        # The check() method has to be continuously polled, to check if
        # there are new readings into the sensor's FIFO queue. When new
        # readings are available, this function will put them into the storage.
      
        sensor.check()

        # Check if the storage contains available samples
        if (sensor.available()):
           
         # Check wheater the device is worn
         read_available = dataCheck(sensor)
         
         # It will calculate heart rate and oxygen level if the device is worn
         if (read_available == True):
             sensor.check()
            
             # Print calculating if the user just booted the device or jus t worn it properly
             if (is_first_reading == True):
                 no_pulse = 5
                 print("Calculating HR and oxygen level...")
                 print()
                 oled.fill(0)
                 oled.text("Calculating HR ", 0,0,1000)
                 oled.text("and oxygen level", 0,10,1000)
                 oled.text("...", 0,21,1000)
                 oled.show()
                 is_first_reading = False
                 utime.sleep(2)
                
             # Reading the 1st valley, 1st peak, 2nd valley, and 2nd peak for red light
             # vally = lowest value
             # Peak = higest
             # Please refer to the report for better understanding
             
             red_valley_time1, red_valley_value1 = spo2calc.getValleyRed(sensor)
             red_peak_time1, red_peak_value1 = spo2calc.getPeaksRed(sensor)
             red_valley_time2, red_valley_value2 = spo2calc.getValleyRed(sensor)
             red_peak_time2, red_peak_value2 = spo2calc.getPeaksRed(sensor)
             
             # Reading the 1st valley, 1st peak, 2nd valley, and 2nd peak for infrared light
             ir_valley_time1, ir_valley_value1 = spo2calc.getValleyIr(sensor)
             ir_peak_time1, ir_peak_value1 = spo2calc.getPeaksIr(sensor)
             ir_valley_time2, ir_valley_value2 = spo2calc.getValleyIr(sensor)

             
             # Finding the gradient of both red and infrared light
             # Gradient = the inline or decline value of the 1st valley and 2nd valley
             red_gradient = spo2calc.findGradient(red_valley_value2, red_valley_value1, red_valley_time2, red_valley_time1)
             ir_gradient = spo2calc.findGradient(ir_valley_value2, ir_valley_value1, ir_valley_time2, ir_valley_time1)
             
             # Finding the constant of both red and infrared light
             # Constand = the fix value
             red_constant = spo2calc.findConstant(red_gradient, red_valley_value1, red_valley_time1)
             ir_constant = spo2calc.findConstant(ir_gradient, ir_valley_value1, ir_valley_time1)
             
             # Finding the point where the the value intersect between the gradient line and time of the 1st peak for red and infrared light
             red_dc = spo2calc.findDC(red_gradient, red_constant, red_peak_time1)
             ir_dc = spo2calc.findDC(ir_gradient, ir_constant, ir_peak_time1)
             
             # Finding the distance between the 1st weak and dc for both red and infrared light
             red_ac = spo2calc.findAC(red_peak_value1, red_dc)
             ir_ac = spo2calc.findAC(ir_peak_value1, ir_dc)
             
             
             
             # Finding the ratio of both red infrared light
             ratio = spo2calc.findRatio(red_ac, red_dc, ir_ac, ir_dc)
             
             # Print the oxygen level and heart rate value
             spo2 = round(spo2calc.spo2Result(ratio))
             
             del  red_valley_time1, red_valley_value1, red_peak_value1, red_valley_time2, red_valley_value2, red_peak_value2
             del ir_valley_time1, ir_valley_value1, ir_valley_time2, ir_valley_value2, ir_peak_time1, ir_peak_value1
             del red_gradient,ir_gradient, red_constant, ir_constant, red_dc,  ir_dc,  red_ac, ir_ac
             gc.collect()
        
             
             print()
             
             if spo2 > 100:
                 spo2 = 100
                 print("Spo2: ", spo2, "%")
                 add_spo2 = Spo2s.append(spo2)
                 
                 # Finding the time difference between the first peak and the second peak
                 delta = utime.ticks_diff(red_peak_time2, red_peak_time1)
                 
                 # calculating heart rate (beats per minute)
                 heart_rate = round(60 / (delta/1000.00))
                 print("Heart rate:", heart_rate)
                 
            
                 
                 add_heartRate = Hr.append(heart_rate)
                 
             elif spo2 <= 0:
                 print("Still reading...")
                 
                 # Display the result on the screen
                 oled.fill(0)
                 oled.text(f"Still reading...%",0,0,100)
                 oled.show()
                 
             else:
                 print("Spo2: ", spo2, "%")
                 add_spo2 = Spo2s.append(spo2)
                 
                 # Finding the time difference between the first peak and the second peak
                 delta = utime.ticks_diff(red_peak_time2, red_peak_time1)
                 
                 # calculating heart rate (beats per minute)
                 heart_rate = round(60 / (delta/1000.00))
                 print("Heart rate:", heart_rate)
            
                 
                 add_heartRate = Hr.append(heart_rate)
                
             
             if (len(Spo2s) == 5):
                sum_oxy = 0
                avg_oxy = 0
                sum_hr = 0
                avg_hr = 0
                for oxy_level in Spo2s:
                     sum_oxy += oxy_level
                     
                for pulse_rate in Hr:
                    sum_hr += pulse_rate
                    
                
                avg_oxy = round(sum_oxy / 5)
                avg_hr = round(sum_hr / 5)
                
                print(avg_oxy)
                print(avg_hr)
                Spo2s.clear()
                Hr.clear()
                
                # Display the result on the screen
                oled.fill(0)
                oled.text(f"Avg Spo2: {avg_oxy}%",0,0,100)
                oled.text(f"Avg HR: {avg_hr}",0,10,100)
                
                oled.show()
                
                
                msg = {
                    "heartRate": heart_rate,
                    "oxygenLevel": spo2
                    }
                # Send the data to the cloud
                iotcentral.send_telemetry(msg)
                
                # Check wheater the the spo2 and heart rate is normal or not                
                check_heart_health = alertChecker.alertCheck(avg_hr,avg_oxy,Hr,Spo2s)
                
             else:
                pass
            
              
    
                     
         else:
            # Display this when the sensor did not read the value
            if no_pulse != 0:
                no_pulse = no_pulse - 1
                
                oled.fill(0)
                print("Please wear the sensor.")             
                print()
                oled.text("Please wear the ",0,0,1)
                oled.text("sensor properly", 0,10,1)
                oled.text("...", 0,20,1)
                oled.show()
                utime.sleep(4)
                
                Spo2s.clear()
                Hr.clear()
                
                # Re-setup the whole sensor before checking wheater the user is wearing the sensor or not
                main(True ,Spo2s,Hr,no_pulse)
            
            else:
                del Spo2s, Hr
                gc.collect()
                
                print("Power off...")
                
                oled.fill(0)
                oled.text("Power off...", 0, 0,500)
                oled.show()
                utime.sleep(2)
                oled.fill(0)
                
                check_sensor = touch_capacitive_checker.check_for_response()
                                      


if __name__ == "__main__":
    #Prompt user that the device is connected to power
    print("Power on...")
    
    # Display in OLED
    oled.text("Power on...",0,10,500)
    oled.show()
    utime.sleep(3)
    oled.fill(0)
    
    #prompt user that the device is getting ready
    print("Getting sensor ready...")
    oled.text("Getting sensor ", 0, 0,500)
    oled.text("ready...",0,10,500)
    oled.show()
    utime.sleep(5)
    no_pulse = 5
    
    #bollean value to print the text of calculating the heart rate and oxygen level
    is_first_reading = True
    
    Spo2s = []
    Hr = []
    #calling the main and passing the bollean value
    main(is_first_reading, Spo2s, Hr, no_pulse)