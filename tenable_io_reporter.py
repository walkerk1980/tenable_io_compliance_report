#!/usr/bin/env python3
import json
import sys
from tenable_functions import *
from mongo_functions import *
#from csv_functions import *
from nessus_file import *

endpoint_address='cloud.tenable.com'
MONGO_HOST = 'localhost'
MONGO_PORT = 27017

mongo_collections = setup_mongo(MONGO_HOST, MONGO_PORT)
scans_col = mongo_collections[0]

try:
  tenable_access_key = sys.argv[1]
except:
  tenable_access_key = ''

io = tenable_login(endpoint_address)

scan_list = get_scan_list(io)

print_scan_list(scan_list)

scan_id = '53'

scan_results = get_scan_results(io, scan_id)

print()
for key in scan_results.keys():
  if key in ['info']: #, 'compliance']:
    print('{0}: {1}'.format(key, scan_results.get(key)))
    pass
exit()


for scan in scan_53_results.get('compliance'):
  print()
  for key in scan.keys():
    print('{0}: {1}'.format(key, scan.get(key)))
    pass

#print(dir(io.scans.results))

#vulnerability_list = 

#scan_944_details = sc.scans.details('944')

#print('assets: ' + str(scan_944_details.get('assets')))
#print('ip_list: ' + scan_944_details.get('ipList'))

#find_ip_in_nessus_file('1508.nessus', '10.10.9.82')

