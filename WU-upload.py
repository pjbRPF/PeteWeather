import interrupt_client, MCP342X, wind_direction, HTU21D, bmp085, tgs2600, ds18b20_therm
import database
import requests

pressure = bmp085.BMP085()
temp_probe = ds18b20_therm.DS18B20()
air_qual = tgs2600.TGS2600(adc_channel = 0)
humidity = HTU21D.HTU21D()
wind_dir = wind_direction.wind_direction(adc_channel = 0, config_file="wind_direction.json")
interrupts = interrupt_client.interrupt_client(port = 49501)
#db = database.weather_database() #Local MySQL db

wind_average = wind_dir.get_value(10) #ten seconds
ambient_temp = humidity.read_temperature()
ground_temp = temp_probe.read_temp()
air_quality = air_qual.get_value()
pressure = pressure.get_pressure()
humidity = humidity.read_humidity()
wind_speed = interrupts.get_wind()
wind_gust = interrupts.get_wind_gust()
rainfall = interrupts.get_rain()

#print("Inserting...")
#db.insert(ambient_temp, ground_temp, air_quality, pressure, humidity, wind_average, wind_speed, wind_gust, rainfall)
#print("done")

interrupts.reset()

# Conversion functions
def hpa_to_inches(pressure_in_hpa):
    pressure_in_inches_of_m = pressure_in_hpa * 0.02953
    return pressure_in_inches_of_m

def mm_to_inches(rainfall_in_mm):
    rainfall_in_inches = rainfall_in_mm * 0.00393701
    return rainfall_in_inches

def degc_to_degf(temperature_in_c):
    temperature_in_f = (temperature_in_c * (9/5.0)) + 32
    return temperature_in_f

def kmh_to_mph(kmh):
    mph = kmh * 0.621371
    return mph

## TEST DATA
#humidity = 55.998
#ambient_temp = 23.456
#pressure = 1067.890
#ground_temp = 16.345
#wind_speed = 5.6129
#wind_gust = 12.9030
#wind_average = 180
#rainfall = 1.270

# create a string to hold the first part of the URL
WUurl = "https://weatherstation.wunderground.com/weatherstation\
/updateweatherstation.php?"
stationID = "ISOWER8"
stationKey = "mYkwha6B"
WUcreds = "ID=" + stationID + "&PASSWORD="+ stationKey
date_str = "&dateutc=now"
action_str = "&action=updateraw"


humidity_str = "{0:.2f}".format(humidity)
pressure_str = "{0:.2f}".format(hpa_to_inches(pressure))
wind_speed_str = "{0:.2f}".format(kmh_to_mph(wind_speed))
wind_gust_str = "{0:.2f}".format(kmh_to_mph(wind_gust))
rainfall_str = "{0:.2f}".format(mm_to_inches(rainfall))
wind_average_str = str(wind_average)
ambient_temp_str = "{0:.2f}".format(degc_to_degf(ambient_temp))

r= requests.get(
    WUurl +
    WUcreds +
    date_str +
    "&humidity=" + humidity_str +
    "&tempf=" + ambient_temp_str +
    "&baromin=" + pressure_str +
    "&windspeedmph=" + wind_speed_str +
    "&windgustmph=" + wind_gust_str +
    "&rainin=" + rainfall_str +
    "&winddir=" + wind_average_str +
    action_str)

# print("Received " + str(r.status_code) + " " + str(r.text))
print("Pressure is:",pressure_str)
print("Temp is:",ambient_temp_str)
print("Humidity is:",humidity_str)
print("Wind speed is:",wind_speed_str)
print("Wind gust is:",wind_gust_str)
print("Rain is:",rainfall_str)
print("Wind Average is:",wind_average_str)
