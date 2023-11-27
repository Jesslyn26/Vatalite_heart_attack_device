import urequests

def get_lat_long():
    # Set the Geolocation API endpoint
    url = f'https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyBN2TlJDb2HQDG_nAJa4dFuNnhxLjSRgao'
    # Make the API request
    
    response = urequests.post(url, json={})

    # Parse the response and extract the location coordinates and address
    if response.status_code == 200:
        data = response.json()
        longitude = data['location']['lng']
        latitude = data['location']['lat']
        
        print(f"Longitude: {longitude}")
        print(f"Latitude: {latitude}")
    else:
        print("Error occurred while fetching location.")
    response.close()
        
    return latitude, longitude

def get_address(latitude, longitude):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={},{}&key=AIzaSyDWS0cq1-_TAS3meUdDEX_V0_eeJyMjxtY".format(latitude, longitude)
    response = urequests.get(url)

    if response.status_code == 200:
        data = response.json()
        address = data["results"][0]["formatted_address"]
        response.close()
        return address
    else:
        response.close()
        return None
    