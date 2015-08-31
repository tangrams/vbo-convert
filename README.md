vbo-export
==========

A few ways to convert [Tangram](https://github.com/tangram-map/tangram) VBOs to 3D file formats.

![an exported 3D tile](https://github.com/tangram-map/vbo-export/blob/master/tile.png)

These scripts work with vertex buffer objects (VBOs) exported from Tangram. For an example of how to export these VBOs, see https://github.com/meetar/manhattan-project/blob/master/lib/batch_export.js

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
- tile_faces_base.stl - example of OBJ file converted to STL, with an extruded ground plane
- tile_faces_base.gcode - stl file sliced with Makerbot software – ready to print!
