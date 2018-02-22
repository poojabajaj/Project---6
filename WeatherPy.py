
# coding: utf-8

# In[1]:


#Installing citipy package thru jupyter notebook
get_ipython().system('pip install citipy')


# In[2]:


#Dependencies
import requests as req
import json
import random
from random import randint, choice, shuffle
import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import csv
import kdtree
import os
import csv
import numpy as np
import pandas as pd


# In[3]:


#Loading the citipy data
class City:
    '''
    City wraps up the info about a city, including its name, coordinates,
    and belonging country.
    '''
    def __init__(self, city_name, country_code):
        self.city_name = city_name
        self.country_code = country_code

#_world_cities_csv_path = "citipy-0.0.5 2/citipy/worldcities.csv"
#_world_cities_csv_path = os.path.join(_current_dir, 'worldcities.csv')

# load the city data up
_current_dir, _current_filename = os.path.split('__file__')
_world_cities_csv_path = "citipy-0.0.5 2/citipy/worldcities.csv"
_world_cities_kdtree = kdtree.create(dimensions=2)
WORLD_CITIES_DICT = {}

with open(_world_cities_csv_path, 'r') as csv_file:
    cities = csv.reader(csv_file)

    # discard the headers
    cities.__next__()

    # populate geo points into kdtree
    for city in cities:
        city_coordinate_key = (float(city[2]), float(city[3]))
        _world_cities_kdtree.add(city_coordinate_key)
        c = City(city[1], city[0])
        WORLD_CITIES_DICT[city_coordinate_key] = c


def nearest_city(latitude, longitude):
    nearest_city_coordinate = _world_cities_kdtree.search_nn((latitude, longitude, ))
    return WORLD_CITIES_DICT[nearest_city_coordinate[0].data]


# In[4]:


#Testing on a particular coordinates
#a = nearest_city(37.3382, 121.8863)
#print(a.city_name)
#print(a.country_code)


# In[5]:


# See above - we've created an API key in a file called 'apikey', 
# in the same directory as this notebook
filename = 'apikey'


# In[6]:


def get_file_contents(filename):
    """ Given a filename,
        return the contents of that file
    """
    try:
        with open(filename, 'r') as f:
            # It's assumed our file contains a single line,
            # with our API key
            return f.read().strip()
    except FileNotFoundError:
        print("'%s' file not found" % filename)


# In[7]:


api_key = get_file_contents(filename)
print("Our API key is: %s" % (api_key))


# In[8]:


# Note that the ?t= is a query param for the t-itle of the
# movie we want to search for.
#api.openweathermap.org/data/2.5/weather?q=London,uk&APPID=559509be0d4a4cde600b5fe55c9c2a71
#api.openweathermap.org/data/2.5/weather?q={city name}

url = "http://api.openweathermap.org/data/2.5/weather?q="


# In[9]:


#Latitudes range from -90 to 90. Longitudes range from -180 to 180
latitude = np.arange(-90, 90)
longitude = np.arange(-180, 180)

cities_500_unique = {}
log = []
count = 0
#print(cities_500)

# Create a random array of data that we will use for our y values\n",
while(len(cities_500_unique)<500):
    lat = random.choice(latitude)
    lon = random.choice(longitude)
    city = str(nearest_city(lat, lon).city_name)
    country = str(nearest_city(lat, lon).country_code)
    query = url+city+","+country+"&APPID="+api_key
    outputQuery = req.get(query).json()
    if(city in cities_500_unique) or (outputQuery['cod']=='404'):
        pass
    else:
        #500 unique and random cities identified
        cities_500_unique[city]=country
        #creating log
        count = count +1
        record = "Processing Record " +  str(count) + " of Set 500 " + " | " + city + " "+ str(query)
        log.append(record)


# In[10]:


len(cities_500_unique)


# In[11]:


log_df = pd.DataFrame(log, columns=["Beginning Data Retrieval"])
log_df.to_csv('log.csv', index=False)


# In[12]:


#for key in cities_500_unique.keys():
#    print(key)
    
#for value in cities_500_unique.values():
#    print(value)


# In[13]:


#cities_500_unique


# In[14]:


#Creating dataset
#Temperature (F) vs. Latitude 
#Humidity (%) vs. Latitude
#Cloudiness (%) vs. Latitude
#Wind Speed (mph) vs. Latitude
MaxTemp= []
latitude = []
humidity = []
cloudiness = []
windSpeed = []
queries_500 = []
dates = []
cities = []
CountryCode =[]

