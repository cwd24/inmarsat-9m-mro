#!/bin/bash
wget http://www.atsb.gov.au/media/5243942/ae-2014-054_mh370_searchareas.pdf
echo "Time,x,y,z,x',y',z'" > atsb-report.csv
pdftotext -layout ae-2014-054_mh370_searchareas.pdf - | grep 'Table 1: BTO Calibration' -A 9 | sed -r 's/.*(Time|\(UTC\)|16:)/\1/' | tail -n+5 | sed -r 's/\s\s*/,/g' | sed -r 's/,[^,]*,[^,]*$/,,,/' >> atsb-report.csv
#pdftotext -layout mr052_MH370_Definition_of_Sea_Floor_Wide_Area_Search.pdf - | grep 'Table 4: Satellite Location and Velocity (ECEF)' -A 14 | sed 's/\s\s*/,/g' | tail -n+5 | sed 's/^,//' >> atsb-report.csv
pdftotext -layout ae-2014-054_mh370_searchareas.pdf - | grep 'Table4:3:Satellite' -A 19 | sed 's/\s\s*/,/g' | tail -n+10 | sed 's/^,//' >> atsb-report.csv
