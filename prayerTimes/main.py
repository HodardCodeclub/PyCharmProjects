#!/usr/bin/python
#-*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import sys, os

url = 'http://www.diyanet.gov.tr/en/PrayerTime/PrayerTimesList'

country = 2     #default country => Turkey
state = 500     #default state => Adana
district = -1     #default district => -1(None)
period = 'Haftalik'     #default period => Haftalik

def unicodeEncode(txt):
    s = u' '.join((txt, '')).encode('utf-8').strip()
    return str(s)

def start():
    getCountries()
    selectCountry()
    getStates()
    selectState()
    getDistricts()
    parameters = {}
    if os.stat("districts.txt").st_size == 0:
        parameters = {'Country': country, 'State': state}
    else:
        selectDistrict()
        parameters = {'Country': country, 'State': state, 'City': district}
    selectPeriod()
    parameters.update({'period': period})
    getPrayerTimes(parameters)

def getCountries():
    params = {}
    r = requests.post(url, data=params)
    page = r.text

    f = open('countries.txt', 'w')

    soup = BeautifulSoup(page)
    for span in soup.find_all('span'):
        sel = span.find('select', {'id': 'Country', 'name': 'Country'})
        if sel != None:
            for opt in sel.find_all('option'):
                if opt.text != "" and opt.get('value') != "":
                    f.write(opt.text + ": " + str(opt.get('value')) + "\n")

    f.close()

def selectCountry():
    f = open('countries.txt', 'r')
    lines = f.readlines()
    f.close()
    for line in lines:
        print line,
    global country
    country = raw_input('Select Country: ')
    print "----------------"

def getStates():
    params = {'Country': country}
    r = requests.post(url, data=params)
    page = r.text

    f = open('states.txt', 'w')

    soup = BeautifulSoup(page)
    for span in soup.find_all('span'):
        sel = span.find('select', {'id': 'State', 'name': 'State'})
        if sel != None:
            for opt in sel.find_all('option'):
                if opt.text != "" and opt.get('value') != "":
                    f.write(opt.text + ": " + str(opt.get('value')) + "\n")

    f.close()

def selectState():
    f = open('states.txt', 'r')
    lines = f.readlines()
    f.close()
    for line in lines:
        print line,
    global state
    state = raw_input('Select State: ')
    print "----------------"

def getDistricts():
    params = {'Country': country, 'State': state}
    r = requests.post(url, data=params)
    page = r.text

    f = open('districts.txt', 'w')

    soup = BeautifulSoup(page)
    for span in soup.find_all('span'):
        sel = span.find('select', {'id': 'City', 'name': 'City'})
        if sel != None:
            for opt in sel.find_all('option'):
                if opt.text != "" and opt.get('value') != "":
                    f.write(opt.text + ": " + str(opt.get('value')) + "\n")
    f.close()

def selectDistrict():
    f = open('districts.txt', 'r')
    lines = f.readlines()
    f.close()
    for line in lines:
        print line,
    global district
    district = raw_input('Select District: ')
    print "----------------"

def selectPeriod():
    global period
    print "Haftalik: 1\nAylik: 2"
    c = int(raw_input('Select Period: '))
    print "----------------"
    if c == 1:
        period = 'Haftalik'
    elif c == 2:
        period = 'Aylik'
    else:
        print "Wrong input, period is Haftalik(default)"

def getPrayerTimes(params):
    try:
        r = requests.post(url, data=params)
        if not r.status_code == requests.codes.ok:
            with open('times.txt', "w"):
                pass
            print r.raise_for_status()
            sys.exit(1)
    except requests.exceptions.HTTPError as e:
        print e
        sys.exit(1)
    page = r.text
    #print page

    f = open('times.txt', 'w')

    f.write("Country: " + str(params.get('Country')) + "\n")
    f.write("State: " + str(params.get('State')) + "\n")
    if len(params) == 4:
        f.write("District: " + str(params.get('City')) + "\n")

    soup = BeautifulSoup(page)
    for tbody in soup.find_all('tbody'):
        tr = tbody.find_all('tr')
        for td in tr:
            f.write(td.text + '\n')
            f.write("\n-------------\n\n")

if __name__ == '__main__':
    start()