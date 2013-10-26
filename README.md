python3Dplay
============

This project is a slicer for 3d printers. Conventional slicers cut 3d meshes into planar layers, then fill those layers with paths for the 3d printer to follow. This project differs in that instead of slicing with planes,
I plan to slice with arbitrary functions of 2 variables. In the iteration hosted here, those functions were meant to be represented as meshes, which is why most of this repo is just code for mesh intersections.

The iteration hosted here was my first attempt, which I dropped part way through because I realized it would never be efficient. I was trying to take the direct approach imitating regular slicers:
Occlude my slicing surface for each layer, then fill it with paths. 

However this approach is inherently slow because even with tricky optimizations (see boundingbox.py) I have to check check some of the triangles in the slicing surface against many of the triangles in the object for
every layer. It also gets extremely complex in the uppermost layers.

My new approach is to take every point in the object, find the value of the surface function at its (x,y) coordinates, and add that value to its z coordinate. This produces a version of the object warped by the slicing
surface. I can then slice this warped version into flat layers very efficiently like conventional slicers, and populate those layers with toolpaths. Finally, I can shift every point in the toolpaths downward by
their values on the surface function. This deforms each layer into the shape of the function, and deforms all the layers such that they add up to the original object.

This project is essentially on hold right now until I have my 3d printer project at Marshall Lane Elementary done, and my early action college apps out of the way.