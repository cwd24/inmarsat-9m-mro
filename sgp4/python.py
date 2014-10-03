#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
from skyfield.timelib import julian_date
from skyfield.sgp4lib import TEME_to_ITRF
from math import radians
from scipy import mat, cos, sin, arctan, sqrt, pi, arctan2
import numpy
import csv
import platform
import datetime

def main():
    lines = open('../sat23839.txt','r').read().splitlines()

    satellite = twoline2rv(lines[7], lines[8], wgs72)

    times = []
    report = csv.DictReader(open('../inmarsat-su-log-redacted.csv', 'r'))
    for r in report:
        if r['Frequency Offset (Hz)'] != '':
            t = datetime.datetime.now().strptime(r['Time'],"%d/%m/%Y %H:%M:%S.%f")
            times.append(t)

    w = csv.writer(open('python.csv', 'w'), lineterminator='\n')
    w.writerow(['Time','x', 'y','z', 'dx','dy', 'dz'])

    for t in times:
        time = [t.year, t.month, t.day, t.hour, t.minute, t.second]
	position, velocity = satellite.propagate(*time)

	jd = julian_date(*time)
	velocity = numpy.asarray(velocity) * 24.0 * 60.0 * 60.0
	p,v = TEME_to_ITRF(jd, position, velocity.tolist())
	v = v / (24.0 * 60.0 * 60.0)
#	p = ["%0.1f" % i for i in p]
#	v = ["%0.5f" % i for i in v]
	w.writerow([ t,p[0],p[1],p[2],v[0],v[1],v[2] ])

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
    alt /= 0.3048 * 1000 # from ft to km
    speed *= 1.852 / (60 * 60) # from kn to Km/s
    roc *= 0.3048 / (60 * 1000) # from ft/min to Km/s
    xi = sqrt(1 - esq * sin(lat))
    x = (a / xi + alt) * cos(lat) * cos(lon)
    y = (a / xi + alt) * cos(lat) * sin(lon)
    z = (a / xi * (1 - esq) + alt) * sin(lat)
    dx, dy, dz = sin(heading) * speed, cos(heading) * speed, roc
    R = [[-sin(lon), -sin(lat) * cos(lon), cos(lat) * cos(lon)],[cos(lon), -sin(lat) * sin(lon), cos(lat) * sin(lon)],[0, cos(lat), sin(lat)]]
    return [x, y, z], numpy.dot(R,[dx, dy, dz])

if __name__=='__main__':
#    print enu2ecef(0,0,0,1,0,0)
#    print enu2ecef(0,0,0,0,1,0)
#    print enu2ecef(0,0,0,0,0,1)
    main()
