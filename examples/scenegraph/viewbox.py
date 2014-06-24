"""
Simple test of stacking viewboxes, demonstrating the three methods that
can be used by a viewbox to provide clipping.

There is one root scene with an NDC camera. It contains two viewboxes.
One with an NDC camera on the left, and one with a pixel camera on the
right. Each of these viewboxes contains again two viewboxes. One with
ndc camera at the bottom, and one with a pixel camera at the top.

Use the global PREFER_PIXEL_GRID variables to set the clipping method
for the two toplevel and four leaf viewbox, respectively. You can also
manyally set the preferred_clip_method property of one or more viewboxes.

"""

import numpy as np

from vispy import app, gloo
from vispy import scene

gloo.gl.use('desktop debug')

# <<< Change method here
# With the none method you can see the absence of clipping.
# With the fbo method you can see the texture interpolation (induced by
# a delibirate mismatch in screen and textue resolution)
# Try different combinarions, like a viewport in an fbo
PREFER_PIXEL_GRID1 = 'fbo'  # none, viewport, fbo (fragment to come)
PREFER_PIXEL_GRID2 = 'viewport'


# Create lines for use in ndc and pixel coordinates
N = 1000
color = np.ones((N, 4), dtype=np.float32)
color[:, 0] = np.linspace(0, 1, N)
color[:, 1] = color[::-1, 0]
pos = np.empty((N, 2), np.float32)
#
pos[:, 0] = np.linspace(-1., 1., N)
pos[:, 1] = np.random.normal(0.0, 0.5, size=N)
pos[:20, 1] = -0.5  # So we can see which side is down
line_ndc = scene.visuals.Line(pos=pos.copy(), color=color)
#
pos[:, 0] = np.linspace(50, 350., N)
pos[:, 1] = 150 + pos[:, 1] * 50
pos[:20, 1] = 100  # So we can see which side is down
line_pixels = scene.visuals.Line(pos=pos.copy(), color=color)

# Create canvas
canvas = scene.SceneCanvas(size=(800, 600), show=True, close_keys='escape')
canvas.scene.camera = scene.cameras.NDCCamera()  # Default NDCCamera

# Create viewboxes left ...

vb1 = scene.ViewBox(canvas.scene)
vb1.pos = -1.0, -1.0
vb1.size = 1.0, 2.0
vb1.scene.camera = scene.cameras.NDCCamera()
#
vb11 = scene.ViewBox(vb1.scene)
vb11.pos = -1.0, -1.0
vb11.size = 2.0, 1.0
vb11.scene.camera = scene.cameras.TwoDCamera()
#
vb12 = scene.ViewBox(vb1.scene)
vb12.pos = -1.0, 0.0
vb12.size = 2.0, 1.0
vb12.scene.camera = scene.cameras.PixelCamera()
#vb12.scene.camera.scale = (100, 100)
#
line_ndc.add_parent(vb11.scene)
line_pixels.add_parent(vb12.scene)

box = np.array([[0,0], [0,1], [1,1], [1,0], [0,0]], dtype=np.float32)
unit_box = scene.visuals.Line(pos=box, color=(1,0,0,1), name='unit box')
nd_box = scene.visuals.Line(pos=box*2-1, color=(0,1,0,1), name='nd box')
vb11.add(unit_box)
vb11.add(nd_box)

# Create viewboxes right ...

vb2 = scene.ViewBox(canvas.scene)
vb2.pos = 0.0, -1.0
vb2.size = 1.0, 2.0
vb2.scene.camera = scene.cameras.PixelCamera()
#
vb21 = scene.ViewBox(vb2.scene)
vb21.pos = 0, 0
vb21.size = 400, 300
vb21.scene.camera = scene.cameras.TwoDCamera()
#
vb22 = scene.ViewBox(vb2.scene)
vb22.pos = 0, 300
vb22.size = 400, 300
vb22.scene.camera = scene.cameras.PixelCamera()
#
line_ndc.add_parent(vb21.scene)
line_pixels.add_parent(vb22.scene)

print vb1, vb11, vb12
print vb2, vb21, vb22

# Set preferred pixel grid method
for vb in [vb1, vb2]:
    vb.preferred_clip_method = PREFER_PIXEL_GRID1
for vb in [vb11, vb12, vb21, vb22]:
    vb.preferred_clip_method = PREFER_PIXEL_GRID2


# For testing/dev
vb1._name = 'vb1'
vb11._name = 'vb11'
vb12._name = 'vb12'
vb2._name = 'vb2'
vb21._name = 'vb21'
vb22._name = 'vb22'


if __name__ == '__main__':
    app.run()
