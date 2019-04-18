#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 08:46:33 2018

@author: jasmine vazin, niklas griessbaum, sean goral, Molly Williams, Charlene Kormondy, Rae Fuhrman
"""

import requests
import configparser
from bs4 import BeautifulSoup
import re
import time

class WebsiteSession():

    def __init__(self):
        self.session = requests.Session()
        self.username = None
        self.password = None      
        self.config_name = None
        
    def read_credentials(self):
        config = configparser.ConfigParser(allow_no_value=False)
        config.optionxform = str
        config.read('credentials.config')
        self.username = config[self.config_name]['username']
        self.password = config[self.config_name]['password']
    
    def login(self):
        self.read_credentials()
        login_url = 'https://spotter.conserve.io/accounts/login/?next=/spotter/projects'
        self.session.get(url=login_url)
        self.session.headers.update({'referer': login_url})
        csrf_token = self.session.cookies['csrftoken']
        payload = {'username': self.username, 'password': self.password, 'csrfmiddlewaretoken': csrf_token}
        self.session.post(url='https://spotter.conserve.io/accounts/login/', data=payload)
    
    def download(self, url):
        download_succeded = False
        while not download_succeded:
            try:
                ret = self.session.get(url, timeout=60)
                download_succeded = True
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                print('Connection Error; logging out and in again')
                time.sleep(1)
                self.logout()
                self.login()
        if ret.status_code == 404:
            print('could not download {}'.format(url))
            return None
        else:
            return ret.text

    def logout(self):
        logout_url = 'https://spotter.conserve.io/accounts/logout'
        self.session.get(logout_url)

    def download_json(self, trip_id):
        url_trunk = 'https://spotter.conserve.io/spotter/trip/{trip_id}/data'
        url = url_trunk.format(trip_id=trip_id)
        json = self.download(url)
        return json
    
    def save_json(self, trip_id, folder):
        json_string = self.download_json(trip_id)
        json_file_name = '{folder}/trip_{trip_id}.json'.format(trip_id=trip_id, folder=folder)
        with open(json_file_name, 'w') as json_file:
            json_file.write(json_string)
            
    def get_trip_ids(self):
        trips_html = self.download_trips()
        soup = BeautifulSoup(trips_html, "lxml")
        tags = soup.find_all('a', href=re.compile("/spotter/trip/.*/data"))
        trip_ids = []
        for tag in tags:
            link = tag["href"]
            trip_id = int(link.split("/")[-2])
            trip_ids.append(trip_id)
        return trip_ids

    def download_trips(self):        
        ret = self.session.get(self.trip_url)
        return ret.text


class SpotterProSession(WebsiteSession):    
    
    def __init__(self):
        super(SpotterProSession, self).__init__()
        self.config_name = 'whale_spotter'
        self.trip_url = 'https://spotter.conserve.io/spotter/project/2/trips'
        

class WhaleAlertSession(WebsiteSession): 
    
    def __init__(self):
        super(WhaleAlertSession, self).__init__()
        self.config_name = 'whale_alert'
        self.trip_url = 'https://spotter.conserve.io/spotter/project/7/trips'


def test_getting_trip_ids():
    session = WhaleAlertSession()
    session.login()
    trip_ids = session.get_trip_ids()
    print(trip_ids)
    session.logout()


def test_getting_trip_json():
    session = WhaleAlertSession()
    session.login()
    trip_id = 1
    json = session.download_json(trip_id=trip_id)
    print(json)
    session.logout()


if __name__ == '__main__':
    test_getting_trip_ids()
    test_getting_trip_json()