x = 0
for city, country in cities_500_unique.items():
    #city = str(city)
    #country = str(country)
    #queries_500.append(querygenerator(a,b))
    query = url+city+","+country+"&APPID="+api_key
    #query = querygenerator(city, country)
    #print(query)
    outputQuery = req.get(query).json()
    MaxTemp.append(outputQuery['main']['temp_max'])
    latitude.append(outputQuery['coord']['lat'])
    humidity.append(outputQuery['main']["humidity"])
    cloudiness.append(outputQuery['clouds']["all"])
    windSpeed.append(outputQuery['wind']["speed"])
    dates.append(outputQuery['dt'])
    cities.append(city)
    CountryCode.append(country)


# In[15]:


print(len(MaxTemp))
print(len(latitude))
print(len(humidity))
print(len(cloudiness))
print(len(windSpeed))
#print("~~~~~~1~~~~~~~")
#print(temp)
#print("~~~~~~2~~~~~~~")
#print(latitude)
#print("~~~~~~3~~~~~~~")
#print(humidity)
#print("~~~~~~4~~~~~~~")
#print(cloudiness)
#print("~~~~~~5~~~~~~~")
#print(windSpeed)


# In[16]:


#creating city dataframe
city_df = pd.DataFrame(
    {'City': cities,
     'CountryCode': CountryCode,
     'Latitude': latitude, 
     'MaxTemp': MaxTemp, 
     'Humidity': humidity, 
     'Cloudiness': cloudiness, 
     'WindSpeed': windSpeed,
     'Date':dates
    })
#city_df.set_index('Latitude', inplace=True)
city_df.to_csv('CityAndData.csv', index=False)
city_df.head(5)


# In[17]:


#Temperature (F) vs. Latitude --creating scatter plot
x_axis = city_df['Latitude']
y_axis = city_df['MaxTemp']
plt.title("Latitude vs Temperature Plot (02/20/2018)")
plt.xlabel("Latitude")
plt.ylabel("Max Temp (F)")
plt.grid()
plt.scatter(x_axis, y_axis,  marker="o", color="blue")
plt.savefig("Latitude_vs_Temperature_Plot")
plt.show()


# In[18]:


#Humidity (%) vs. Latitude ----creating scatter plot
x_axis = city_df['Latitude']
y_axis = city_df['Humidity']
plt.title("Latitude vs. Humidity Plot (02/02/2018)")
plt.xlabel("Latitude")
plt.ylabel("Humidity (%)")
plt.grid()
plt.scatter(x_axis, y_axis, marker="o", color="blue")
plt.savefig("Latitude_vs_Humidity_Plot")
plt.show()


# In[19]:


#Cloudiness (%) vs. Latitude
x_axis = city_df['Latitude']
y_axis = city_df['Cloudiness']
plt.title("Latitude vs. Cloudiness Plot (02/02/2018)")
plt.xlabel("Latitude")
plt.ylabel("Cloudiness (%)")
plt.grid()
plt.scatter(x_axis, y_axis, marker="o", color="blue")
plt.savefig("Latitude_vs_Cloudiness_Plot")
plt.show()


# In[20]:


#Wind Speed (mph) vs. Latitude
x_axis = city_df['Latitude']
y_axis = city_df['WindSpeed']
plt.title("Latitude vs. WindSpeed Plot (02/02/2018)")
plt.xlabel("Latitude")
plt.ylabel("WindSpeed (mph)")
plt.grid()
plt.scatter(x_axis, y_axis, marker="o", color="blue")
plt.savefig("Latitude_vs_WindSpeed_Plot")
plt.show()


# In[21]:


#observable trends
#Temperature (F) vs. Latitude - It appears that first max temperature increases with latitude but once 
#latitude is positive it starts to taper down.
#Humidity (%) vs. Latitude - There seems to be no strong trend in latitude and humidity. Around latitude zero, 
#there are only higher humidity points.
#Cloudiness (%) vs. Latitude -- Latitude does not seem to affect cloudiness. At almost all ranges of latitude, 
#there are cities with highest as well as lowest cloudiness.
#Wind Speed (mph) vs. Latitude -- As latitude increases, there starts to appear a handful of cities with higher than 
#normal Windspeed.

