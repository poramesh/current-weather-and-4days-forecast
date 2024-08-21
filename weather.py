from flask import Flask,render_template,request,abort
import json
import urllib.request
import os
from dotenv import load_dotenv
from collections import defaultdict
from datetime import datetime


app = Flask(__name__)

API_KEY = os.environ.get('API')


def tocelcius(temp):
    return str(round(float(temp) - 273.16,2)) #if we dont round it to two decimal places then it would be like this - 25.123456789

@app.route('/',methods=['POST','GET'])
def weather():
    
    source = None
    weather_data = {}
    forecast_dict = defaultdict(list)

    if request.method == 'POST':
        city = request.form['city']
        #forecast_specific_day = request.form['specific_day']
        
        weather = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid='+API_KEY).read()
        forecast = urllib.request.urlopen(f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}').read()  

        if weather is not None:
            list_of_data = json.loads(weather)
            weather_data = {
                "country_code": str(list_of_data['sys']['country']),
                "coordinate": str(list_of_data['coord']['lon']) + ' in longitude and '  + str(list_of_data['coord']['lat']) + ' in latitude ',
                "temp": str(list_of_data['main']['temp']) + ' K',
                "temp_cel": tocelcius(list_of_data['main']['temp']) + ' °C',
                "pressure": str(list_of_data['main']['pressure']),
                "humidity": str(list_of_data['main']['humidity'])+ '%',
                "cityname":str(city).capitalize()
            }

        if forecast is not None: 
            list_of_data = json.loads(forecast)
            forecast_list = list_of_data['list']
            forecast_data = defaultdict(list) #this is how it would look, defaultdict(<class 'list'>, {'a': [1, 2], 'b': [3]})
            
            for forecast in forecast_list:
                date = forecast['dt_txt'].split(' ')[0]
                forecast_data[date].append(forecast)
            
            for date,forecasts in forecast_data.items():
                formated_date = datetime.strptime(date, "%Y-%m-%d").strftime("%d %B, %A") #Saturday 9 August
                for forecast in forecasts:
                    time = datetime.strptime(forecast['dt_txt'],"%Y-%m-%d %H:%M:%S").strftime("%H:%M")
                    temp_k = forecast["main"]["temp"]
                    temp_c = round(temp_k - 273.15) # temp_c = round(26.85) would result in 27
                    description = forecast['weather'][0]['description']
                    icon = forecast['weather'][0]['icon']

                    forecast_info = {
                                     "formated_date": formated_date,
                                     "time": time, 
                                      "temp_k":temp_k,
                                      "temp_c":temp_c, 
                                      "description":description,
                                      "icon":icon
                                      }
                    
                    if time in ('09:00','12:00','18:00','21:00'):
                        if time == '09:00': val = 'Morning'
                        elif time == '12:00': val = 'Afternoon'
                        elif time == '18:00': val = 'Evening'
                        elif time == '21:00': val = 'Night'
                        forecast_info['val'] = val
                        forecast_dict[date].append(forecast_info)     
                  
    return render_template('index.html',weather_data=weather_data,forecast_data = forecast_dict)


    
@app.errorhandler(500)
def global_page_not_found(e):
    return render_template('errorPage.html')
            



if __name__ == '__main__':
    app.run(debug=True)


''''


http://api.openweathermap.org/data/2.5/weather?q=Bangalore&appid={}



http://api.openweathermap.org/data/2.5/forecast?q=Bangalore&cnt=2&appid={} #no need of cnt fetc,h all the data that they allow cause there are hardly any

http://api.openweathermap.org/data/2.5/forecast?q=Bangalore&appid={}







'''