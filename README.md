python3Dplay
============

Current Status: Just a framework for simple operations on .stl files.

End Goal: Allow slicing of .stl files for 3d printing using arbitrary surfaces as the layer contour. 

By using layers which are not simple planes orthogonal to the Z axis, we can improve the structural properties of prints. 
	-Parts intended to undergo torque along the Z axis can be made with radially interlocked layers to prevent shearing at layer boundaries.
	-Parts expected to undergo pressure along the z axis can be made with the layers curved up toward the region where pressure is expected.
	-Interior properties of the nonisotropic 3d printed parts can in general be manipulated.
	
Basic program structure (planned):
	1. Import .stl
	2. Import/select surface to be used as the layer contour. Format undecided as of yet. Ideally it will be a mathematical representation and not a mesh.
	3. Define the region of the contour that will actually contact the object
	4. Check that that region of the contour doesn't have any slopes too steep for the bevel of the printer hotend.
	5. For each layer:
		-Find intersections of the contour with the object
		-Generate perimeter paths and ensure that they are as continuous as possible. Continuous extrusions add to the strength of parts.
		-Generate infill paths, potentially with overlap to ensure they bond together strongly
		-Connect to previous layer
	6. Once the path is completed, map its proximity to itself along its length.
	7. Taking proximity to self into account, plan the extrusion along the path
	8. Convert to gcode and export
	
	
Open ends:
	-No firmware that I know of can do 3d curves, so curves will at some point have to be interpolated. For simplicity's sake, I'm also avoiding G2 arcs for now because I don't think their small benefit is worthwhile yet. The question then is, at what point in the program do we interpolate curves?
	-How should I represent the slicing contour? Mathematical formulae would be ideal because checking intersections of the .stl mesh against the contour mesh would be O(n*m) where n and m are polycounts of the model and the contour. 
	-How should top and bottom layers be done?
		-Slice using the contour from the beginning. This would potentially make some very funny looking first layers, and therefore limit this to machines that are almost perfectly in tram.
		-Make the first layer flat and all subsequent layers incl. the top with the contour. This moves the funny looking layers from before onto plastic, where they will adhere far better.
		-Make top and bottom flat which would make the top slightly prettier but not do much else. Would also complicate the code a fair bit if I wanted to do all top surfaces instead of just the topmost one.
	-How should I optimize the intersections check? I could use the max and min z values of each tri and the contour to eliminate a bunch, but i would need to see whether that actually provides savings. It probably does.