import pandas as pd
import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def main():
    city_name = input('Введите название города Беларуси: ').capitalize()
    start_date = input('Введите начальную дату периода (формат даты: YYYY-MM-DD): ')
    end_date = input('Введите конечную дату периода (формат даты: YYYY-MM-DD): ')

    url = 'https://data.opendatasoft.com/api/explore/v2.1/catalog/datasets/geonames-postal-code@public/records'
    params = {'limit':20, 'where':f'place_name:"{city_name}" and country_code:"BY"' }
    response = requests.get(url,params=params)
    response.raise_for_status()
    data = response.json()
    city = data["total_count"] 
    if city == 0:
        print('Город не найден! Проверьте существование города!')
        exit()
    latitude = data["results"][0]["latitude"]
    longitude = data["results"][0]["longitude"]

    url = "https://archive-api.open-meteo.com/v1/era5"
    params = {"hourly":"temperature_2m", "latitude":latitude, "longitude":longitude, "start_date":start_date, "end_date":end_date}
    response = requests.get(url,params=params)
    response.raise_for_status()
    data_temperature = response.json()
    temperature_value = data_temperature["hourly"]["temperature_2m"]
    temperature_date = data_temperature["hourly"]["time"]

    dataframe = pd.DataFrame(list(zip(temperature_date, temperature_value)), columns=['date', 'temp'])

    dataframe['date'] = pd.to_datetime(dataframe['date'])  
    plt.plot(dataframe['date'], dataframe['temp'])
    plt.title(f'График температуры в городе {city_name}')
    plt.xlabel('Даты')
    plt.ylabel('Температуры (°C)')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gcf().autofmt_xdate()
    plt.show()

if __name__=='__main__':
    main()
    