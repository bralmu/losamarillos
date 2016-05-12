#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import sqlite3
import sys
import time
import threading
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from htmlscraper import getTripFromHTML

DBFILE = 'schedule.db'

def getOriginsFromWebsite(simulation=False):
    if not simulation:
        try:
            url = 'https://regular.autobusing.com/parada_nombres'
            headers = {'cookie': 'rack.session=BAh7CUkiC2xvY2FsZQY6BkVGSSIHZXMGOwBUSSIPZW1wcmVzYV9pZAY7AEZp%0ADEkiD3Nlc3Npb25faWQGOwBUSSJFM2RlMDlkZjEzNjFhMmRiYzQ3ZTMzZGYw%0ANzFhN2RkYTdkYTRiNTZkMjg5Yjk2YzdkYjM2NWUwYzM1OWViYjY5NAY7AEZJ%0AIghvcGUGOwBGew86DXRpcG9faXl2SSIIaWRhBjsAVDoPZW1wcmVzYV9pZGkM%0AOhJzaW5mZV9lbXByZXNhMDoOb3JpZ2VuX2lkaQLyBToPZGVzdGlub19pZGkC%0A9AU6DmZlY2hhX2lkYVU6CURhdGVbC2kAaQOvfyVpAGkAaQBmDDIyOTkxNjE6%0ADmZlY2hhX3Z0YTA6DWNhbnRpZGFkaQY6FGhvcmFyaW9zX2lkYV9pZGkD6%2BoL%0AOgtzZWd1cm9pAA%3D%3D%0A--c959624cf7ff5bc4a94992a4ae66f2256532d407'}
            r = requests.get(url, headers=headers)
        except:
            print("Retrieving origins from autobusing.com FAILED\t✕")
            exit()
    else:
        class Object(object):
            pass
        r = Object()
        r.content = '["ALGAR","ALCALA DEL VALLE","ALGODONALES","ALJAIMA","ALMARGEN","ALMENDRALEJO","ARCOS DE LA FRONTERA","ARDALES","BADAJOZ","BENALMADENA","BENAMAHOMA","BENAOCAZ","BENAOJAN","BORNOS","CADIZ","CALZADILLA","CAMAS","CAÑETE LA REAL","CARRATRACA","CHIPIONA","COSTA BALLENA","CRUCE DE LAS CABEZAS","CRUCE SERRATO","CRUCE SEVILLA","CUEVAS DEL BECERRO","D.BENITO","DOS HERMANAS","EL BOSQUE","EL RONQUILLO","EL TORBISCAL","EMPALME CAÑETE","ESPERA","ESTACION DE CARTAMA","FTE.CANTOS","FUENGIROLA","GRAZALEMA","GUAREÑA","HOSPITAL C, SOL","INTERMEDIO RONDA","JEDULA","JEREZ","LAS CABEZAS","LAS PAJANOSAS","LEBRIJA","LOS PALACIOS","LOS SANTOS","MADRID","MALAGA","MALAGA PORTILLO","MARBELLA","MENGABRIL","MERIDA","MONESTERIO","MONTECORTO","MONTEJAQUE","OLVERA","PRADO DEL REY","PUERTO REAL","PUERTO SANTA MARIA","RONDA","ROTA","SAN FERNANDO","SANLUCAR D BARRAMEDA","SAN PEDRO","SANTIPONCE","SETENIL","SEVILLA PRADO S.S.","STA.MARTA","STA.OLALLA","TORRE ALHAQUIME","TORREMEGIAS","TORREMOLINOS","TREBUJENA","UBRIQUE","UTRERA","VALVERDE MERIDA","VCA.BARROS","VENTA SEBASTIAN","VILLALUENGA","VILLAMARTIN","VTA.CULEBRIN","VVA.SERENA","ZAFRA"]'
    origins = json.loads(r.content)
    print("Origins retrieved from autobusing.com\t✓")
    conn = sqlite3.connect(DBFILE)
    print("Local database opened\t✓")
    conn.execute('''DROP TABLE IF EXISTS ORIGINS;''')
    conn.execute('''CREATE TABLE ORIGINS (NAME TEXT PRIMARY KEY NOT NULL);''')
    print("Origins table created\t✓")
    for x in range(0, len(origins)):
        conn.execute('INSERT INTO ORIGINS (NAME) VALUES ("%s")' % (origins[x]))
    conn.commit()        
    print("%s Origins rows inserted\t✓" % (len(origins)))
    conn.close()
    
