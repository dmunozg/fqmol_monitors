#!/usr/bin/env python3

import requests
import os

pingURL = 'https://healthchecks.asgamers.net/ping/d0eead86-dc6b-48b1-8461-a2e0d56ddb3e'
hostList = ['ceylan3', 'ceylan4']

def check_online(host):
    response = os.system('ping -c 1 '+host+' > /dev/null')
    if response == 0:
        return True
    else:
        return False

def healthcheck_report(status=0, msg=''): # 0 for success, 1 for failure
    if status == 0:
        requests.get(pingURL, timeout=20)
    else:
        requests.post(pingURL+'/fail', data=msg)

onlineMachines = 0
for host in hostList:
    if check_online(host):
        onlineMachines += 1
    else:
        pass

if onlineMachines == len(hostList):
    healthcheck_report()
else:
    machinesDown = len(hostList)-onlineMachines
    healthcheck_report(1, '{} nodes down'.format(machinesDown))
        
