import requests,os
from bs4 import BeautifulSoup

EVENTS_APIKEY = os.environ.get('ACCUWEATHER_APIKEY')


class GetEvents:

    __slots__ = ['location', 'date', 'events']

    def __init__(self, location, date=""):
        self.location = location
        self.date = date
        self.events = self.get_events_text()

    def get_events_text(self):

        query_string = {"app_key": EVENTS_APIKEY, "location": self.location, "date": self.date}
        url = "http://api.eventful.com/rest/events/search"

        response = requests.request("GET", url, params=query_string)

        return BeautifulSoup(response,"html.parser").events

    def get_events(self):

        return {event.title: event for event in self.events if not isinstance(event, type("me".upper))}  #replace bound function with better code


