# Project setup
## Prerequisites
Python 3.10+ with libraries:
* Astroquery (`pip install astroquery`)
* Astropy (`pip install astropy`)
* OpenCV (`pip install opencv-python`)

## Preparing the site
Run `python planet_coordinates.py` to generate a json file with planet coordinates.
Run `python object_finder.py` to generate a json file with stars' coordinates relative to Earth (assuming Earth to be constantly at `(0, 0, 0)` for simplicity).
Run `python create_skyboxes.py` to generate skyboxes for planets. This will take a while as it calculates star positions relative to each exoplanet.
