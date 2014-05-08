# Concentric segment plot utility
# Created by John Tocher, 09/05/2014
# 
# Built for generating a template for a particular type of word-chart

import svgwrite
import math
import os

from svgwrite import cm, mm 

# Put your paths here

output_path="/home/john/Temp"
output_file_name = "my_output_file.svg"

# basic drawing settings

ring_colour = 'black'
line_thickness = 2

# How many times to divide each subring, can be the same or different
# This number describes how many sectors each sector will be divided into
# If they're not multipes if the ones inside them, the segment lines won't 
# meet neatly, but it will still draw just fine!

annulus_segments = [ 6, 30 , 60 ]

# Ring radii

ring_radii = [ 20 , 40 , 60 ]

# Ring Colours

ring_colours = [ "red" , "green" , "blue" ]

# A Scale factor, not really necessary for svg, but can make testing simpler

global_scale_factor = 10

# Start of main program
# You shouldn't have to edit much below here if you just want variations on the original

base_radius = int(ring_radii[-1]) * global_scale_factor

annulus_count=0
annulus_radius=[]

# Origin
org_x=ring_radii[-1]*global_scale_factor
org_y=org_x
print "Scaled origin is {0},{1}".format(org_x,org_y)
print "Max Radii is {0}".format(ring_radii[-1])

outputfile=os.path.join(output_path,output_file_name)

dwg = svgwrite.Drawing(outputfile, profile='tiny')

outlines = dwg.add(dwg.g(id='outlines', stroke=ring_colour, stroke_width=line_thickness, fill='none'))

# First we'll draw and fill the circles

colour_count=-1
last_radius=0

for this_radius in reversed(ring_radii):

	outlines.add(dwg.circle((org_x,org_y),this_radius*global_scale_factor, fill=ring_colours[colour_count] ))
	colour_count-=1
	
annulus_count=0
last_radius=0

# Now we'll draw the segment dividing lines

for this_radius in ring_radii:

	sectors_for_this_annulus = annulus_segments[annulus_count]
	each_angle=2*math.pi/sectors_for_this_annulus

	for sector_count in range(0 , sectors_for_this_annulus ):
		this_angle = sector_count*each_angle
		inner_x = last_radius * math.cos(this_angle) * global_scale_factor
		inner_y = last_radius * math.sin(this_angle) * global_scale_factor
		outer_x = this_radius * math.cos(this_angle) * global_scale_factor
		outer_y = this_radius * math.sin(this_angle) * global_scale_factor
		outlines.add(dwg.line( (org_x+inner_x,org_x+inner_y) , (org_x+outer_x,org_y+outer_y) ))
		print "Annulus {0} Sector {1} angle {2} from ( {3},{4} ) to ( {5},{6} )".format(annulus_count, sector_count, this_angle, inner_x , inner_y, outer_x, outer_y)
		
	annulus_count+=1
	last_radius = this_radius
	
dwg.save()
