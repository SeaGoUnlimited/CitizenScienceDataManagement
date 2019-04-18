#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 22 18:38:33 2018

@author: jasmine vazin, niklas griessbaum, sean goral, Molly Williams, Charlene Kormondy, Rae Fuhrman
"""

import glob
from website import WhaleAlertSession
from database import DataBase
from json_data import WhaleAlertJson


file_name = 'spotter.sqlite'
database = DataBase(file_name=file_name)
database.load_spatialite()

session = WhaleAlertSession()
session.login()

def get_trip_ids_website_whalealert():
    whalealert_trips = session.get_trip_ids()
    return whalealert_trips

def get_trip_ids_database():
    trips_database = database.whalealert_trip_ids()
    return trips_database

def load_whalealert_trip(trip_id):
    json_string = session.download_json(trip_id=trip_id)
    whalealert_json = WhaleAlertJson(json_string=json_string, trip_id=trip_id)
    database.insert_whalealert_json(whalealert_json)
    
def load_trips(trip_ids):
    for trip_id in trip_ids:
        print(trip_id)
        load_whalealert_trip(trip_id)
        
def load_missing():
    trip_ids_website_whalealert = get_trip_ids_website_whalealert()
    trip_ids_database = get_trip_ids_database()
    trip_ids_missing = sorted(list(set(trip_ids_website_whalealert) - set(trip_ids_database)))
    load_trips(trip_ids=trip_ids_missing)


def load_folder(folder_path):
    file_paths = glob.glob(folder_path + '*.json')
    for file_path in file_paths:
        load_json(file_path)


def load_json(file_path):
    whalealert_json = WhaleAlertJson(file_path=file_path)
    database.insert_json(whalealert_json)


def load_all():
    trip_ids_website_whalealert = get_trip_ids_website_whalealert()
    load_trips(trip_ids=trip_ids_website_whalealert)
    database.add_geomertries()


if __name__ == '__main__':
    #load_all()    
    load_missing()
    database.add_geomertries()
    database.remove_duplicates()
    database.vacuum()
    



