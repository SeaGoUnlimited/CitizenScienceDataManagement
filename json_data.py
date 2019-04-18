#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 17:18:04 2018

@author: jasmine vazin, niklas griessbaum, sean goral, Molly Williams, Charlene Kormondy, Rae Fuhrman
"""

import json
import pandas
from shapely import geometry


class JsonData:
    
    def __init__(self, file_path=None, json_string=None, trip_id=None):
        self.trip_id = trip_id
        self.json = None
        if file_path is not None:
            self.from_file(file_path)
        elif json_string is not None:
            self.from_string(json_string)
            
    def from_file(self, file_name):
        with open(file_name) as f:
            self.json = json.load(f)
        self.trip_id_from_filename(file_name)        

    def from_string(self, json_string):
        self.json = json.loads(json_string)        
        
class WhaleAlertJson(JsonData):
    
    def __init__(self, file_path=None, json_string=None, trip_id=None):       
        super(WhaleAlertJson, self).__init__(file_path=file_path, json_string=json_string, trip_id=trip_id)
        self.sightings = pandas.DataFrame()        
        self.parse()       

    def parse(self):
        self.extract_sightings()

    def extract_sighting(self, sighting):
        sighting_dict = dict()
        sighting_dict['trip_id'] = self.trip_id
        string_keys = ['Whale Alert Species','Whale Alert Other Species','Comments','Whale Alert Submitter Name','Whale Alert Submitter Phone','Whale Alert Submitter Email','Animal Status', 'photos', 'species', 'url', 'create_date']
        float_keys = ['device_bearing', 'device_latitude', 'device_longitude', 'lat', 'lon']
        int_keys = ['number_sighted', 'Number Sighted', 'trip_id', 'number_sighted', 'id']
        for key in sighting:     
            if sighting[key] is None:
                sighting_dict[key] = None
            elif key in string_keys:
                sighting_dict[key] = str(sighting[key])
            elif key in float_keys:
                sighting_dict[key] = float(sighting[key])
            elif key in int_keys:                
                sighting_dict[key] = int(sighting[key])
        if 'lat' in sighting:
            sighting_dict['wkt'] = str(geometry.Point(sighting['lon'], sighting['lat']))
        return sighting_dict

    def extract_sightings(self):
        for sighting in self.json['sightings']:
            sighting = self.extract_sighting(sighting)
            self.sightings = self.sightings.append(sighting, ignore_index=True)
        if self.sightings.size > 0:
            self.sightings = self.sightings.groupby(by='create_date', as_index=False).first()
            self.sightings['trip_id'] = self.sightings['trip_id'].astype(int)
            

class SpotterJson(JsonData):
    
    def __init__(self, file_path=None, json_string=None, trip_id=None):        
        super(SpotterJson, self).__init__(file_path=file_path, json_string=json_string, trip_id=trip_id)
        self.trip = pandas.DataFrame()
        self.sightings = pandas.DataFrame()
        self.weather = pandas.DataFrame()
        self.behavior = pandas.DataFrame()
        self.parse()

    def parse(self):
        self.extract_trip()
        self.extract_sightings()
        self.extract_weather()
        
    def trip_id_from_filename(self, file_name):
        self.trip_id = int(file_name.split('trip_')[1].split('.json')[0])

    def set_trip_id(self, trip_id):
        self.trip_id = trip_id

    def extract_trip(self):
        trip = dict()
        trip['trip_id'] = self.trip_id
        trip_item_keys = ['end_date', 'create_date', 'Comments', 'CINMS Vessel', 'start_date', 'Other Vessel']
        for trip_item_key in trip_item_keys:
            trip[trip_item_key] = self.json.get(trip_item_key, None)
        if 'Observer Names' in self.json:
            trip['Observer Names'] = self.json['Observer Names'].replace('\n', '; ')
        if 'CINMS Weather' in self.json:
            trip['CINMS Weather'] = str(self.json['CINMS Weather'])
        if 'track' in self.json:
            trip['track'] = str(self.json['track'])
        trip['wkt'] = self.extract_track()
        self.trip = pandas.DataFrame(trip, index=['trip_id'])

    def extract_track(self):
        coordinates = []
        if "track" in self.json and \
                'gpx' in self.json['track'] and \
                self.json['track']['gpx']['trk']['trkseg'] is not None and \
                'trkpt' in self.json['track']['gpx']['trk']['trkseg'] and \
                type(self.json['track']['gpx']['trk']['trkseg']['trkpt']) is list:
            for trkpt in self.json['track']['gpx']['trk']['trkseg']['trkpt']:
                coordinate = (float(trkpt['@lon']), float(trkpt['@lat']))
                coordinates.append(coordinate)
            line = geometry.LineString(coordinates).wkt
        else:
            line = None
        return line
    
    def extract_cinms_behavior(self):
        pass

    def extract_cinms_photo_log(self):
        pass
    
    def extract_sighting(self, sighting):
        sighting_dict = dict()
        sighting_dict['trip_id'] = self.trip_id
        string_keys = ['CINMS Behavior', 'CINMS Photo Log', 'CINMS Species', 'Certainty',
                       'Distance Category', 'Comments', 'photos', 'species', 'url', 'Other Species', 'create_date']
        float_keys = ['device_bearing', 'device_latitude', 'device_longitude', 'lat', 'lon']
        int_keys = ['Total Sighted (Including Calves)', 'Calves Sighted', 'Number Sighted',
                    'Other Vessels On Scene', 'trip_id', 'number_sighted', 'id']
        for key in sighting:     
            if sighting[key] is None:
                sighting_dict[key] = None
            elif key in string_keys:
                sighting_dict[key] = str(sighting[key])
            elif key in float_keys:
                sighting_dict[key] = float(sighting[key])
            elif key in int_keys:                
                sighting_dict[key] = int(sighting[key])
        if 'lat' in sighting:
            sighting_dict['wkt'] = str(geometry.Point(sighting['lon'], sighting['lat']))
        if 'CINMS Behavior' in sighting:
            self.extract_cinms_behavior()
        if 'CINMS Photo Log' in sighting:
            self.extract_cinms_photo_log()
        return sighting_dict

    def extract_sightings(self):
        for sighting in self.json['sightings']:
            sighting = self.extract_sighting(sighting)
            self.sightings = self.sightings.append(sighting, ignore_index=True)
        if self.sightings.size > 0:
            self.sightings = self.sightings.groupby(by='create_date', as_index=False).first()
            self.sightings['trip_id'] = self.sightings['trip_id'].astype(int)

    def extract_weather(self):
        for weather in self.json['CINMS Weather']:
            weather['trip_id'] = self.trip_id
            self.weather = self.weather.append(weather, ignore_index=True)
        if self.weather.size > 0:
            self.weather['trip_id'] = self.weather['trip_id'].astype(int)
            

    
    


