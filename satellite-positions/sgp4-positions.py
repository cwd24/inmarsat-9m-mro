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

    times = [
		[2014, 3, 7, 16, 00, 00],
		[2014, 3, 7, 16, 05, 00],
		[2014, 3, 7, 16, 10, 00],
		[2014, 3, 7, 16, 15, 00],
		[2014, 3, 7, 16, 20, 00],
		[2014, 3, 7, 16, 25, 00],
		[2014, 3, 7, 16, 30, 00],
		[2014, 3, 7, 16, 45, 00],
		[2014, 3, 7, 16, 55, 00],
		[2014, 3, 7, 17, 05, 00],
		[2014, 3, 7, 18, 25, 00],
		[2014, 3, 7, 19, 40, 00],
		[2014, 3, 7, 20, 40, 00],
		[2014, 3, 7, 21, 40, 00],
		[2014, 3, 7, 22, 40, 00],
		[2014, 3, 8, 00, 10, 00],
		[2014, 3, 8, 00, 20, 00]
        ]


    w = csv.writer(open('sgp4-positions.csv', 'w'), lineterminator='\n')
    w.writerow(['x', 'y','z', 'dx','dy', 'dz'])

    for time in times:
	position, velocity = satellite.propagate(*time)

	jd = julian_date(*time)
	velocity = numpy.asarray(velocity) * 24.0 * 60.0 * 60.0
	p,v = TEME_to_ITRF(jd, position, velocity.tolist())
	v = v / (24.0 * 60.0 * 60.0)
	w.writerow([ p[0],p[1],p[2],v[0],v[1],v[2] ])

if __name__=='__main__':
    main()
