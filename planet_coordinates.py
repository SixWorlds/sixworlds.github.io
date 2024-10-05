# Author: Adam Kuziemski (https://github.com/AdamKuziemski)
# This script generates a JSON file based on data from
# https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=PS
# That JSON file will power the Exosky app to create menus and serve as a base for new star position calculations
import math

import csv
import json

with open('./assets/exoplanets.csv') as planets_file:
    planet_reader = csv.DictReader(
        filter(lambda row: row[0]!='#', planets_file), # skip comments in the header
        delimiter=',',
        quotechar='|'
    )
    planets = {}

    for planet in planet_reader:
        # skip planets with no distance, as they are useless for calculations
        if planet.get('sy_dist') == '':
            continue

        # read relevant planet information
        dist = float(planet.get('sy_dist'))
        dec = float(planet.get('dec'))
        ra = float(planet.get('ra'))

        # calculate positions relative to earth, assuming earth is (0, 0, 0)
        # not accounting for earth orbiting the sun
        x_earth = dist * math.cos(ra)
        y_earth = dist * math.sin(ra) * -1
        z_earth = dist * math.sin(dec)

        # add planet to "db"
        planets[planet.get('pl_name')] = {
            "dec": dec,
            "dist": dist,
            "ra": ra,
            "x_earth": x_earth,
            "y_earth": y_earth,
            "z_earth": z_earth
        }

    with open("assets/planets.json", "w") as outfile: 
        json.dump(planets, outfile)
