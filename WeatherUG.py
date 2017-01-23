# This is for Weather Underground API
import urllib2, json, logging, time
import PrivateResource

REQUEST_URL_HOME = "http://api.wunderground.com"
API_KEY = PrivateResource.WU_API

def getHourlyFC(zipcode):
    url = "%s/api/%s/hourly/q/%s.json" % (REQUEST_URL_HOME, API_KEY, str(zipcode))
    respJson = requestWUG(url)
    return respJson

def getWeeklyFC(zipcode):
    url = "%s/api/%s/forecast/q/%s.json" % (REQUEST_URL_HOME, API_KEY, str(zipcode))
    respJson = requestWUG(url)
    return respJson

def getWeeklyFC_Overall(zipcode, day_after):
    respJson = getWeeklyFC(zipcode)
    forecastJson = respJson['forecast']['simpleforecast']['forecastday'][day_after]
    temp_high = forecastJson["high"]["celsius"]
    temp_low = forecastJson["low"]["celsius"]
    condition = forecastJson["conditions"]
    cond_icon = forecastJson["icon_url"]
    qpf_day = forecastJson["qpf_allday"]
    return {"condition": condition, "icon": cond_icon, "temp_high": temp_high, "temp_low": temp_low, "gpf_day": qpf_day["mm"]}

def getHourlyFC_QPF(zipcode):
    respJson = getHourlyFC(zipcode)
    forecastJson = respJson['hourly_forecast']
    qpf = []
    for item in forecastJson:
        if int(item["qpf"]["metric"]) > 0:
            qpf.append({"hour":int(item["FCTIME"]["hour_padded"]), "qpf":float(item["qpf"]["metric"])})
    return qpf

def getHourlyFC_HTSensor(zipcode):
    respJson = getHourlyFC(zipcode)
    forecastJson = respJson['hourly_forecast']
    newFormat = []
    for item in forecastJson:
        hourly = {}
        hourly['zipcode'] = zipcode
        hourly['tstamp'] = int(item['FCTTIME']['epoch'])
        hourly['temp'] = item['temp']['metric']
        hourly['humidity'] = item['humidity']
        newFormat.append(hourly)
    return newFormat

def requestWUG(url):
    errorCount = 10
    while errorCount > 0:
        #response = requests.get(url)
        resp = urllib2.urlopen(url)
        #str_response = response.text.decode('utf-8')
        str_response = resp.read().decode('utf-8')
        obj = json.loads(str_response)
        if 'error' in obj['response']:
            print("Error in retrieving data. Trying again...")
            logging.error("DataRetrievalError - TWC API Error")
            # Retrying after 1 sec
            time.sleep(1)
        else:
            errorCount = 0
    return obj

