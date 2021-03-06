# -*- coding: utf-8 -*-
import googlemaps
import os, sys
import api_credentials
    
from continents import continents

def get_coordinates(location):
    gmaps = googlemaps.Client(key=api_credentials.api_key)
    
    geocode_res = gmaps.geocode(location)[0]
    
    return (geocode_res['geometry']['location']['lat'],
            geocode_res['geometry']['location']['lng'])

def get_continent(location):
    coordinates = get_coordinates(location)
    
    gmaps = googlemaps.Client(key=api_credentials.api_key)
    address = gmaps.reverse_geocode((coordinates[0], coordinates[1]))
    
    continent = "unknown"
    for component in address[0]['address_components']:
        if component['types'] == ['country', 'political']:
            continent = continents[component['short_name']]
    
    return continent

if __name__ == "__main__":
    print(get_continent("Kuala lumpur"))