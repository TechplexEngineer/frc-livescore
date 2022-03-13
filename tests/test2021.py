import difflib
import os
import sys
import yaml
import cv2.cv2 as cv2
import numpy as np

from livescore import Livescore2021

# Initialize new Livescore instance
frc = Livescore2021(debug=False)

error = False

with open('data/2021.yml') as data:
    values = yaml.load(data)

for f in values:

    expected_value = values[f]

    print("Processing: {}".format(f))

    # Read the image with OpenCV
    image = cv2.imread('images/2021/' + f)

    # Get score data
    data = frc.read(image, force_find_overlay=True)
    print(data)
    #
    # if str(data) != expected_value:
    #     error = True
    #
    #     d = difflib.Differ()
    #     diff = '\n'.join(d.compare(expected_value.splitlines(), str(data).splitlines()))
    #     print('[2019] Error Processing: {}\nDiff:\n{}'.format(f, diff))
    # else:
    #     print('[2019] {} Passed'.format(f))

    # break

if error:
    sys.exit(1)
