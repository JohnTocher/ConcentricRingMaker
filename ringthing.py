""" Concentric segment plot utility
    Created by John Tocher, 09/05/2014

    Built for generating a template for a particular type of word-chart
    Updated on 14/11/2014 tested with python 3.6.6
"""

import os
import math
import svgwrite

# Put your paths here

OUTPUT_PATH = "/home/john/Temp"
OUTPUT_FILE_NAME = "my_output_file.svg"

# basic drawing settings

RING_COLOUR = 'black'
LINE_THICKNESS = 2

# How many times to divide each subring, can be the same or different
# This number describes how many sectors each sector will be divided into
# If they're not multipes if the ones inside them, the segment lines won't
# meet neatly, but it will still draw just fine!

ANNULUS_SEGMENTS = [6, 30, 60]

# Ring radii

RING_RADII = [20, 40, 60]

# Ring Colours

RING_COLOURS = ["red", "green", "blue"]

# A Scale factor, not really necessary for svg, but can make testing simpler

GLOBAL_SCALE_FACTOR = 10

# Start of main program
# You shouldn't have to edit much below here if you just want variations on the original

def create_the_image():
    """ Create the image with the defined parameters
    """

    #base_radius = int(RING_RADII[-1]) * GLOBAL_SCALE_FACTOR

    annulus_count = 0
    #annulus_radius = []

    # Origin
    org_x = RING_RADII[-1] * GLOBAL_SCALE_FACTOR
    org_y = org_x
    print("Scaled origin is {0},{1}".format(org_x, org_y))
    print("Max Radii is {0}".format(RING_RADII[-1]))

    outputfile = os.path.join(OUTPUT_PATH, OUTPUT_FILE_NAME)

    dwg = svgwrite.Drawing(outputfile, profile='tiny')

    outlines = dwg.add(dwg.g(id='outlines',
                             stroke=RING_COLOUR,
                             stroke_width=LINE_THICKNESS,
                             fill='none'))

    # First we'll draw and fill the circles

    colour_count = -1
    last_radius = 0

    for this_radius in reversed(RING_RADII):

        outlines.add(dwg.circle((org_x, org_y),
                                this_radius * GLOBAL_SCALE_FACTOR,
                                fill=RING_COLOURS[colour_count]))
        colour_count -= 1

    annulus_count = 0
    last_radius = 0

    # Now we'll draw the segment dividing lines

    for this_radius in RING_RADII:

        sectors_for_this_annulus = ANNULUS_SEGMENTS[annulus_count]
        each_angle = 2 * math.pi / sectors_for_this_annulus

        for sector_count in range(0, sectors_for_this_annulus):
            this_angle = sector_count*each_angle
            inner_x = last_radius * math.cos(this_angle) * GLOBAL_SCALE_FACTOR
            inner_y = last_radius * math.sin(this_angle) * GLOBAL_SCALE_FACTOR
            outer_x = this_radius * math.cos(this_angle) * GLOBAL_SCALE_FACTOR
            outer_y = this_radius * math.sin(this_angle) * GLOBAL_SCALE_FACTOR
            outlines.add(dwg.line((org_x + inner_x, org_x+inner_y),
                                  (org_x + outer_x, org_y+outer_y)))
            print("Annulus {0} Sector {1} angle {2} from ( {3},{4} ) to ( {5},{6} )".format(
                annulus_count, sector_count, this_angle, inner_x, inner_y, outer_x, outer_y))

        annulus_count += 1
        last_radius = this_radius

    dwg.save()

if __name__ == "__main__":
    create_the_image()

