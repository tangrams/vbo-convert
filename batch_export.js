
// batch_export.js
// rough draft of batch tile export from Tangram -
// prepares tiles for conversion by vbo-export
//
// TODO:
// take in a selection of tiles from landgrab and pass files/data directly to vbo-export
//

mytiles = [{'x': 9647.0, 'y': 12323.0, 'z': 15},
 {'x': 9646.0, 'y': 12323.0, 'z': 15},
 {'x': 9645.0, 'y': 12323.0, 'z': 15},
 {'x': 9647.0, 'y': 12322.0, 'z': 15},
 {'x': 9646.0, 'y': 12322.0, 'z': 15}];

// find tile range
min = {x: Infinity, y: Infinity};
max = {x:-Infinity, y: -Infinity};
for (t in mytiles) {
  mt = mytiles[t];
  console.log(mt);
  console.log(min);
  console.log(max);

  min.x = Math.min(min.x, mt.x);
  min.y = Math.min(min.y, mt.y);
  max.x = Math.max(max.x, mt.x);
  max.y = Math.max(max.y, mt.y);
}
console.log("min:", min);
console.log("max:", max);
for (t in mytiles) { scene._loadTile(mytiles[t]); }

// prepare a list of links
elements = [];

// make a downloadable blob from a string and create a link to the blob
makelink = function(text) {
  window.URL = window.webkitURL || window.URL;
  var data = new Blob([text], {type: 'text/plain'});
  var u = window.URL.createObjectURL(data)

  elements.push(u);
  console.log(u);
}

for (t in mytiles) {
  mt = mytiles[t];
  coords = mt.x+"/"+mt.y+"/"+mt.z;

  // calculate offset relative to the extents of the tile batch -
  // the top-left tile is 0,0 - one tile over is 1,0 - one tile down is 0,1
  offset = {x: mt.x - min.x, y: mt.y - min.y};
  // multiply the offset by the local tile coordinate range for vertex position offset
  offset.x *= 4096;
  offset.y *= 4096;
  console.log("coords", coords);
  console.log("offset", offset);
  verts = Array.prototype.slice.call(new Float32Array(scene.tiles[coords].meshes.polygons.vertex_data));
  length = verts.length / 9;
  console.log("length:", length)

  // apply offset to tile vertices
  for (v in verts) {
      if (v % 9 == 0) verts[v] += offset.x;
      if (v % 9 == 1) verts[v] -= offset.y;
  }

  // make it one long string
  verts = verts.join('\n');
  // make it into a downloadable blob
  makelink(verts);
}

// open a new window
var opened = window.open("");
opened.document.write("<html><body></body></html>");
console.log("document");

// write the download links to all the blobs in the new window
for (e in elements) {
  var a = opened.document.createElement('a');
  a.href = elements[e];
  a.download = 'filename.txt';
  a.textContent = 'Download';

  window.open(elements[e], 'Download');

  opened.document.body.appendChild(a);
  var b = opened.document.createElement('br');
  opened.document.body.appendChild(b);
}

