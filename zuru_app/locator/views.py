# -*- coding: utf-8 -*-
import socket,os,requests
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from ipware import get_client_ip

ACCU_API = os.environ.get('ACCUWEATHER_APIKEY')

def validate_ip(address):
    try:
        socket.inet_aton(address)
        return True
    except socket.error:
        return False

def find_ip(request):
    ip = None
    client_ip, is_routable = get_client_ip(request)
    if client_ip is None:
        #Unable to get the client's IP address'
        return HttpResponse("Ip address not found!")
    else:
        # We got the client's IP address
        if is_routable:# The client's IP address is publicly routable on the Internet
            client_ip= ip
        else:
            # The client's IP address is private
            return HttpResponse("Ip address is private!")
        return ip if validate_ip(ip) else None

class get_location_details():
    def __init__(self,ip):
        self.ip = ip
        self.location_key,self.response = self.get_response()

    def get_response(self):
        response = requests.get("http://dataservice.accuweather.com/locations/v1/cities/ipaddress?apikey={}&q={}".format(ACCU_API, self.ip))
        self.response = response.json()
        self.location_key= self.response["Key"]
        return self.response,self.location_key


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

