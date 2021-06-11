#!/usr/bin/env python3

from cysystemd.reader import JournalReader, JournalOpenMode, Rule
from pathlib import Path
import re
import time
import os

LOG_DIR = "sshd_monitor"

rules = (
   Rule("SYSLOG_IDENTIFIER", "sshd") &
   Rule("_SYSTEMD_UNIT", "sshd.service")
)

reader = JournalReader()
reader.open(JournalOpenMode.SYSTEM)
reader.add_filter(rules)
reader.seek_tail()

poll_timeout = 255

def get_target_logdir():
   currentYear = time.strftime("%y")
   currentMonth = time.strftime("%m")
   targetLogdir = os.path.join(LOG_DIR, currentYear, currentMonth)
   Path(targetLogdir).mkdir(parents=True, exist_ok=True)
   return targetLogdir

def get_target_logfile():
   currentDay = time.strftime("%d")
   targetLogfile = os.path.join(get_target_logdir(), currentDay+".log")
   return open(targetLogfile, 'a')

hourTimeFormat = "%H:%M:%S"

def log_fail(match):
   currentTimeStr = time.strftime(hourTimeFormat)
   currentDayLogfile = get_target_logfile()
   print(currentTimeStr,'FAILED', match.group(1), match.group(2), sep='\t', file=currentDayLogfile)
   currentDayLogfile.close()

def log_success(match):
   currentTimeStr = time.strftime(hourTimeFormat)
   currentDayLogfile = get_target_logfile()
   print(currentTimeStr, "ACCEPT", match.group(2), match.group(3), match.group(1), sep="\t", file=currentDayLogfile)
   currentDayLogfile.close()

failedLoginPattern = r"Failed\ password\ for\ (?:invalid user\ )?([\S]*)\ from\ (\S*).*"
failedLogin = re.compile(failedLoginPattern)
successfulLoginPattern = r"Accepted\ ((?:publickey)|(?:password))\ for\ (\S*)\ from\ (\S*).*"
successfulLogin = re.compile(successfulLoginPattern)

while True:
   reader.wait(poll_timeout)

   for record in reader:
      journalMsg = record.data['MESSAGE']
      if failedLogin.match(journalMsg):
         log_fail(failedLogin.match(journalMsg))
      elif successfulLogin.match(journalMsg):
         log_success(successfulLogin.match(journalMsg))
      else:
         pass
