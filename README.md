# Project setup
## Prerequisites
Python 3.10+ with libraries:
* Astroquery (`pip install astroquery`)
* Astropy (`pip install astropy`)
* OpenCV (`pip install opencv-python`)

## Preparing the site
1. Run `python planet_coordinates.py` to generate a json file with planet coordinates.
2. Run `python object_finder.py` to generate a json file with stars' coordinates relative to Earth (assuming Earth to be constantly at `(0, 0, 0)` for simplicity).
3. Run `python create_skyboxes.py` to generate skyboxes for planets.
**NOTE:** This will take a while as it calculates star positions relative to each exoplanet. It will also consume an ungodly amount of RAM (32 gigabytes doesn't seem to be enough), therefore it might be better to partition the `assets/planets.json` file into smaller chunks and generate skyboxes for each chunk separately. This is due to the fact that OpenCV keeps all generated images in RAM before saving them to disk. Resulting skyboxes are in `assets/<planet name>/skybox_<cube_side>.png`.
4. Run `python create_skymaps.py` to generate sky maps for planets. Resulting skymaps are in `assets/<planet name>/skymap_n.png` and `assets/<planet name>/skymap_s.png`.
