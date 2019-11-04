import os,requests
ACCU_APIKEY = os.environ.get('ACCUWEATHER_APIKEY')


class GetLocationDetails:

    """

    Return location details after obtaining  ip address.

    """

    def __init__(self, ip):
        self.ip = ip
        self.location_key, self.response = self.get_response()

    def get_response(self):

        response = requests.get("http://dataservice.accuweather.com/locations/v1/cities/ipaddress?apikey={}&q={}".format(ACCU_APIKEY, self.ip))
        self.response = response.json()
        self.location_key = self.response["Key"]

        return self.response, self.location_key

    def get_location_key(self):

        return self.location_key

    def get_type(self):

        return self.response["Type"]

    def get_region(self):

        return self.response["Region"]["EnglishName"]

    def get_country(self):

        return self.response["Country"]["EnglishName"]

    def get_cityname(self):

        return self.response['EnglishName']

    def get_timezone(self):

        return self.response['TimeZone']['Code'],self.response['TimeZone']['Name']

    def get_geoposition(self):

        return self.response['Geoposition']['Latitude'],self.response['Geoposition']['Longitude']


class GetForecastDetails:

    def __init__(self, location_key):
        self.location_key = location_key

    def get_response(self, query_string):

        return requests.get("http://dataservice.accuweather.com/forecasts/v1/{}/{}?apikey={}"
                            .format(query_string, self.location_key, ACCU_APIKEY))

    def get_5_day_forecast(self):
        response = self.get_response('daily/5day')

        return {day['Date']: {'Day': day['Day'],
                              'Night': day['Night'],
                              'Temperature': [day['Temperature']['Minimum'], day['Temperature']['Maximum']]
                              } for day in response.json()['DailyForecasts']
                }

    def get_12_hour_forecast(self):
        response = self.get_response('hourly/12hour')

        return {hour['DateTime']: {'Icon': hour['WeatherIcon'],
                                   'Phrase': hour['IconPhrase'],
                                   'Temperature': hour['Temperature'],
                                   'RainProbability':hour['PrecipitationProbability']
                              } for hour in response.json()[:]
                }

    def get_current_conditions(self):
        response = requests.get("http://dataservice.accuweather.com/currentconditions/v1/{}?apikey={}"
                                .format(self.location_key, ACCU_APIKEY))

        return [{"Time": time["LocalObservationDateTime"],
                 "WeatherText": time["WeatherText"],
                 "Icon": time["WeatherIcon"],
                 "Temperature": time["Temperature"]} for time in response.json()
                ]


