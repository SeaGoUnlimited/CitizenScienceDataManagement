#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 17:18:19 2018

@author: jasmine vazin, niklas griessbaum, sean goral, Molly Williams, Charlene Kormondy, Rae Fuhrman
"""
import sqlite3
import platform
import os
import pandas as pd

class DataBase:
    
    def __init__(self, file_name):
        self.file_name = file_name
        self.connection = None
        self.cursor = None
        self.connect()
        self.load_spatialite()
        if self.is_empty():
            self.init_spatial_metadata()
            self.create_tables()
            self.add_geometry_columns()

    def wipe_trips(self):
        query = 'DELETE FROM trips;'
        self.cursor.execute(query)
        self.connection.commit()

    def wipe_weather(self):
        query = 'DELETE FROM weather;'
        self.cursor.execute(query)
        self.connection.commit()

    def wipe_sightings(self):
        query = 'DELETE FROM sightings;'
        self.cursor.execute(query)
        self.connection.commit()
        
    def wipe_whalealert_sightings(self):
        query = 'DELETE FROM whale_alert;'
        self.cursor.execute(query)
        self.connection.commit()
        
    def wipe_whalealert_obis(self):
        query = 'DELETE FROM whale_alert_obis;'
        self.cursor.execute(query)
        self.connection.commit()
        
    def wipe_spotter_pro_obis(self):
        query = 'DELETE FROM spotter_pro_obis;'
        self.cursor.execute(query)
        self.connection.commit()

    def wipe(self):
        self.wipe_trips()
        self.wipe_weather()
        self.wipe_sightings()
        self.wipe_whalealert_sightings()
        self.wipe_whalealert_obis()
        self.wipe_spotter_pro_obis()

    def exists(self):
        return os.path.isfile(self.file_name)

    def is_empty(self):
        query = 'SELECT name FROM sqlite_master WHERE type="table";'
        self.cursor.execute(query)
        if self.cursor.fetchone() is None:
            return True
        else:
            return False

    def connect(self):
        self.connection = sqlite3.connect(self.file_name)
        self.connection.enable_load_extension(True)
        self.cursor = self.connection.cursor()

    def create_tables(self):
        self.create_sightings_table()
        self.create_trips_table()
        self.create_weather_table()
        self.create_whalealert_table()
        self.create_whalealert_obis()
        self.create_spotter_pro_obis()

    def table_exists(self, table):
        query = 'SELECT name FROM sqlite_master WHERE type="table" AND name="{table}";'
        query = query.format(table=table)
        self.cursor.execute(query)
        if self.cursor.fetchone() is None:
            return False
        else:
            return True

    def create_sightings_table(self):
        with open('queries/create_sightings.sql') as query_file:
            query = query_file.read()
        self.connection.execute(query)

    def create_trips_table(self):
        with open('queries/create_trips.sql') as query_file:
            query = query_file.read()
        self.connection.execute(query)

    def create_weather_table(self):
        with open('queries/create_weather.sql') as query_file:
            query = query_file.read()
        self.connection.execute(query)
        
    def create_whalealert_table(self):
        with open('queries/create_whale_alert.sql') as query_file:
            query = query_file.read()
        self.connection.execute(query)

    def create_whalealert_obis(self):
        with open('queries/whale_alert_obis_view.sql') as query_file:
            query = query_file.read()
        self.connection.execute(query)
        
    def create_spotter_pro_obis(self):
        with open('queries/spotter_pro_obis_view.sql') as query_file:
            query = query_file.read()
        self.connection.execute(query)
        
    def load_spatialite(self):
        if platform.system() == 'Linux':
            self.connection.execute('SELECT load_extension("mod_spatialite.so")')
        elif platform.system() =='Darwin':
            self.connection.execute('SELECT load_extension("mod_spatialite.dylib")')

    def init_spatial_metadata(self):
        self.connection.execute('SELECT InitSpatialMetaData(1);') 

    def insert_dict(self, dictionary, table):
        columns = '"' + '", "' .join(dictionary.keys()) + '"'
        placeholders = ', '.join('?' * len(dictionary))
        query = 'INSERT INTO {table} ({columns}) VALUES ({placeholders});'
        query = query.format(table=table, columns=columns, placeholders=placeholders)
        values = tuple(dictionary.values())
        self.cursor.execute(query, values)
        self.connection.commit()
        
    def insert_trip(self, trip):
        trip.to_sql(name='trips', con=self.connection, if_exists='append', index=False)

    def insert_sightings(self, sightings):
        sightings.to_sql(name='sightings', con=self.connection, if_exists='append', index=False)

    def insert_weather(self, weather):
        weather.to_sql(name='weather', con=self.connection, if_exists='append', index=False)

    def insert_behavior(self, behavior):
        #behavior.to_sql(name='behavior', con=self.connection, if_exists='append', index=False)
        pass
    
    def insert_whalealert(self, whalealert):
        whalealert.to_sql(name='whale_alert', con=self.connection, if_exists='append', index=False)
        
    def insert_scientific_names(self, insert_scientific_names):
        scientific_names.to_sql(name='scientific_names', con=self.connection, if_exists='replace')
    
    def insert_json(self, trip_json):
        self.insert_trip(trip_json.trip)
        self.insert_sightings(trip_json.sightings)
        self.insert_weather(trip_json.weather)
        self.insert_behavior(trip_json.behavior)
        self.connection.commit()
    
    def insert_whalealert_json(self, whalealert_json):
        self.insert_whalealert(whalealert_json.sightings)        
    
    def newest_whalealert_trip_id(self):
        query = 'SELECT trip_id FROM whale_alert ORDER BY trip_id DESC LIMIT 1;'
        self.cursor.execute(query)
        latest_trip_id_whalealert = self.cursor.fetchone()[0]
        return latest_trip_id_whalealert
    
    def whalealert_trip_ids(self):
        query = 'SELECT trip_id FROM whale_alert ORDER BY trip_id;'
        self.cursor.execute(query)
        whalealert_trip_ids_list = []
        for trip_id in self.cursor.fetchall():
            whalealert_trip_ids_list.append(trip_id[0])
        return whalealert_trip_ids_list
    
    def newest_trip_id(self):
        query = 'SELECT trip_id FROM trips ORDER BY trip_id DESC LIMIT 1;'
        self.cursor.execute(query)
        latest_trip_id = self.cursor.fetchone()[0]
        return latest_trip_id

    def trip_ids(self):
        query = 'SELECT trip_id FROM trips ORDER BY trip_id;'
        self.cursor.execute(query)
        trip_ids_list = []
        for trip_id in self.cursor.fetchall():
            trip_ids_list.append(trip_id[0])
        return trip_ids_list

    def add_geometry_columns(self):
        self.connection.execute("SELECT AddGeometryColumn('trips', 'geom', 4326, 'LINESTRING', 2);")
        self.connection.execute("SELECT AddGeometryColumn('sightings', 'geom', 4326, 'POINT', 2);")
        self.connection.execute("SELECT AddGeometryColumn('whale_alert', 'geom', 4326, 'POINT', 2);")

    def add_geomertries(self):
        self.connection.execute("UPDATE trips SET geom=GeomFromText(wkt, 4326);")
        self.connection.execute("UPDATE sightings SET geom=GeomFromText(wkt, 4326);")
        self.connection.execute("UPDATE whale_alert SET geom=GeomFromText(wkt, 4326);")
        self.connection.commit()

    def remove_duplicates(self):
        self.remove_duplicates_sightings()
        self.remove_duplicates_trips()
        self.remove_duplicates_weather()
        self.remove_duplicates_whalealert()
        
    def remove_duplicates_weather(self):
        query = 'DELETE FROM weather WHERE row_id NOT IN(SELECT min(row_id) FROM weather GROUP BY create_date,trip_id);'
        self.cursor.execute(query)

    def remove_duplicates_sightings(self):
        query = 'DELETE FROM sightings WHERE row_id NOT IN (SELECT min(row_id) FROM sightings GROUP BY id);'
        self.cursor.execute(query)

    def remove_duplicates_trips(self):
        query = 'DELETE FROM trips WHERE row_id NOT IN (SELECT min(row_id)FROM trips GROUP BY trip_id);'
        self.cursor.execute(query)
    
    def remove_duplicates_whalealert(self):
        query = 'DELETE FROM whale_alert WHERE row_id NOT IN (SELECT min(row_id) FROM whale_alert GROUP BY id);'
        self.cursor.execute(query)
        
    def vacuum(self):
        self.connection.isolation_level = None
        query = 'VACUUM;'
        self.cursor.execute(query)
        self.connection.isolation_level = ''
    
    def table_to_csv(self, table_name):
        csv_filename = table_name + ".csv"
        query = "SELECT * FROM {table_name};".format(table_name=table_name)
        df = pd.read_sql_query(query, self.connection)
        df.to_csv(csv_filename, encoding='utf-8', sep=',', index=False)


if __name__ == '__main__':
    database = DataBase('spotter.sqlite')
