from rest_framework import serializers


class Event:

    def __init__(self,event):
        self.event = event

    def get_data(self):

        return {"title": self.event.title.get_text(),
                "url": self.event.url.get_text(),
                "description": self.event.description.get_text(),
                "start": self.event.start_time.get_text(),
                "venue": "{},{},{}".format(self.event.venue_name.get_text(), self.event.venue_address.get_text(),
                                           self.event.city_name.get_text()),
                "image": self.event.medium.url.get_text()
        }

class EventSerializer

