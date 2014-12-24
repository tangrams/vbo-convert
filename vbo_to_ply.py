from __future__ import division # required for float results when dividing ints
import sys 
INFILE=sys.argv[1]
OUTFILE=sys.argv[2]
# zoom=int(sys.argv[3])

# todo: get stride from vertex buffer layout property
stride=9 # number of total lines for each vertex in VBO
indices=[0,1,2,3,4,5,6] # lines we want to keep
zoom=17 # current zoom level
maximum_range = 4096 # tile-space coordinate maximum

open(OUTFILE, 'w').close() # clear existing OUTFILE

# convert from tile-space coords to meters, depending on zoom
def tile_to_meters(zoom):
	return 40075016.68557849 / pow(2, zoom)

conversion_factor = tile_to_meters(zoom) / maximum_range

# get number of lines in a file
def file_len(fname):
	with open(fname) as f:
		for i, l in enumerate(f):
			pass
	return i + 1

lines = file_len(INFILE)
keep = [] # array of kept lines

loops = int(lines/stride) # cast to int because of "division" module

for i in range(0,loops):
	offset= i*stride
	offset_indices = [j + offset for j in indices]
	# print offset_indices
	for k in offset_indices:
		keep.append(k)
# print keep
newline = ""
index = 0
vertex_count = 0
newfile = open(OUTFILE, "w")

with open(INFILE, "r") as file:
	for i, line in enumerate(file):
		if i in keep:
			# collect all the relevant lines for this vertex
			newline = newline + line.rstrip(",\n") + " "
			if index == len(indices)-1:
				# perform conversions
				tokens = newline.split(" ")
				# print "tokens:"
				# print tokens
				tokens[0] = str(float(tokens[0]) * conversion_factor)
				tokens[1] = str(float(tokens[1]) * conversion_factor)
				# print "tokens:"
				# print tokens
				# print float(tokens[3])
				# color = int(tokens[3])
				# tokens[3] = str(int(float(tokens[3]) * 255)) # vertex color is a uchar
				# tokens[4] = str(int(float(tokens[4]) * 255))
				# tokens[5] = str(int(float(tokens[5]) * 255))
				newline = " ".join(tokens)
				newfile.write(newline + "\n")
				newline = ""
				index = 0
				vertex_count += 1
			else:
				index += 1
		if (i % 1000 == 0): # print progress
			sys.stdout.flush()
			sys.stdout.write("\r"+(str(round(i / offset_indices[len(offset_indices)-1] * 100, 2))+"%"))
	face_count = int(vertex_count / 3)
	for i in range(face_count):
		j = i*3
		newline = "3 "+str(j)+" "+str(j+1)+" "+str(j+2)+"\n"
		newfile.write(newline)
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
end_header
'''
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