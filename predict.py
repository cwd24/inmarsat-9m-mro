#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
from skyfield.timelib import julian_date
from skyfield.sgp4lib import TEME_to_ITRF
from math import radians, sqrt, sin, cos
import numpy
import csv
import platform
import datetime

def main():
    pushback = datetime.datetime(2014, 3, 7, 16, 27, 40)

    times = dict()
    report = csv.DictReader(open('inmarsat-su-log-redacted.csv', 'r'))
    for r in report:
        if r['Frequency Offset (Hz)'] != '':
            t = datetime.datetime.now().strptime(r['Time'],"%d/%m/%Y %H:%M:%S.%f")
            if t < pushback:
                records = [t,int(r['Burst Timing Offset (microseconds)']),int(r['Frequency Offset (Hz)'])]
                if r['Channel Type'] == 'T-Channel RX':
                    records[1] += 5000
                key = r['Channel Name']
                key += r['Channel Unit ID']
		if key in times.keys():
           	     times[key].append(records)
                else:
                     times[key] = [records]
    for i in times.keys():
            print 'CHANNEL: ', i
	    calibrate(times[i])

#    w = csv.writer(open('sgp4-positions.csv', 'w'), lineterminator='\n')
#    w.writerow(['Time','x', 'y','z', 'dx','dy', 'dz'])
lines = open('sat23839.txt','r').read().splitlines()
satellite = twoline2rv(lines[7], lines[8], wgs72)

def calibrate(records):
    c1_p,c1_v = adsb2ecef(2.74668, 101.71266, 0.021, 0, 0, 0)
    # http://web.acma.gov.au/pls/radcom/site_search.site_lookup?pSITE_ID=139331
    perth_p,perth_v = adsb2ecef(-31.804545,115.887337,0.056, 0, 0, 0)
    # http://web.acma.gov.au/pls/radcom/site_search.site_lookup?pSITE_ID=139331
    c = 299792.458
    a = []
    for r in records:
        t = r[0]
        time = [t.year, t.month, t.day, t.hour, t.minute, t.second]
	position, velocity = satellite.propagate(*time)

	jd = julian_date(*time)
	velocity = numpy.asarray(velocity) * 24.0 * 60.0 * 60.0
	p,v = TEME_to_ITRF(jd, position, velocity.tolist())
	v = v / (24.0 * 60.0 * 60.0)

        radius_a = p - c1_p
        radius_a = numpy.sqrt(radius_a.dot(radius_a))
        radius_p = p - perth_p
        radius_p = numpy.sqrt(radius_p.dot(radius_p))
        bias = int(r[1]) - (2000000 * (radius_a + radius_p) / c )
        a.append(bias)
    print 'Number of records:', len(a)
    print 'min:', numpy.amin(a)
    print 'max:', numpy.amax(a)
    print 'mean:', numpy.mean(a)
    print 'std:', numpy.std(a)
#        print radius_a, radius_p, r[1]

#	w.writerow([ t,p[0],p[1],p[2],v[0],v[1],v[2] ])

# https://code.google.com/p/pysatel/source/browse/trunk/pysatel/coord.py
# http://www.navipedia.net/index.php/Transformations_between_ECEF_and_ENU_coordinates
# Constants defined by the World Geodetic System 1984 (WGS84)
a = 6378.137
b = 6356.7523142
esq = 6.69437999014 * 0.001
e1sq = 6.73949674228 * 0.001
f = 1 / 298.257223563
def adsb2ecef(lat, lon, alt, heading, speed, roc):
    lat, lon, heading = radians(lat), radians(lon), radians(heading)
    alt *= 0.3048 / 1000 # from ft to km
    speed *= 1.852 / (60 * 60) # from kn to Km/s
    roc *= 0.3048 / (60 * 1000) # from ft/min to Km/s
    p = lla2ecef(lat, lon, alt)
    dx, dy, dz = sin(heading) * speed, cos(heading) * speed, roc
    R = [[-sin(lon), -sin(lat) * cos(lon), cos(lat) * cos(lon)],[cos(lon), -sin(lat) * sin(lon), cos(lat) * sin(lon)],[0, cos(lat), sin(lat)]]
    return p, numpy.dot(R,[dx, dy, dz])

# radians, radians, km
def lla2ecef(lat, lon, alt):
    xi = sqrt(1 - esq * sin(lat))
    x = (a / xi + alt) * cos(lat) * cos(lon)
    y = (a / xi + alt) * cos(lat) * sin(lon)
    z = (a / xi * (1 - esq) + alt) * sin(lat)
    return [x, y, z]

if __name__=='__main__':
    main()
