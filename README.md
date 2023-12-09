# Vatalite: The heart attack detector device

The device was made in order to detect any possible heart attack. It will be able to notify the emergency number 
including emergency contact number and ambulance when a heart attack is occurring and no user respond is detected 
from the device.

![WhatsApp Image 2023-06-24 at 22 49 18](https://github.com/Jesslyn26/Vatalite_heart_attack_device/assets/79516995/fe21b966-ad48-4279-a475-6f7bcbfd97b6)


## Project Objective:

- Develop a wearable device that can record real time heart rate and oxygen level
- Alert user when the device is detecting a potential heart attack
- Send emergency SMS containing the type of emergency, location, and the emergency discription (heart attack) to the emergency number (Singapore Civil Defence Force /SCDF)
- Implementing machine learning (transfer learning) to detect the heart attack using the

  ![image](https://github.com/Jesslyn26/Vatalite_heart_attack_device/assets/79516995/9a694ba1-0568-4c11-93ab-6c081522cff0)

## Project Scope
### In scope
- Developing IoT device that can take users' heart rate and oxygen level as its telemetry data.
- Developing a device that focuses on identifying abnormal heart.
- Send notification and SMS to the emergency number (Singapore Civil Defense Force/SCDF) using user smart phone
- Store data and dashboard in Microsoft Azure IoT Central
- Implement Machine learning to predict and detect potential heart attack
P.S. The machine learning was not implemented in the microcontroller due to lack of computational storage.

## Project Requirements 
### Software
- Azure 
- Thonny (IDE for microcontroller) 
- Visual Studio Code (Machine learning)
### Hardware
- PPG sensor (MAX 30102)
- Microcontroller (Raspberry Pi Pico W)
- Vibrator (Ywrobot vibrator motor)
- Battery (2AA)
- Display screen (SH1160 Oled Display)
- Touch Capacitive TTP223
- Laptop to develop the device, cloud, machine learning.

## Overview of how the device should run
![image](https://github.com/Jesslyn26/Vatalite_heart_attack_device/assets/79516995/bc5e9e05-f39c-4f81-a910-63896cbdd950)


## Project Codes
### Building Device and connecting to the 
Pico Backup Folder:
- RPi, lib = necesarry libraires to run the program
- GPIO = responsible for the input and output of the hardware, breadboard, and power
- alertChecker = vibrate the device and display the alert when a potential heart attack is detected 
- ifttt_send_message = responsible for connecting the prototype to the user's phone to alert the user through the user's phone and send SMS message when the device is detected heart attack is detected and no user respond on the device under 30 second
- iot_message: the form of the telemetry data that will be send to Microsoft Azure IoT Central
- iotcentral, iotcentral_creds = connecting to the Microsoft Azure IoT Central account and send telemetry data
- main = connecting each hardware and running them as one. this program in charge of connecting the display, heart rate sensore, vibrator, touch capacitive/ button, and connecting to Microsoft Azure IoT Central
- map_location = responsible on getting current location of the device with urequest and Google API geocode
- sh1106 = display the status of the device, together with heart rate and oxygen level on the oled screen
- touch_capacitive_check = check if there is user respond when the device has detected a potential heart attack. this is to ensure that a heart attack is really detected before sending SMS message to the emergency number
- wifi_iotc = connecting the Raspberry Pi Pico W to the wifi. The device will still work when wifi is not detected. however the data will not be store anywhere if the device failed to connect to the cloud or wifi.

### Machine learning
Pico Backup Folder:
- predic_heart_attack: implementing Virtual Machine in Microsoft Azure IoT to run the prediction in the cloud. however this is still a working progress
- Preprocessed_data = visualize data and elimiting noise from the dataset
- concantinated_dataset = concantinating the all of the dataset as one
- Training_heart.csv = cleaned and labelled the dataset to detect heart attack
- Validate_heart.csv = use to evaluate the model with the Validate_heart dataset
