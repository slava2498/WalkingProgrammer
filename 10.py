# x = 10 / 0

# try:
#     x = 10 / 0
# except ZeroDivisionError:
#     print("Нельзя делить на ноль!")

# a = 10
# b = 0
#
# if b == 0:
#     print("Нельзя делить на ноль!")
# else:
#     x = a / b


response = {
  "coord": {
    "lon": 10.99,
    "lat": 44.34
  },
  "weather": [
    {
      "id": 501,
      "main": "Rain",
      "description": "moderate rain",
      "icon": "10d"
    }
  ],
  "base": "stations",
  "main": {
    # "temp": None,
    "temp": 'asd123.3',
    # "temp": 298.48,
    "feels_like": 298.74,
    "temp_min": 297.56,
    "temp_max": 300.05,
    "pressure": 1015,
    "humidity": 64,
    "sea_level": 1015,
    "grnd_level": 933
  },
  "visibility": 10000,
  "wind": {
    "speed": 0.62,
    "deg": 349,
    "gust": 1.18
  },
  "rain": {
    "1h": 3.16
  },
  "clouds": {
    "all": 100
  },
  "dt": 1661870592,
  "sys": {
    "type": 2,
    "id": 2075663,
    "country": "IT",
    "sunrise": 1661834187,
    "sunset": 1661882248
  },
  "timezone": 7200,
  "id": 3163858,
  "name": "Zocca",
  "cod": 200
}

# temperature = response['main']['temperature']
# print(temperature)


# clouds = response['clouds']['all']
# weather = response['weather'][0]['main']
#
# try:
#     temperature = response['main']['temperature']
# except KeyError:
#     temperature = None
#
# print(f"Облачность: {clouds}%")
# print(f"Погода: {weather}")
# print(f"Температура: {temperature if temperature is not None else 'Не известно'}")

# clouds = response['clouds']['all']
# weather = response['weather'][0]['main']
#
#
# if "temperature" in response['main']:
#   temperature = response['main']['temperature']
# else:
#   temperature = None
#
# print(f"Облачность: {clouds}%")
# print(f"Погода: {weather}")
# print(f"Температура: {temperature if temperature is not None else 'Не известно'}")

temperature = response['main']['temp']
clouds = response['clouds']['all']
weather = response['weather'][0]['main']

try:
    float(temperature)
except (ValueError, TypeError) as error_text:
    temperature = None
    print(f"Ошибка: {error_text}")
finally:
  print('Блок finally')


print(f"Облачность: {clouds}%")
print(f"Погода: {weather}")
print(f"Температура: {float(temperature) if temperature is not None else 'Не известно'}")

