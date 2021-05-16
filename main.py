#!/usr/bin/python

import datetime, os, time
now = datetime.datetime.now()
now_time = now.strftime("%H%M")

# Until the time between 09:15 and 15:30, sleep for 5 min
while int(now_time) < 915 or int(now_time) >= 1530:
    time.sleep(300)

# If time is between 09:15 and 15:30, start pulling the data every 5 mins
while int(now_time) >= 915 and int(now_time) <= 1530:
    os.system('python /Users/mandar.shinde/personal/nse/nse_scrapper.py')
    time.sleep(300)
    now = datetime.datetime.now()
    now_time = now.strftime("%H%M")
