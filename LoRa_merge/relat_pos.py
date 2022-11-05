# -*- coding: utf-8 -*-
"""
@author: Min Lun Wu
"""
from numpy import pi, sqrt, cos, sin, tan, arcsin, arccos, arctan
import pandas as pd

#%%
def cac_dis_ang(lat_ref, lon_ref, alt_ref, lat, lon, alt):
    # Input: lat of observer, lon of observer, altitude(m) of observer
    #        lat of object,   lon of object,   altitude(m) of object

    ## Haversine formula
    ## Vincenty's formulae
    ## Great-circle navigation
    ## World Geodetic System

    R = 6378100 # Radius of Earth (km)

    # Convert degrees to radians
    lat1 = lat_ref * pi/180
    lon1 = lon_ref * pi/180 
    
    lat2 = lat.values * pi/180
    lon2 = lon.values * pi/180

    # Difference in latitude/longitude
    dLon = lon2 - lon1
    dLat = lat2 - lat1

    # Distance: haversine formula
    h = sin(dLat/2)*sin(dLat/2) + cos(lat1)*cos(lat2)*sin(dLon/2)* sin(dLon/2)
    h[h>1]=1
    dis = 2 * R * arcsin(sqrt(h))
    
    # Elevation angle
    lmd = arctan( (alt-alt_ref)/dis )

    # Convert radians to degrees
    lamba = lmd * (180/pi)

    return pd.Series(dis/1000.), pd.Series(lamba) # Distance(km), Azimuth(deg), Elevation angle(deg)