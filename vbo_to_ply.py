#new

from __future__ import division # required for float results when dividing ints
import os, sys
from glob import glob
from os.path import isfile, join
from itertools import islice

INPUT=sys.argv[1]
# zoom=int(sys.argv[3])

def convert(filename):

	# todo: get zoom from filename
	zoom=15# current zoom level - sets x & y scale relative to z values
	maximum_range = 4096 # tile-space coordinate maximum

	# convert from tile-space coords to meters, depending on zoom
	def tile_to_meters(zoom):
		return 40075016.68557849 / pow(2, zoom)

	conversion_factor = tile_to_meters(zoom) / maximum_range
	lines = []

	# get lines from input file
	with open(filename, 'r') as f:
		lines = [line.strip() for line in f]
	f.close()

	vertex_count = 0
	newlines = []

	# add vertex definitions
	for i, line in enumerate(lines):
		index = 0

		if len(line) == 0: # skip the occasional empty line
			continue

		newlines.append(line+"\n")
		vertex_count += 1
		# print('vertex_count', vertex_count)
		if (i % 1000 == 0): # print progress
			sys.stdout.flush()
			sys.stdout.write("\r"+(str(round(i / len(lines) * 100, 2))+"%"))

	sys.stdout.flush()
	sys.stdout.write("\r100%")
	sys.stdout.flush()

	# add simple face definitions - every three vertices make a face
	face_count = int(vertex_count / 3)
	for i in range(face_count):
		j = i*3
		newline = "3 "+str(j)+" "+str(j+1)+" "+str(j+2)+"\n"
		newlines.append(newline)

	name, extension = os.path.splitext(filename)
	OUTFILE = name + ".ply"
	open(OUTFILE, 'w').close() # clear existing OUTFILE, if any
	newfile = open(OUTFILE, "w")
	for line in newlines:
		newfile.write("%s" % line)
	newfile.close()

	def line_prepend(filename,line):
	    with open(filename,'r+') as f:
	        content = f.read()
	        f.seek(0,0)
	        f.write(line.rstrip('\r\n') + '\n' + content)

	# generate PLY header
	header = '''ply
	format ascii 1.0
	element vertex '''+str(vertex_count)+'''
	property float x
	property float y
	property float z
	element face '''+str(face_count)+'''
	property list uchar int vertex_indices
	end_header'''

	##
	## a header with vertex colors
	##

	# header = '''ply
	# format ascii 1.0
	# element vertex '''+str(vertex_count)+'''
	# property float x
	# property float y
	# property float z
	# property uchar red
	# property uchar green
	# property uchar blue
	# element face '''+str(face_count)+'''
	# property list uchar int vertex_indices
	# end_header
	# '''


	line_prepend(OUTFILE, header)
	print("Wrote "+OUTFILE)
if os.path.isfile(INPUT):
	sys.stdout.write("Converting 1 file\n")
	convert(INPUT)
elif os.path.isdir(INPUT):
	files = [ f for f in glob(INPUT+"*.vbo") if isfile(f) ]
	sys.stdout.write("Converting %s files\n"%(len(files)))
	for f in files:
		convert(f)
else:
	print('Unrecognized path')
print("Done!")
