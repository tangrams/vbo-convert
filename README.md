vbo-export
==========

A few ways to convert [Tangram](https://github.com/tangram-map/tangram) VBOs to 3D file formats.

![an exported 3D tile](https://github.com/tangram-map/vbo-export/blob/master/tile.png)

These scripts assume that you have exported a tile's VBO.

To export tile data, first identify the tile in question – Tangram provides a overlay of tile-sized divs for reference which are named according to their respective tile, and these can be identified through "inspect element" or similar methods. The name will be something like  "38602/49261/17".

Once the tile name is found, the raw data export can be as simple as executing the following javascript:

`copy(Array.prototype.slice.apply(scene.tiles["38602/49261/17"].gl_geometry.polygons.vertex_data))`

...then pasting the clipboard contents into a new text file. The result must then be trimmed of punctuation and white space to produce a plain list of values, one per line, as seen in the `tile_verts` file.

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
