#!/usr/bin/env python
import os
import sys
from urlparse import urljoin

import requests

BASE_URL = "http://raw.githubusercontent.com/"

try:
    arg = sys.argv[1]
    rep_count = int(sys.argv[2])
except IndexError:
    rep_count = None
    print("No repeation count given, default is 1000.")

# swift smoke tests and xss

try:
    if arg == 'create_containers':
        # create a set of containers
        for i in range(rep_count or 1000):
            os.system('ccurl.py -r container_{} -X PUT'.format(str(i)))
    if arg == 'delete_containers':
        # delete a list of containers
        for i in range(100, 1000):
            os.system('ccurl.py -r object_{} -X DELETE'.format(str(i)))
    if arg == 'xssp_containers':
        # xss container names with polygot xss strings
        xss_list = requests.get(
            urljoin
            (BASE_URL,
             "/fuzzdb-project/fuzzdb/master/attack/xss/XSSPolyglot.txt")
        ).content.split("\n")
        for i in xss_list:
            os.system('ccurl.py  -r {{0}} -X PUT'.format(str(i)))


except KeyboardInterrupt:
    print("Exiting..>>")
