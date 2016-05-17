# -*- coding: utf-8 -*-

import re

class Trip:
    def __init__(self, departureTime, arrivalTime, price):
        self.departureTime = departureTime
        self.arrivalTime = arrivalTime
        self.price = price

# Uses regex to extract times and prices from html, generates trips and returns them.
def getTripFromHTML(rawdata):
    prehoursre = re.compile('<td><strong>\d\d:\d\d</strong></td>')
    prepricesre = re.compile('<td class="numeric">\d+,\d+€</td></tr>')
    prehourslist = prehoursre.findall(rawdata)
    prepriceslist = prepricesre.findall(rawdata)
    hoursre = re.compile('\d\d:\d\d')
    pricesre = re.compile('\d+,\d+')
    hourslist = []
    priceslist = []
    for prehourelement in prehourslist:
        hourmatch = hoursre.findall(prehourelement)
        hourslist.append(hourmatch[0])        
    for prepriceelement in prepriceslist:
        pricematch = pricesre.findall(prepriceelement)
        priceslist.append(pricematch[0])
    trips = []
    for i in range (0, len(priceslist)):
        trips.append(Trip(hourslist[2*i], hourslist[2*i+1], float(priceslist[i].replace(",", "."))))   
    for trip in trips:
        print(trip.departureTime, " ", trip.arrivalTime, " ", trip.price)
    return trips
