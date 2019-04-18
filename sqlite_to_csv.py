#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 13:29:37 2019

@author: seang
"""

from database import DataBase

db = DataBase(file_name="spotter.sqlite")
db.load_spatialite()
#db.table_to_csv(table_name='spwa_obis_ocean')
db.table_to_csv(table_name='spotter_pro_obis')
db.table_to_csv(table_name='whale_alert_obis')  
    
