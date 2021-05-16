#!/usr/bin/python

import datetime, os, time
now = datetime.datetime.now()
now_time = now.strftime("%H%M")

while int(now_time) >= 915 and int(now_time) <= 1530:
    os.system('python /Users/mandar.shinde/personal/nse/nse_scrapper.py')
    time.sleep(300)
    now = datetime.datetime.now()
    now_time = now.strftime("%H%M")
