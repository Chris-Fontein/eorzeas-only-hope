import json
import random
import datetime
import calendar
import unicodedata
import xml.etree.ElementTree as ET
import urllib.request

import bot.commands

SPEED_CONVERSION = 1.609344 #conversion of mi -> km
BASE_ADDRESS = "https://dd.weather.gc.ca/citypage_weather/xml"

class Weather(bot.commands.ParamCommand):
    key: str

    def __init__(self) -> None:
        super().__init__("weather", 0, 8)

    async def process_args(self, context: bot.commands.MessageContext, *args: str) -> bool:
        if not args: #random
            ret = get_current_city_weather()
        else: #request
            ret = get_current_city_weather(" ".join(args))

        await context.reply_all(ret)
        return True

def get_current_city_weather(request = None):
    city, province, code = lookup_city(request)
    
    if not city and not province:
        return f'"{request}" is not a valid town or city'
    elif type(province) is list:
        province_list = ','.join(province)
        return f"There is more then one {city} searchable please specify [{province_list}]"
    elif city and province and not code:
        return f'"There is no {city}" in {province}'
    #code = "s0000400"
    #province = "NL"
    
    root, url = get_city_data(code, province)
    try:
        current = root.find("currentConditions")

        if len(current) == 0:
            return f"Current weather for {city}, {province} is unavailable"

        temp_desc = get_temp_desc(current)
        wind_desc = get_wind_desc(current.find("wind"))
        epoch_time = get_epoch_time(current.find("dateTime"))

        return f"Weather for {city}, {province} as of {epoch_time}\n{temp_desc}\n{wind_desc}"
    except:
        return f"Error reading {url}"


####################
# Aquire city data #
####################
def get_city_data(code, province):
    url = f"{BASE_ADDRESS}/{province}/{code}_e.xml"
    #print(url)
    response = urllib.request.urlopen(url).read()
    tree = ET.fromstring(response)

    return tree, url

def lookup_city(request):
    with open("../../commands/city_codes.json", "r") as f:
        city = province = code = None
        cities = json.load(f)
        if not request: #pick a random city
            city_key = random.choice(list(cities.keys()))
            province = random.choice(list(cities[city_key].keys()))
            city = cities[city_key][province]["name"]
            code  = cities[city_key][province]["code"]
        else:
            split = request.split(" ")
            if len(split) > 1 and len(split[-1]) == 2: #check for a province
                province = split[-1]
                request = " ".join(split[:-1])
            lower_name = strip_accents(request.lower())

            #city exists in records
            if lower_name in cities:
                city_info = cities[lower_name]
                if province:
                    #specified province doesn't have the city
                    if province not in city_info: 
                        return lower_name, province, None
                    #specified province has the city
                    city = city_info[province]["name"]
                    code = city_info[province]["code"]
                else:
                    #only one option
                    if len(city_info) == 1:
                        province = list(city_info.keys())[0]
                        city = city_info[province]["name"]
                        code = city_info[province]["code"]
                    #more then one province has a city of that name
                    else:
                        city = lower_name
                        province = list(city_info.keys())

                
            else:
                return None, None, None

        return city, province, code

########################
# Compose Descriptions #
########################

def get_temp_desc(current):
    temp_desc = get_temperature_display(current.find("temperature"))
    windchill_desc = get_temperature_display(current.find("windChill"))
    desc = f":thermometer: It's {temp_desc}"
    if(windchill_desc):
        desc = f"{desc}, feels like {windchill_desc} with windchill."
    return desc

def get_wind_desc(wind):
    speed = get_speed_display(wind[0])
    gusts = get_speed_display(wind[1])
    direction = wind[2].text

    desc = f":dash: Winds are approaching from the {direction} at speeds of {speed}"
    if gusts:
        desc = f"{desc} with gusts up to {gusts}"
    return  desc

###########################################
# data formating and conversion functions #
###########################################
def get_epoch_time(date_time):
    year = int(date_time[0].text)
    month = int(date_time[1].text)
    day = int(date_time[2].text)
    hour = int(date_time[3].text)
    minute = int(date_time[4].text)

    t=datetime.datetime(year, month, day, hour, minute, 0)
    epoch = calendar.timegm(t.timetuple())
    return f"<t:{epoch}>"

def convert_temperature(value, scale):
    if scale == "C":
        return value / 5 * 9 + 32, "F"
    else:
        return (value - 32) / 9 * 5, "C"

def get_temperature_display(temp):
    try:
        value = float(temp.text)
        scale = temp.get("units")
        if not scale:
            scale = "C" if temp.get("unitType") == "metric" else "F" 
        c_value, c_scale = convert_temperature(value, scale)
        return f"{round(value, 1)}°{scale}({round(c_value,1)}°{c_scale})"
    except:
        return None

def convert_speed(value, scale):
    if scale == "km/h":
        return value / SPEED_CONVERSION, "mi/h"
    else:
        return value * SPEED_CONVERSION, "km/h"

def get_speed_display(speed):
    try:
        value = float(speed.text)
        scale = speed.get("units")
        c_value, c_scale = convert_speed(value, scale)
        return f"{round(value,1)}{scale}({round(c_value,1)}{c_scale})"
    except:
        return None


def strip_accents(text):
    text = unicodedata.normalize('NFD', text)\
           .encode('ascii', 'ignore')\
           .decode("utf-8")

    return str(text)

#####################
# City Lookup Build #
#####################
#construct the city lookup info from online json
def city_lookup_builder():
    url = "https://collaboration.cmc.ec.gc.ca/cmc/cmos/public_doc/msc-data/citypage-weather/site_list_en.geojson"
    response = urllib.request.urlopen(url).read()
    city_dict = json.loads(response)["features"]
    cities = {}
    for i in city_dict:
        properties = i["properties"]
        name = properties["English Names"]
        lower_name = strip_accents(name.lower())
        if lower_name in cities:
            cities[lower_name][properties["Province Codes"]] = {"code":properties["Codes"], "name":name}
        else:
            cities[lower_name] = {properties["Province Codes"] : {"code":properties["Codes"], "name":name}}

    with open("../../commands/city_codes.json", "w") as f:
        json.dump(cities, f, indent = 2)

#city_lookup_builder()
#print(get_current_city_weather())
#print()
#print(get_current_city_weather("sheb"))
#print()
#print(get_current_city_weather("toronto"))
#print()
#print(get_current_city_weather("shelburne AB"))
#print()
#print(get_current_city_weather("shelburne ON"))
#print()
#print(get_current_city_weather("shelburne NS"))
