#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
from skyfield.timelib import julian_date
from skyfield.sgp4lib import TEME_to_ITRF
import numpy
import csv
import platform

def main():
    lines = open('../sat23839.txt','r').read().splitlines()

    satellite = twoline2rv(lines[7], lines[8], wgs72)

    times = []
    report = csv.DictReader(open('atsb-report.csv', 'r'))
    for r in report:
	time = r['Time']
	hours = int(time[0:2])
	minutes = int(time[3:5])
	seconds = int(time[6:8])
	day = 7 if (hours > 12) else 8
        times.append([2014, 3, day, hours, minutes, seconds])

    w = csv.writer(open('sgp4-positions.csv', 'w'), lineterminator='\n')
    w.writerow(['x', 'y','z', 'dx','dy', 'dz'])

    for time in times:
	position, velocity = satellite.propagate(*time)

	jd = julian_date(*time)
	velocity = numpy.asarray(velocity) * 24.0 * 60.0 * 60.0
	p,v = TEME_to_ITRF(jd, position, velocity.tolist())
	v = v / (24.0 * 60.0 * 60.0)
	p = ["%0.1f" % i for i in p]
	v = ["%0.5f" % i for i in v]
	w.writerow([ p[0],p[1],p[2],v[0],v[1],v[2] ])

if __name__=='__main__':
    main()
