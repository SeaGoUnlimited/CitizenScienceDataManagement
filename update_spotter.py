#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 16:00:38 2018

@author: jasmine vazin, niklas griessbaum, sean goral, Molly Williams, Charlene Kormondy, Rae Fuhrman
"""

import glob
from website import SpotterProSession
from database import DataBase
from json_data import SpotterJson


file_name = 'spotter.sqlite'
database = DataBase(file_name=file_name)
database.load_spatialite()

session = SpotterProSession()
session.login()


def get_trip_ids_website():
    trips = session.get_trip_ids()
    return trips

def get_trip_ids_database():
    trips_database = database.trip_ids()
    return trips_database

def load_trip(trip_id):
    json_string = session.download_json(trip_id=trip_id)
    trip_json = SpotterJson(json_string=json_string, trip_id=trip_id)
    database.insert_json(trip_json)

def load_trips(trip_ids):
    for trip_id in trip_ids:
        print(trip_id)
        load_trip(trip_id)

def load_missing():
    trip_ids_website = get_trip_ids_website()
    trip_ids_database = get_trip_ids_database()
    trip_ids_missing = sorted(list(set(trip_ids_website) - set(trip_ids_database)))
    load_trips(trip_ids=trip_ids_missing)


def load_folder(folder_path):
    file_paths = glob.glob(folder_path + '*.json')
    for file_path in file_paths:
        load_json(file_path)


def load_json(file_path):
    trip_json = SpotterJson(file_path=file_path)
    database.insert_json(trip_json)


def load_all():
    trip_ids_website = get_trip_ids_website()
    load_trips(trip_ids=trip_ids_website)
    database.add_geomertries()


if __name__ == '__main__':
    #load_trip(101)
    #load_json('json_files_test/trip_102.json')
    #load_all()    
    #load_folder('json_files/')
    load_missing()
    database.add_geomertries()
    database.remove_duplicates()
    database.vacuum()
    
