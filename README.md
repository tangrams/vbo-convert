vbo-export
==========

A few ways to convert Tangram VBOs to 3D file formats.

These scripts assume that you have exported a tile's VBO, which can be as simple as executing following javascript:

`copy(scene.tiles["19292/24640/16"].gl_geometry.water.vertex_data)`

...then pasting the clipboard contents into a new text file. The result must then be trimmed of brackets and line numbers to produce a list of values as seen in the `tile_verts` file.

### usage

`python [scriptname] [infile] [outfile]`

### example usage

`python vbo_to_ply.py tile_verts tile_faces.ply`

### filelist

- tile_verts - processed vertices extracted from a Tangram tile's VBO
- tile_verts_small - a trimmed version of tile_verts with only 1000 vertices
- vbo_to_obj.py - Wavefront OBJ format converter
- tile_verts.obj - sample output of above
- vbo_to_ply.py - Stanford Poly format converter - includes vertex color information
- tile_verts.ply - sample output of above
- tile_points.ply - example pointcloud for visualization
- tile_faces.stl - example of OBJ file converted to STL
- tile_faces.gcode - file sliced with Makerbot software – ready to print!