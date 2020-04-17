#!/usr/bin/env python3
import sys
import getpass
import json
try:
  from tenable.reports import NessusReportv2
except ModuleNotFoundError:
  print('pyTenable module must be installe via pip')
  exit(1)


report_item_keys = [ 'port', 'svc_name', 'protocol', 'severity', \
'pluginID', 'pluginName', 'pluginFamily', 'host-report-name', \
'HOST_END_TIMESTAMP', 'HOST_END', 'LastAuthenticatedResults', \
'policy-used', 'cpe', 'os', 'operating-system-conf', \
'operating-system-method', 'mac-address', 'ssh-fingerprint', \
'cpe-0', 'patch-summary-total-cves', 'system-type', \
'operating-system', 'source_name', 'Credentialed_Scan', \
'ssh-login-used', 'local-checks-proto', 'ssh-auth-meth', \
'traceroute-hop-4', 'traceroute-hop-3', 'traceroute-hop-2', \
'traceroute-hop-1', 'traceroute-hop-0', 'sinfp-ml-prediction', \
'sinfp-signature', 'host-fqdn', 'host-rdns', 'host-ip', \
'HOST_START_TIMESTAMP', 'HOST_START', 'plugin_output' ]

desired_keys_to_print = [ 'host-ip', 'host-fqdn','os', 'Credentialed_Scan', \
'pluginID' ]

def print_report_item(report_item):
  for key in desired_keys_to_print:
    print(key + ': ' + str(report_item.get(key)))
  print()

def find_ip_in_nessus_file(file_name, ip):
  with open(file_name) as nessus_file:
    report = NessusReportv2(nessus_file)
    [ (print_report_item(item)) for item in report if item.get('host-ip') == ip ]
