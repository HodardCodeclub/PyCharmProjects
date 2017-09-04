import requests
import re

f = open('info.json', 'w')

def parseCities(countryid, countryname):
    url = 'https://namazvakitleri.com.tr/ulke/'
    url = url + countryid + "/" + countryname
    r = requests.get(url)
    pattern = re.compile('<li><a href=(\"https://namazvakitleri\.com\.tr/sehir/(\d+)/([a-zA-Z-]+)/(\w+)\")>([a-zA-Z- ]+)</a>')
    res = pattern.findall(r.text)
    f.write("\t\t\t\"Cities\": [\n")
    for i in range(0, len(res)):
        x = res[i]
        f.write("\t\t\t\t{\n")
        f.write("\t\t\t\t\t\"id\": " + "\""+ x[1] + "\",\n")
        f.write("\t\t\t\t\t\"name\": " + "\""+ x[4] + "\",\n")
        #f.write("\t\t\t\t\t\"id\": " + "\""+ x[1] + "\",\n")
        f.write("\t\t\t\t\t\"link\": " + x[0] + "\n")
        if(i == len(res)-1):
            f.write("\t\t\t\t}\n")
        else:
            f.write("\t\t\t\t},\n")
    f.write("\t\t\t]\n")

def parseCountries():
    url = 'https://namazvakitleri.com.tr/ulkeler'
    r = requests.get(url)
    pattern = re.compile('<li><a href=\"https://namazvakitleri\.com\.tr/ulke/(\d+)/(\w+)\">(\w+)</a>')
    res = pattern.findall(r.text)
    f.write("\t\"Countries\": [\n")
    for i in range(0, len(res)):
        x = res[i]
        f.write("\t\t{\n")
        f.write("\t\t\t\"Name\":" + "\"" + x[1] + "\",\n")
        #f.write("\t\t\t\"ID\":" + "\"" + x[0] + "\",\n")
        parseCities(x[0], x[1])
        if(i == len(res)-1):
            f.write("\t\t}\n")
        else:
            f.write("\t\t},\n")
    f.write("\t]\n")

f.write("{\n")
parseCountries()
f.write("}")
f.close()
