import utime
  
class spo2Calc:
 
    # Function to find the valley of the red light
    def getValleyRed(spo2_sens):
        minValue = 100000
        minTime = 0
        # Checking 20 times if the value is below minValue or not
        buffer_value = 20
        buffer = buffer_value
   
        while buffer != 0:
            # Pause for 12 millisecond before checking new value
            utime.sleep_ms(15)
            spo2_sens.check()
            buffer = buffer - 1
            # The current time and the value to compare with the minValue
            time = utime.ticks_ms()
            currentValue = spo2_sens.pop_red_from_storage()
    
            if (minValue > currentValue and currentValue != 0):
                # Rewrite the lowest value and time with the current value and time
                minValue = currentValue
                minTime = time
                # Reset the count or buffer
                buffer = buffer_value
            
        return minTime,minValue
    
    # Function to find the peaks of the red light
    def getPeaksRed(spo2_sens):
        maxValue = 0
        maxTime = 0
        # Checking 20 times if the value is below minValue or not
        buffer_value = 20
        buffer = buffer_value
        
        while buffer != 0:
            # Pause for 12 millisecond before checking new value
            utime.sleep_ms(15)
            spo2_sens.check()
            buffer = buffer - 1
            
            # The current time and the value to compare with the maxValue
            time = utime.ticks_ms()
            currentValue = spo2_sens.pop_red_from_storage()
            
            if (maxValue < currentValue):
                # Rewrite the highest value and time with the current value and time
                maxValue = currentValue
                maxTime = time
                # Reset the count or buffer
                buffer = buffer_value
        
        return maxTime, maxValue
    


    # Function to find the valley of the infrared light
    def getValleyIr(spo2_sens):
        minValue = 100000
        minTime = 0
        # Checking 20 times if the value is below minValue or not
        buffer_value = 20
        buffer = buffer_value
            
        while buffer != 0:
            # Pause for 12 millisecond before checking new value
            utime.sleep_ms(15)
            spo2_sens.check()
            buffer = buffer - 1
            # The current time and the value to compare with the minValue
            time = utime.ticks_ms()
            currentValue = spo2_sens.pop_ir_from_storage()
            
            if (minValue > currentValue and currentValue != 0):
                # Rewrite the lowest value and time with the current value and time
                minValue = currentValue
                minTime = time
                # Reset the count or buffer
                buffer = buffer_value
            
        return minTime,minValue
    
    # Function to find the peak for the infrared light
    def getPeaksIr(spo2_sens):
        maxValue = 0
        maxTime = 0
        # Checking 20 times if the value is below minValue or not
        buffer_value = 20
        buffer = buffer_value
            
        while buffer != 0:
            # Pause for 12 millisecond before checking new value
            utime.sleep_ms(15)
            spo2_sens.check()
            buffer = buffer - 1
            # The current time and the value to compare with the maxValue
            time = utime.ticks_ms()
            currentValue = spo2_sens.pop_ir_from_storage()
            
            if (maxValue < currentValue):
                # Rewrite the highest value and time with the current value and time
                maxValue = currentValue
                maxTime = time
                # Reset the count or buffer
                buffer = buffer_value
        
        return maxTime, maxValue
    
    
    #Funtion to calculate the gradient
    def findGradient (pointValue3, pointValue1, pointTime3, pointTime1):
        m = (pointValue3 - pointValue1)/ (pointTime3 - pointTime1)
        
        return m
    
    #Funtion to calculate the constant
    def findConstant(gradience, pointValue1, pointTime1):
        c = pointValue1 - (gradience * pointTime1)
        return c
    
    #  Function to find the intersect point between the 1st peak point and the gradient line
    def findDC(gradience, constant, pointTime2):
        dcValue = (gradience * pointTime2) + constant
        
        return dcValue
    
    # Find the distance between the first peak and DC point
    def findAC(pointValue2, dc):
        ac = pointValue2 - dc
        
        return ac
    
    # Find ratio between red and infrared
    def findRatio(redAc, redDc, irAc, irDc):
        try: 
            r = (redAc / redDc)/(irAc/ irDc)
        except ZeroDivisionError:
            r = 0
            
        return r
    
    # Oxygen level result
    def spo2Result(r):
        spo2 = 104 - 17*r
        
        return spo2
    
    