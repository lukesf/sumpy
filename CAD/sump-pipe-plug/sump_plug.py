import cadquery as cq

# These can be modified rather than hardcoding values for each dimension.
circle_radius = 55.0/2.        # Radius of the plate
thickness = 10.0            # Thickness of the plate
hole_radius = 16/2.
hole_offset = (42.-8.-8.)/2.
rectangle_width = 15.0      # Width of rectangular hole in cylindrical plate
rectangle_length = 10.0     # Length of rectangular hole in cylindrical plate

# Extrude a cylindrical plate with a rectangular hole in the middle of it.
# 1.  Establishes a workplane that an object can be built on.
# 1a. Uses the named plane orientation "front" to define the workplane, meaning
#     that the positive Z direction is "up", and the negative Z direction
#     is "down".
result = cq.Workplane("front").circle(circle_radius) 

result = result.pushPoints([(hole_offset, 0), (-hole_offset,0)])
result = result.circle(hole_radius)

result = result.pushPoints([(0, -20)])
result = result.rect(rectangle_width, rectangle_length) 

result = result.extrude(thickness)
result = result.edges("|Z").fillet(2)
result = result.edges("|Y").fillet(2)
#result = result.edges("#Z").fillet(2)

# Displays the result of this script
show_object(result)
