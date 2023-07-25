import sys
from utime import sleep
from random import randint
from iotc import IoTCClient,IoTCConnectType,IoTCLogLevel,IoTCEvents
import iot_msg
import json

# Registering IoT central details to connect to the cloud
scope_id = '0ne009D5A3E'
device_id = 'nzcogc1d9z'
key = 'adntjzNpvQt6Vr6wPHeVFU+CvXcj1smUNe61jjlQTD8='
conn_type=IoTCConnectType.DEVICE_KEY

client=IoTCClient(scope_id,device_id,conn_type,key)
client.set_log_level(IoTCLogLevel.ALL)
def on_properties(name, value):
    print('Received property {} with value {}'.format(name, value))
    return value


def on_commands(command, ack):
    print('Command {}.'.format(command.name))
    ack(command, command.payload)
    
def listen_commands():
    client.on(IoTCEvents.COMMANDS, on_commands)

def on_enqueued(command):
    iot_msg.MSG_ENQ["name"] = command.name
    try:
        iot_msg.MSG_ENQ["msg"] = json.loads((command.value).decode("utf8"))
    except ValueError as e:
        print(e)
    print('Enqueued Command {}.'.format(command.name))


def connect():
    client.on(IoTCEvents.PROPERTIES, on_properties)
    client.on(IoTCEvents.ENQUEUED_COMMANDS, on_enqueued)
    check = client.connect()
    

def is_connected():
    return client.is_connected()

def send_telemetry (msg):
#     sleep(2)
#     client.listen()
#     sleep(2)
    print("Sending telemetry....")
    client.send_telemetry(msg)
    print()
    print ("Telemetry sent")
    #return iot_msg.MSG_ENQ["msg"]
    
def listen ():
    client.listen()
    

while client.is_connected():
    client.listen()
    print('Sending telemetry')
    sleep(2)
