#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pandas 
from database import Database


def read_scientific_names(filename='whalealert.csv'):
    scientific_names = pandas.read_csv(filename)    
    return scientific_names

def upsert_scientific_names(scientific_names):        
    db = database.DataBase("spotter.sqlite")
    db.insert_scientific_names(scientific_names)
    
    
if __name__ == '__main__':
    scientific_names = read_scientific_names()
    upsert_scientific_names(scientific_names