def getDestinationsFromWebsite():
    url = 'https://regular.autobusing.com/parada_nombre_destinos'
    headers = {'cookie': 'rack.session=BAh7CUkiC2xvY2FsZQY6BkVGSSIHZXMGOwBUSSIPZW1wcmVzYV9pZAY7AEZp%0ADEkiD3Nlc3Npb25faWQGOwBUSSJFM2RlMDlkZjEzNjFhMmRiYzQ3ZTMzZGYw%0ANzFhN2RkYTdkYTRiNTZkMjg5Yjk2YzdkYjM2NWUwYzM1OWViYjY5NAY7AEZJ%0AIghvcGUGOwBGew86DXRpcG9faXl2SSIIaWRhBjsAVDoPZW1wcmVzYV9pZGkM%0AOhJzaW5mZV9lbXByZXNhMDoOb3JpZ2VuX2lkaQLyBToPZGVzdGlub19pZGkC%0A9AU6DmZlY2hhX2lkYVU6CURhdGVbC2kAaQOvfyVpAGkAaQBmDDIyOTkxNjE6%0ADmZlY2hhX3Z0YTA6DWNhbnRpZGFkaQY6FGhvcmFyaW9zX2lkYV9pZGkD6%2BoL%0AOgtzZWd1cm9pAA%3D%3D%0A--c959624cf7ff5bc4a94992a4ae66f2256532d407'}
    conn = sqlite3.connect(DBFILE)
    conn.execute('''DROP TABLE IF EXISTS EDGES''')
    conn.execute('''CREATE TABLE EDGES 
                    (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    ORIGIN TEXT NOT NULL,
                    DESTINATION TEXT NOT NULL);''')
    print("Edges table created\t✓")
    cursor = conn.execute('SELECT NAME FROM ORIGINS;')
    for row in cursor:
        print("\tDestinations from %s: " % (row[0]), end="")
        payload = {'nombre': row[0]}
        r = requests.get(url, headers=headers, params=payload)
        destinations = json.loads(r.content.decode())
        for x in range(0, len(destinations)):
            print("%s, " % (destinations[x]), end="")
            conn.execute('''INSERT INTO EDGES (ORIGIN, DESTINATION) VALUES ("%s", "%s");''' % (row[0], destinations[x]))
        print("✓")
        time.sleep(.2)
    conn.commit()
    print("Edges rows inserted\t✓")
    conn.close()
    
def getTimesAndPrices(thisthreadid, totalthreads, origins, destinations, date):
    global finished
    driver = webdriver.Firefox()
    for i in range(0, len(origins)):
        if i % totalthreads == thisthreadid:
            origin = origins[i]
            destination = destinations[i]
            print("(Thread %d, Case %d) Retrieving timetable and prices from %s to %s on %s" % (thisthreadid, i, origin, destination, date))
            try:
                driver.get("http://losamarillos.autobusing.com/")
                assert "Los Amarillos" in driver.title
                elem = driver.find_element_by_id("origen_nombre")
                elem.send_keys(origin)
                elem = driver.find_element_by_id("destino_nombre")
                elem.send_keys(destination)
                elem = driver.find_element_by_id("fecha_ida")
                elem.send_keys(date)
                elem.send_keys(Keys.RETURN)
                trips = getTripFromHTML(driver.page_source)
                if trips:
                    for trip in trips:
                        conn = sqlite3.connect(DBFILE)
                        conn.execute('INSERT INTO SCHEDULE (ORIGIN, DESTINATION, DEPARTURE_TIME, ARRIVAL_TIME, PRICE) VALUES ("%s", "%s", "%s", "%s", %f);' % (origin, destination, trip.departureTime, trip.arrivalTime, trip.price))
                        conn.commit()
                        conn.close()
            except:
                print("There was a problem with case %d. Skipping to next case." % (i))
    finished[thisthreadid] = True


getOriginsFromWebsite(True) #extracts and saves origin location names
getDestinationsFromWebsite() #extracts and saves destination location names for each origin, creating origin-destination pairs.

# creates empty schedule table
conn = sqlite3.connect(DBFILE)
conn.execute('''DROP TABLE IF EXISTS SCHEDULE''')
conn.execute('''CREATE TABLE SCHEDULE 
                (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                ORIGIN TEXT NOT NULL,
                DESTINATION TEXT NOT NULL,
                DEPARTURE_TIME TEXT NOT NULL,
                ARRIVAL_TIME TEXT NOT NULL,
                PRICE INT NOT NULL);''')
                
# loads to memory all origin-destination pairs from the local database.
cursor = conn.execute('SELECT ORIGIN, DESTINATION FROM EDGES')
origins = []
destinations = []
for row in cursor:
    origins.append(row[0])
    destinations.append(row[1])
conn.close()

# extracts times and prices for each origin-destination pair on date DATE
DATE = "13/05/2016"
SELENIUM_THREADS = 2 # can use multiple threads to go extract data faster
finished = [False] * SELENIUM_THREADS # global flag to know if the threads have finished
tlist = []
for threadid in range(0, SELENIUM_THREADS):
    tlist.append(threading.Thread(target=getTimesAndPrices, args=(threadid, SELENIUM_THREADS, origins, destinations, DATE)))
    tlist[threadid].start()

def allFinished():
    for v in finished:
        if not v:
            return False
    return True
    
while not allFinished(): # keeps the program alive while threads are still working.
    time.sleep(2) # checks again every 2 seconds.
    
print("The End.")
