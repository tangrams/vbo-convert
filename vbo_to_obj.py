from __future__ import division
import sys 
FILE=sys.argv[1]
OUTFILE=sys.argv[2]
stride=14
indices=[0,1,2]
zoom=16
maximum_range = 4096

open(OUTFILE, 'w').close()

def tile_to_meters(i):
	return 40075016.68557849 / pow(2, zoom)

conversion_factor = tile_to_meters(zoom) / maximum_range

def file_len(fname):
	with open(fname) as f:
		for i, l in enumerate(f):
			pass
	return i + 1

lines = file_len(FILE)
keep = []

loops = int(lines/stride)

for i in range(0,loops):
	offset= i*stride
	offset_indices = [j + offset for j in indices]
	#print offset_indices
	for k in offset_indices:
		keep.append(k)

newline = "v "
index = 0
vertex_count = 0
newfile = open(OUTFILE, "w")

with open(FILE, "r") as file:
	for i, line in enumerate(file):
		if i in keep:
			index += 1
			newline = newline + line.rstrip(",\n") + " "
			if index == 3:
				tokens = newline.split(" ")
				#print(tokens)
				tokens[1] = str(float(tokens[1]) * conversion_factor)
				tokens[2] = str(float(tokens[2]) * conversion_factor)
				newline = " ".join(tokens) + "\n"
				newfile.write(newline)
				newline = "v "
				index = 0
				vertex_count += 1
		if (i % 1000 == 0):
			print(str(round(i / offset_indices[len(offset_indices)-1] * 100, 2))+"%")
	face_count = vertex_count / 3
	for i in range(int(face_count)):
		j = i*3 + 1
		newline = "f "+str(j)+" "+str(j+1)+" "+str(j+2)+"\n"
		newfile.write(newline)
newfile.close()


def line_prepend(filename,line):
    with open(filename,'r+') as f:
        content = f.read()
        f.seek(0,0)
        f.write(line.rstrip('\r\n') + '\n' + content)


header = '''ply
format ascii 1.0
element vertex '''+str(vertex_count)+'''
property float x
property float y
property float z
element face '''+str(face_count)+'''
property list uchar int vertex_index
end_header
'''
# line_prepend(OUTFILE, header)