# Author: Adam Kuziemski (https://github.com/AdamKuziemski)
# This script generates a JSON file based on existing files:
# * assets/planets.json
# * assets/stars.json
# That JSON file will then be used to calculate star positions relative to exoplanets
# And to generate skybox files with star positions from each of the exoplanets' perspective.
import json
import cv2
import os

import math
import numpy as np

with open('assets/planets.json', 'r') as planets_file:
    planets = json.load(planets_file)

with open('assets/stars.json', 'r') as stars_file:
    stars = json.load(stars_file)

skyboxes = {}
SKYBOX_WIDTH = 1080

# define X axis boundaries for each side of the sky cube placement
FRONT_LO_RA_THRESHOLD_A = 315
FRONT_HI_RA_THRESHOLD_A = 360
FRONT_LO_RA_THRESHOLD_B = 0
FRONT_HI_RA_THRESHOLD_B = 45
RIGHT_LO_RA_THRESHOLD = 45
RIGHT_HI_RA_THRESHOLD = 135
BACK_LO_RA_THRESHOLD = 135
BACK_HI_RA_THRESHOLD = 225
LEFT_LO_RA_THRESHOLD = 225
LEFT_HI_RA_THRESHOLD = 315
UP_LO_RA_THRESHOLD = 0
UP_HI_RA_THRESHOLD = 360
DOWN_LO_RA_THRESHOLD = 0
DOWN_HI_RA_THRESHOLD = 360

# define Y axis boundaries for the sky cube placement
FRONT_LO_DEC_THRESHOLD = -45
FRONT_HI_DEC_THRESHOLD = 45
RIGHT_LO_DEC_THRESHOLD = -45
RIGHT_HI_DEC_THRESHOLD = 45
BACK_LO_DEC_THRESHOLD = -45
BACK_HI_DEC_THRESHOLD = 45
LEFT_LO_DEC_THRESHOLD = -45
LEFT_HI_DEC_THRESHOLD = 45
UP_LO_DEC_THRESHOLD = 45
UP_HI_DEC_THRESHOLD = 90
DOWN_HI_DEC_THRESHOLD = -90
DOWN_LO_DEC_THRESHOLD = -45

def save_image(folder_name, file_name, image):
    folder_path = 'assets/{}'.format(folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    cv2.imwrite("{}/{}.png".format(folder_path, file_name), image)

for (name, planet) in planets.items():
    skyboxes[name] = []

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
        dec = math.asin(z_diff / vector_length) * 180 / math.pi

        x = 0
        y = 0
        face = -1

        # check where the star lies on the exoplanet sky and assign it to the correct side of the cube
        if ((ra > FRONT_LO_RA_THRESHOLD_A and ra <= FRONT_HI_RA_THRESHOLD_A) or (ra >= FRONT_LO_RA_THRESHOLD_B and ra < FRONT_HI_RA_THRESHOLD_B)) and dec >= FRONT_LO_DEC_THRESHOLD and dec < FRONT_HI_DEC_THRESHOLD:
            x = ra + 45
            y = dec + 45
            face = 1
        elif ra >= RIGHT_LO_RA_THRESHOLD and ra < RIGHT_HI_RA_THRESHOLD and dec >= RIGHT_LO_DEC_THRESHOLD and dec < RIGHT_HI_DEC_THRESHOLD:
            x = ra - 45
            y = dec + 45
            face = 2
        elif ra >= BACK_LO_RA_THRESHOLD and ra < BACK_HI_RA_THRESHOLD and dec >= BACK_LO_DEC_THRESHOLD and dec < BACK_HI_DEC_THRESHOLD:
            x = ra - 135
            y = dec + 45
            face = 3
        elif ra >= LEFT_LO_RA_THRESHOLD and ra < LEFT_HI_RA_THRESHOLD and dec >= LEFT_LO_DEC_THRESHOLD and dec < LEFT_HI_DEC_THRESHOLD:
            x = ra - 225
            y = dec + 45
            face = 4
        elif ra >= UP_LO_RA_THRESHOLD and ra < UP_HI_RA_THRESHOLD and dec >= UP_LO_DEC_THRESHOLD and dec < UP_HI_DEC_THRESHOLD:
            # x = (90 - dec) * math.cos(ra)
            # y = (90 - dec) * math.sin(ra)
            face = 5
        elif ra >= DOWN_LO_RA_THRESHOLD and ra < DOWN_HI_RA_THRESHOLD and dec >= DOWN_HI_DEC_THRESHOLD and dec < DOWN_LO_DEC_THRESHOLD:
            # x = (90 - dec) * math.cos(-ra)
            # y = (90 - dec) * math.sin(-ra)
            face = 6

        skyboxes[name].append({
            "ra": ra,
            "dec": dec,
            "L": vector_length,
            "face": face,
            "x": x % 360,
            "y": y
        })

with open("assets/skyboxes.json", "w") as outfile: 
    json.dump(skyboxes, outfile)

for (box, stars) in skyboxes.items():
    # create empty skybox images
    front_face = np.zeros((SKYBOX_WIDTH, SKYBOX_WIDTH, 3), dtype = np.uint8)
    right_face = np.zeros((SKYBOX_WIDTH, SKYBOX_WIDTH, 3), dtype = np.uint8)
    back_face = np.zeros((SKYBOX_WIDTH, SKYBOX_WIDTH, 3), dtype = np.uint8)
    left_face = np.zeros((SKYBOX_WIDTH, SKYBOX_WIDTH, 3), dtype = np.uint8)
    up_face = np.zeros((SKYBOX_WIDTH, SKYBOX_WIDTH, 3), dtype = np.uint8)
    down_face = np.zeros((SKYBOX_WIDTH, SKYBOX_WIDTH, 3), dtype = np.uint8)

    for star in stars:
        x_deg = (star.get('x') / 90)
        y_deg = (star.get('y') / 90)
        x = math.floor(x_deg * SKYBOX_WIDTH)
        y = math.floor(y_deg * SKYBOX_WIDTH)

        # put star on the correct side of the cube
        if star.get('face') == 1:
            front_face[x, y, 0] = 255
            front_face[x, y, 1] = 255
            front_face[x, y, 2] = 255
        elif star.get('face') == 2:
            right_face[x, y, 0] = 255
            right_face[x, y, 1] = 255
            right_face[x, y, 2] = 255
        elif star.get('face') == 3:
            back_face[x, y, 0] = 255
            back_face[x, y, 1] = 255
            back_face[x, y, 2] = 255
        elif star.get('face') == 4:
            left_face[x, y, 0] = 255
            left_face[x, y, 1] = 255
            left_face[x, y, 2] = 255
        elif star.get('face') == 5:
            up_face[x, y, 0] = 255
            up_face[x, y, 1] = 255
            up_face[x, y, 2] = 255
        elif star.get('face') == 6:
            down_face[x, y, 0] = 255
            down_face[x, y, 1] = 255
            down_face[x, y, 2] = 255

    # save skyboxes
    save_image(box, 'skybox_ft', front_face)
    save_image(box, 'skybox_rt', right_face)
    save_image(box, 'skybox_bk', back_face)
    save_image(box, 'skybox_lf', left_face)
    save_image(box, 'skybox_up', up_face)
    save_image(box, 'skybox_dn', down_face)
