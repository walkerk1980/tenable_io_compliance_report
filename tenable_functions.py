#!/usr/bin/env python3
import sys
import getpass
import json
import configparser
from os.path import expanduser
try:
  from tenable.io import TenableIO
  import tenable
except ModuleNotFoundError:
  print('pyTenable module must be installed via pip')
  exit(1)

def read_credentials_file(config_filename = '.tenable_io_credentials'):
        home = expanduser("~")
        filename = home + '/' + config_filename

        # Read in the existing config file
        config = configparser.RawConfigParser()
        config.read(filename)

        if not config.has_section('tenable_io'):
          return(None)
        access_key = config.get('tenable_io', 'access_key')
        secret_key = config.get('tenable_io', 'secret_key')

        if access_key and secret_key:
          print('\n\r Received credentials from config file ' + config_filename)
          return({
            'access_key': access_key,
            'secret_key': secret_key,
          })

def write_credentials_file(access_key, secret_key, config_filename = '.tenable_io_credentials'):
        home = expanduser("~")
        filename = home + '/' + config_filename

        config = configparser.RawConfigParser()
        config.read(filename)

        if not config.has_section('tenable_io'):
            config.add_section('tenable_io')

        config.set('tenable_io', 'access_key', access_key)
        config.set('tenable_io', 'secret_key', secret_key)

        with open(filename, 'w+') as configfile:
            config.write(configfile)

        print('\n\rCredentials have been stored in the configuration file {0} under the tenable_io profile.'.format(filename))

def test_io_login(access_key, secret_key):
  print('\n\r testing login...\n\r')
  io = TenableIO(access_key, secret_key)
  try:
    sesson_details = io.session.details()
    print(' login success\n\r')
    return(io)
  except tenable.errors.PermissionError as e:
    print()
    print(' Login to ' + endpoint_address + ' failed, please try again..' + "\n")
    raise ValueError

def tenable_login(endpoint_address, credentials=read_credentials_file()):
  if credentials:
    try:
      io = test_io_login(credentials.get('access_key'), credentials.get('secret_key'))
      return(io)
    except:
      print('\n\r Login failed with credentials stored in config file... \n\r')
      print('\n\r Please provide new credentials... \n\r')
      return tenable_login(endpoint_address, credentials=None)
  access_key = input('access_key for ' + endpoint_address + ' : ')
  #secret_key = getpass.getpass(prompt='secret_key for ' + endpoint_address + ' : ', stream=None)
  secret_key = input('secret_key for ' + endpoint_address + ' : ')
  try:
    io = test_io_login(access_key, secret_key)
    write_credentials_file(access_key, secret_key)
    return(io)
  except Exception as e:
    print(e)
    print()
    return tenable_login(endpoint_address)

def get_asset_lists(io):
  return io.asset_lists.list().get('usable')

def choose_an_asset_list(io):
  asset_lists = get_asset_lists(io)
  boundary_asset_lists = ''
  for asset_list in asset_lists:
    print(asset_list.get('id') + ' ' + asset_list.get('name'))

  boundary_id = '-999'
  while boundary_id not in [ (x.get('id')) for x in asset_lists ]:
    boundary_id = input("\n\r" + 'Please enter the id of the Asset list you want to validate' + "\n\r")
  for asset_list in asset_lists:
    if asset_list.get('id') == boundary_id:
      return asset_list

def get_asset_list_ips(io, asset_list_id):
  list_details = io.asset_lists.details(asset_list_id)
  return list_details.get('typeFields').get('definedIPs')

def get_scan_list(io):
  return json.loads(json.dumps(io.scans.list()))

def get_scan_analysis(io, scan_id):
  return io.analysis.scan(scan_id)

def get_scan_details(io, scan_id):
  return  io.scans.details(scan_id)

def find_ip_in_scan_results(ip):
  pass

