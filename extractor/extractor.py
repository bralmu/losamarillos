#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import sqlite3
import sys
import time
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
    writeToDataBase(origins=origins)    
    
def writeToDataBase(origin=None, destinations=None, origins=None):
    conn = sqlite3.connect(DBFILE)
    print("Local database opened\t✓")
    if(origins):
        conn.execute('''DROP TABLE IF EXISTS ORIGINS;''')
        conn.execute('''CREATE TABLE ORIGINS (NAME TEXT PRIMARY KEY NOT NULL);''')
        print("Origins table created\t✓")
        for x in range(0, len(origins)):
            conn.execute('INSERT INTO ORIGINS (NAME) VALUES ("%s")' % (origins[x]))
        conn.commit()        
        print("Origins rows inserted\t✓")
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
    
def getTimes():
    conn = sqlite3.connect(DBFILE)
    cursor = conn.execute('SELECT ORIGIN, DESTINATION FROM EDGES')    
    for row in cursor:
        origin = row[0]
        destination = row[1]
        print("Origen: %s\tDestino: %s" % (origin, destination))
        url = 'https://regular.autobusing.com/venta/horarios'
        headers = {'cookie': 'rack.session=BAh7CUkiC2xvY2FsZQY6BkVGSSIHZXMGOwBUSSIPZW1wcmVzYV9pZAY7AEZp%0ADEkiD3Nlc3Npb25faWQGOwBUSSJFNmExMWE2OTZiMzMxYjA5YmVmZjc5ODJl%0AZmQ5NzZiZTVjZmUwZDg5ODhiOWIyMTQ5YTY5OTBjMTYwZDZjN2Y0YwY7AEZJ%0AIghvcGUGOwBGew86DXRpcG9faXl2SSIIaWRhBjsAVDoPZW1wcmVzYV9pZGkM%0AOhJzaW5mZV9lbXByZXNhSSIHMDEGOwBUOg5vcmlnZW5faWRpAsIFOg9kZXN0%0AaW5vX2lkaQLOBToOZmVjaGFfaWRhVToJRGF0ZVsLaQBpA7F%2FJWkAaQBpAGYM%0AMjI5OTE2MToOZmVjaGFfdnRhMDoNY2FudGlkYWRpBjoUaG9yYXJpb3NfaWRh%0AX2lkaQM%2B8As6C3NlZ3Vyb2kA%0A--2e639325338b8e9bf4068ca59a7b306e16fc8f2f; path=/; HttpOnly'}
        payload = {'empresa': "losamarillos",
                   'venta[origen_nombre]': origin,
                   'venta[destino_nombre]': destination,
                   'venta[fecha_ida]': "12/05/2016",
                   'venta[fecha_vta]': "",
                   'venta[cantidad]': "1",
                   'venta[tipo_iyv]': "ida"}
        r = requests.get(url, headers=headers, params=payload)
        print(r.content)
        trips = getTripFromHTML(r.content.decode())
        time.sleep(2)
    conn.close()


getOriginsFromWebsite(True)
getDestinationsFromWebsite()
#getTimes()
