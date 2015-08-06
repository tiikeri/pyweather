import os, subprocess, json, sys, time
from urllib2 import urlopen
def getIP():
    IPAddress = urlopen('http://ip.42.pl/raw').read() 
    os.system('wget http://ip-api.com/json/%s -qO .raw.userlocation.json' % (IPAddress)) 
    subprocess.Popen(['./parseJson.sh location'], shell = True) 
def get():
    global formatted_address, zipcode, iso_country_code, city
    lines = [line.rstrip('\n') for line in open('.userlocation.json')]
    for i, line in enumerate(lines):
        if i == 13:
            zipcode = line
    os.system('wget http://maps.googleapis.com/maps/api/geocode/json?address=%s -qO .googlemaps.json' % (zipcode)) 
    with open('.googlemaps.json') as data_file:    
        data = json.load(data_file)
    formatted_address = data["results"][0]["formatted_address"]
    iso_country_code = data["results"][0]["address_components"][-1]["short_name"]
    city = data["results"][0]["address_components"][1]["long_name"]
    if iso_country_code == "US":
        state = data["results"][0]["address_components"][-2]["short_name"]
def repl():
    global formatted_address, zipcode, iso_country_code, city, state
    os.system('wget http://maps.googleapis.com/maps/api/geocode/json?address=%s -qO .googlemaps.json' % (zipcode)) 
    with open('.googlemaps.json') as data_file:    
        data = json.load(data_file)
    formatted_address = data["results"][0]["formatted_address"]
    city = data["results"][0]["address_components"][1]["long_name"]
    iso_country_code = data["results"][0]["address_components"][-1]["short_name"]
    if iso_country_code == "US":
        state = data["results"][0]["address_components"][-2]["short_name"]
    print "Address replaced with " + formatted_address + "."
    time.sleep(5)
def check():
        yes = set(['yes','y', 'ye', ''])
        no = set(['no','n'])
        global zipcode
        print "Is this your location?: " + formatted_address 
        sys.stdout.write("[y/n]    ")
        response = raw_input()
        if (response in yes) == False and (response in no) == False:
            while 1:
                print "Try again."
                response = raw_input()
                if response in yes or response in no:
                    break
        if response in yes:
            print "OK."
            autolocate_status = "correct"
        elif response in no:
            sys.stdout.write("Sorry about that - please enter your city's ZIP code.      ")
            while 1:
                zipcode = raw_input()
                print "So your ZIP code is %s? [y/n]" % zipcode
                response_b = raw_input()
                if response_b in yes:
                    print "Got it."
                    repl()
                    break
                if response_b in no:
                    print "Please enter your ZIP code."; pass
                    os.system('wget http://maps.googleapis.com/maps/api/geocode/json?address=%s -qO .googlemaps.json' % (zipcode)) 
def getWeather():
    global zipcode, iso_country_code
    os.system('wget "http://api.openweathermap.org/data/2.5/weather?zip=' + zipcode + ',' + iso_country_code + '&units=imperial" -qO .weather.json')
    with open('.weather.json') as data_file:    
        weather = json.load(data_file)
    errorcode = weather.get("cod")
    if errorcode == "404":
        print "Sorry! Your area couldn't be found using this API. Try searching for a more general area."
        exit(1)
    condition = weather["weather"][0]["main"]
    temp = json.dumps(weather["main"]["temp"])
    hitemp = json.dumps(weather["main"]["temp_max"])
    lotemp = json.dumps(weather["main"]["temp_min"])
    humidity = json.dumps(weather["main"]["humidity"])
    pressure = json.dumps(weather["main"]["pressure"])
    print "CONDITION                    %s    " % condition
    print "TEMPERATURE                  %sF  " % temp
    print "HIGH                         %sF  " % hitemp
    print "LOW                          %sF  " % lotemp
    print "HUMIDITY                     %s%%    " % humidity
    print "PRESSURE                     %smbar" % pressure
    
######
getIP()
get()
check()
getWeather()

    
    
