# -*- coding: utf-8 -*-
import socket,os,requests
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from ipware import get_client_ip


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
        # Unable to get the client's IP address'
        return HttpResponse("Ip address not found!")
    else:
        # We got the client's IP address
        if is_routable:  # The client's IP address is publicly routable on the Internet
            client_ip = ip
        else:
            # The client's IP address is private
            return HttpResponse("Ip address is private!")
        ip= requests.get('https://checkip.amazonaws.com').text.strip()  # remove on production!!!
        return ip if validate_ip(ip) else None


