#!/bin/bash
# Example script used to parse through all the shuttles for Monolith.

FILE_INPUT=`find ~/Documents/Coding/Monolith.SarahRaven/Resources/Maps/_Mono/Shuttles -type f`

for i in $FILE_INPUT
do
    ~/Documents/Coding/map-yaml-to-image/main.py -i "$i" -o output/$(basename $i .yml).png
done

