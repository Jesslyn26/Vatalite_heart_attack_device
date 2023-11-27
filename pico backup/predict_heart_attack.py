import urequests
import ujson


def predict_healthy_heart(hr,spo2):
    data = {' HR': hr, ' SpO2': spo2}
    data_json = ujson.dumps(data)


    # Send the data to the VM
    url = 'http://20.2.86.252:5000/predict-data'  # Replace <vm_ip_address> with the actual IP address of your VM
    response = urequests.post(url, json = data_json)
    prediction = response.json()
    if response.status_code == 200:
        prediction_result = response.json()
        # Process the prediction result
        process_prediction(prediction_result)
    else:
        print('Error:', response.status_code)


prediction = predict_healthy_heart(90,100)
print(prediction)