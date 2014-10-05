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
    times = []
    w = csv.writer(open('cpp.csv', 'w'), lineterminator='\n')
    w.writerow(['Time','x', 'y','z', 'dx','dy', 'dz'])
    cpp = csv.DictReader(open('cpp-teme.csv', 'r'))
    for r in cpp:
        t = datetime.datetime.now().strptime(r['time'],"%Y-%m-%dT%H:%M:%S")
	jd = julian_date(t.year, t.month, t.day, t.hour, t.minute, t.second)
        position = [float(r['x']),float(r['y']),float(r['z'])]
        velocity = [float(r['dx']),float(r['dy']),float(r['dz'])]
	velocity = numpy.asarray(velocity) * 24.0 * 60.0 * 60.0
	p,v = TEME_to_ITRF(jd, position, velocity.tolist())
	v = v / (24.0 * 60.0 * 60.0)
#	p = ["%0.1f" % i for i in p]
#	v = ["%0.5f" % i for i in v]
	w.writerow([ t,p[0],p[1],p[2],v[0],v[1],v[2] ])

if __name__=='__main__':
    main()
