#!/bin/sh
TOKEN=`wget -q -O- http://radarbox24.com/APIv1/guest_init | gunzip -cd | cut -d\" -f4`
curl -o - -X POST 'http://radarbox24.com/APIv1/flighthistory' \
-d "token=$TOKEN&fn=MAS370&s=1394210000&e=1394254380" | gunzip -cd > rb24-flighthistory.json
