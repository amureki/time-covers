#!/usr/bin/python
import datetime
import locale
import logging
import os
import re
import time
from twython import Twython
from urllib2 import urlopen, HTTPError

SCRIPT_PATH = ''

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''

logging.basicConfig(filename=SCRIPT_PATH+'debug.log', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%d.%m.%Y %H:%M:%S')

twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET, 
                    ACCESS_KEY, ACCESS_SECRET)

url_main = 'http://img.timeinc.net/time/magazine/archive/covers/'
today = str.replace(str(datetime.date.today()).lstrip('20'), '-', '')
year = str(datetime.date.today().year)
url_today = url_main + year + '/1101' + today + '_600.jpg'
url_prev = 'http://img.timeinc.net/time/images/covers/europe/2013/20131202_600.jpg'
status = str(datetime.date.today().strftime('%B, %d'))

try:
    try:
        cover = urlopen(url_today).read()
        logging.debug('Cover URL for today: %s', url_today)
        f = open(url_today[57:], 'w+b')
        logging.debug('Cover opened: %s', f)
        f.write(cover)
        f.close
        media = open(url_today[57:], 'rb')
        twitter.update_status_with_media(status=status, media=media)
        logging.debug('Cover uploaded to twitter.')
    except HTTPError, e:
        if e.code == 404:
            e.msg = 'data not found on remote: %s' % e.msg
            logging.debug('No covers for today.')
        raise
except HTTPError, e:
    print e

logging.debug("*************************************************")
logging.debug("")