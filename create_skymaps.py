# Author: Adam Kuziemski (https://github.com/AdamKuziemski)
# This script generates a JSON file based on existing files:
# * assets/planets.json
# * assets/stars.json
# That JSON file will then be used to calculate star positions relative to exoplanets
# And to generate sky maps with star positions from each of the exoplanets' perspective.
import json
import cv2
import os

import math
import numpy as np

with open('assets/planets.json', 'r') as planets_file:
    planets = json.load(planets_file)

with open('assets/stars.json', 'r') as stars_file:
    stars = json.load(stars_file)

skymaps = {}
magnitudes = {}

MAP_WIDTH = 1080

def save_image(folder_name, file_name, image):
    folder_path = 'assets/{}'.format(folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    cv2.imwrite("{}/{}.png".format(folder_path, file_name), image)

for (name, planet) in planets.items():
    skymaps[name] = []
    magnitudes[name] = {
        "max": 0, # faintest
        "min": 999 # brightest
    }

    for star in stars:
        # get distance between star and exoplanet using their cartesian positions
        vector_length = math.sqrt(((star.get('x_earth') - planet.get('x_earth')) ** 2) + ((star.get('y_earth') - planet.get('y_earth')) ** 2) + ((star.get('z_earth') - planet.get('z_earth')) ** 2))

        # don't use objects that are too close together (or on top of one another, basically)
        if vector_length == 0:
            continue

        x_diff = star.get('x_earth') - planet.get('x_earth')
        y_diff = star.get('y_earth') - planet.get('y_earth')
        z_diff = star.get('z_earth') - planet.get('z_earth')

        # get new ascension for the star from exoplanet perspective
        ra = math.acos(x_diff) / vector_length * 180 / math.pi
        if y_diff < 0:
            ra = 360 - ra

        # get new declination for the star from exoplanet perspective
        dec = math.asin(z_diff) / vector_length * 180 / math.pi

        hemisphere = 'south' if dec < 0 else 'north'
        x = 0
        y = 0

        # calculate the star's position on the hemisphere's sky map
        if hemisphere == 'north':
            x = (90 - dec) * math.cos(ra)
            y = (90 - dec) * math.sin(ra)
        else:
            x = (90 + dec) * math.cos(-ra)
            y = (90 + dec) * math.sin(-ra)

        # find min and max star magnitude for each planet 
        mag_v = star.get('mag') - 5 * (1 / math.log10(vector_length))
        if magnitudes[name].get('max') < mag_v:
            magnitudes[name]['max'] = mag_v
        if magnitudes[name].get('min') > mag_v:
            magnitudes[name]['min'] = mag_v

        skymaps[name].append({
            "ra": ra,
            "dec": dec,
            "L": vector_length,
            "hemisphere": hemisphere,
            "mag": mag_v,
            "x": x,
            "y": y
        })

with open("assets/maps.json", "w") as outfile: 
    json.dump(skymaps, outfile)

for (box, stars) in skymaps.items():
    # create empty sky map images
    north_map = np.zeros((MAP_WIDTH, MAP_WIDTH, 3), dtype = np.uint8)
    south_map = np.zeros((MAP_WIDTH, MAP_WIDTH, 3), dtype = np.uint8)

    # find magnitude difference for each planet
    min_mag = magnitudes[box].get('min')
    max_mag = magnitudes[box].get('max')
    magnitude_difference = max_mag - min_mag

    for star in stars:
        # calculate star position on the map
        x = math.floor((star.get('x') * 6) + MAP_WIDTH / 2)
        y = math.floor((star.get('y') * 6) + MAP_WIDTH / 2)

        # get star magnitude and cap it between (0.6, 1) inclusive
        mag_v = star.get('mag') - 5 * (1 / math.log10(star.get('L')))
        relative_mag = math.fabs((mag_v - max_mag) / magnitude_difference)
        if relative_mag > 0.9:
            relative_mag = 1
        if relative_mag < 0.5:
            relative_mag = 0.6

        # translate star magnitude into white saturation
        star_color = math.floor(255 * relative_mag)

        # put the star on the map
        if star.get('hemisphere') == 'north':
            north_map[x, y, 0] = star_color
            north_map[x, y, 1] = star_color
            north_map[x, y, 2] = star_color
            # px left
            if x >= 1:
                north_map[x - 1, y, 0] = star_color
                north_map[x - 1, y, 1] = star_color
                north_map[x - 1, y, 2] = star_color
            # px right
            if x <= MAP_WIDTH - 2:
                north_map[x + 1, y, 0] = star_color
                north_map[x + 1, y, 1] = star_color
                north_map[x + 1, y, 2] = star_color
            # px top
            if y >= 1:
                north_map[x, y - 1, 0] = star_color
                north_map[x, y - 1, 1] = star_color
                north_map[x, y - 1, 2] = star_color
            # px bottom
            if y <= MAP_WIDTH - 2:
                north_map[x, y + 1, 0] = star_color
                north_map[x, y + 1, 1] = star_color
                north_map[x, y + 1, 2] = star_color
            
        else:
            south_map[x, y, 0] = star_color
            south_map[x, y, 1] = star_color
            south_map[x, y, 2] = star_color
             # px left
            if x >= 1:
                south_map[x - 1, y, 0] = star_color
                south_map[x - 1, y, 1] = star_color
                south_map[x - 1, y, 2] = star_color
            # px right
            if x <= MAP_WIDTH - 2:
                south_map[x + 1, y, 0] = star_color
                south_map[x + 1, y, 1] = star_color
                south_map[x + 1, y, 2] = star_color
            # px top
            if y >= 1:
                south_map[x, y - 1, 0] = star_color
                south_map[x, y - 1, 1] = star_color
                south_map[x, y - 1, 2] = star_color
            # px bottom
            if y <= MAP_WIDTH - 2:
                south_map[x, y + 1, 0] = star_color
                south_map[x, y + 1, 1] = star_color
                south_map[x, y + 1, 2] = star_color

    # save sky maps
    save_image(box, 'skymap_n', north_map)
    save_image(box, 'skymap_s', south_map)
