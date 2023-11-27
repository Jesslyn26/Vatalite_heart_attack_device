import network
import iotcentral
import utime
'''
ssid = 'Wireless@PSB'
password = 'PSBstudent123' '''

ssid = 'Jesslyn Galaxy A32'
password = 'jess2610'
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
max_wait = 20
if ssid != '':
    wlan.connect(ssid,password)
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        utime.sleep(1)
        
print("WIfi connected:",wlan.isconnected())
status = wlan.ifconfig()
print(status[0])

if wlan.isconnected():           
    try:
        iotcentral.connect()
    except ValueError as e:
        print(e)
    

