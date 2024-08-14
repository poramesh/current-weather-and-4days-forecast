from flask import Flask,render_template,request,abort
# import json to load json data to python dictionary
import json
# urllib.request to make a request to api
import urllib.request

import os
from dotenv import load_dotenv
#NEXT TASK IS TO IMPLEMENT FORECAST 

app = Flask(__name__)

API_KEY = os.environ.get('API')


def tocelcius(temp):
    return str(round(float(temp) - 273.16,2))

@app.route('/',methods=['POST','GET'])
def weather():
    
    source = None
    data = {}


    if request.method == 'POST':
        city = request.form['city']
        
        # source contain json data from api
        try:
            source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid='+API_KEY).read()
        except:
             message='adikaprasanga'
             return abort(404)
        
        # converting json data to dictionary

        if source is not None:
            list_of_data = json.loads(source)
            data = {
                "country_code": str(list_of_data['sys']['country']),
                "coordinate": str(list_of_data['coord']['lon']) + ' ' + str(list_of_data['coord']['lat']),
                "temp": str(list_of_data['main']['temp']) + 'k',
                "temp_cel": tocelcius(list_of_data['main']['temp']) + 'C',
                "pressure": str(list_of_data['main']['pressure']),
                "humidity": str(list_of_data['main']['humidity']),
                 "cityname":str(city),
            }
    
    return render_template('index.html',data=data)



if __name__ == '__main__':
    app.run(debug=True)


''''


#http://api.openweathermap.org/data/2.5/weather?q=Bangalore&appid=48a90ac42caa09f90dcaeee4096b9e53


{
  "coord": {
    "lon": 77.6033,
    "lat": 12.9762
  },
  "weather": [
    {
      "id": 803,
      "main": "Clouds",
      "description": "broken clouds",
      "icon": "04n"
    }
  ],
  "base": "stations",
  "main": {
    "temp": 294.35,
    "feels_like": 294.95,
    "temp_min": 293.88,
    "temp_max": 294.95,
    "pressure": 1012,
    "humidity": 93,
    "sea_level": 1012,
    "grnd_level": 915
  },
  "visibility": 6000,
  "wind": {
    "speed": 5.66,
    "deg": 240
  },
  "clouds": {
    "all": 75
  },
  "dt": 1722446397,
  "sys": {
    "type": 1,
    "id": 9205,
    "country": "IN",
    "sunrise": 1722386094,
    "sunset": 1722431813
  },
  "timezone": 19800,
  "id": 1277333,
  "name": "Bengaluru",
  "cod": 200
}

'''