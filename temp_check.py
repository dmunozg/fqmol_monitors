#!/usr/bin/env python3

import requests
import os
import re
import subprocess as sb

pingURL = 'https://healthchecks.asgamers.net/ping/5baa96d5-34be-4b94-b450-85068204aaec'
temperatureThreshold = 60

def healthcheck_report(status=0, msg=''): # 0 for success, 1 for failure
    if status == 0:
        requests.post(pingURL, data=msg, timeout=20)
    else:
        requests.post(pingURL+'/fail', data=msg, timeout=20)

def check_current_temperature():
    temperaturePattern = re.compile(r'\s\stemp[\d]{1,2}_input:\s([-\d.]+)')
    sensorsCheck = sb.run(["sensors", "-u"], stdout=sb.PIPE)
    temperaturesMeasured = temperaturePattern.findall(str(sensorsCheck.stdout))
    # Transform the list of strings obtained to a list of float
    temperaturesMeasured = list(map(float, temperaturesMeasured))
    return max(temperaturesMeasured)

currentTemperature = check_current_temperature()
tempMessage = "Temp: {} C".format(currentTemperature)
if currentTemperature >= temperatureThreshold:
    healthcheck_report(1, msg=tempMessage)
else:
    healthcheck_report(0, msg=tempMessage)
