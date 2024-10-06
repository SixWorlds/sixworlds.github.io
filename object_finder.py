import astropy.units as u
from astropy.coordinates import SkyCoord
from astroquery.gaia import Gaia

import json
import math

coord = SkyCoord(ra="06h33m49.17s", dec="-58d31m30.11s", unit="rad")
width = u.Quantity(0.1, u.deg)
height = u.Quantity(0.1, u.deg)

job = Gaia.launch_job_async("SELECT TOP 10000 distance_gspphot,phot_g_mean_mag,ra,dec,ecl_lat,ecl_lon "
    "FROM gaiadr3.gaia_source "
    "WHERE (phot_g_mean_mag IS NOT NULL AND distance_gspphot IS NOT NULL AND ra IS NOT NULL AND dec IS NOT NULL) "
    "ORDER BY phot_g_mean_mag ASC")

r = job.get_results()
stars = []
# tables = Gaia.load_tables()

# for table in tables:
#   print(table.get_qualified_name())

for row in r:
    # ra = float(row.get('ra'))
    # dec = float(row.get('dec'))
    # lat = row.get('ecl_lat')
    # lon = row.get('ecl_lon')
    # mag = row.get('phot_g_mean_mag'),
    # dist = float(row.get('dist'))
    # parallax = float(row.get('parallax'))
    # print("{}, {}, {}".format(r, g,b))
    # read relevant planet information

    if row.get('distance_gspphot') == '--':
        continue

    dist = float(row.get('distance_gspphot'))
    dec = float(row.get('dec'))
    ra = float(row.get('ra'))
    mag = float(row.get('phot_g_mean_mag'))

    # calculate positions relative to earth, assuming earth is (0, 0, 0)
    # not accounting for earth orbiting the sun
    x_earth = dist * math.cos(ra)
    y_earth = dist * math.sin(ra) * -1
    z_earth = dist * math.sin(dec)

    # add row to "db"
    stars.append({
        "dec": dec,
        "dist": dist,
        "ra": ra,
        "mag": mag,
        "x_earth": x_earth,
        "y_earth": y_earth,
        "z_earth": z_earth
    })

with open("assets/stars.json", "w") as outfile: 
    json.dump(stars, outfile)
