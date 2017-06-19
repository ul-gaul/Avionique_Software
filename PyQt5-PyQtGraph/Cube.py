from PyQt5 import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy as np



app = QtGui.QApplication([])
w = gl.GLViewWidget()
w.show()
w.setWindowTitle("Cube")

w.setCameraPosition(distance=40)
gz = gl.GLGridItem()
gx = gl.GLGridItem()
gy = gl.GLGridItem()
gz.scale(0.1,0.1,0.1)
gx.scale(0.1,0.1,0.1)
gy.scale(0.1,0.1,0.1)
#w.addItem(gz)
w.addItem(gx)
w.addItem(gy)
gx.rotate(90,0,1,0)
gy.rotate(90,1,0,0)


"""
## Example 1:
## Array of vertex positions and array of vertex indexes defining faces
## Colors are specified per-face

verts = np.array([
    [0, 0, 0],
    [2, 0, 0],
    [1, 2, 0],
    [1, 1, 1],
])
faces = np.array([
    [0, 1, 2],
    [0, 1, 3],
    [0, 2, 3],
    [1, 2, 3]
])
colors = np.array([
    [1, 0, 0, 0.3],
    [0, 1, 0, 0.3],
    [0, 0, 1, 0.3],
    [1, 1, 0, 0.3]
])

## Mesh item will automatically compute face normals.
m1 = gl.GLMeshItem(vertexes=verts, faces=faces, faceColors=colors, smooth=True)
m1.setGLOptions('additive')
w.addItem(m1)
"""

#Cube

verts2 = np.array([
    [0, 0, 0],
    [0, 0, 2],
    [2, 0, 2],
    [2, 0, 0],
    [0, 2, 0],
    [0, 2, 2],
    [2, 2, 2],
    [2, 2, 0],
])
faces2 = np.array([
    [0, 1, 5],
    [0, 4, 5],
    [0, 3, 7],
    [0, 4, 7],
    [0, 1, 2],
    [0, 2, 3],
    [1, 5, 6],
    [1, 2, 6],
    [4, 5, 6],
    [4, 6, 7],
    [2, 3, 6],
    [2, 7, 6]
])

colors2 = np.ones((12,4), dtype=float)
m2 = gl.GLMeshItem(vertexes=verts2, faces=faces2,faceColors=colors2, smooth=False, drawEdges=True)
w.addItem(m2)
m2.translate(10,10,0)

mcyl = gl.MeshData.cylinder(rows=10, cols=100,radius=[1.0,1.0], length=5.0)
mcon = gl.MeshData.cylinder(rows=10,cols=100,radius=[1.0,0.],length=2.0)
#md = gl.MeshData.cylinder(rows=20, cols=20, radius=[2.0, 2.0], length=5.)
#colors = np.ones((mcyl.faceCount(),4), dtype=float)
m3 = gl.GLMeshItem(meshdata=mcyl, smooth=False, drawEdges=True, shader="balloon")
m4 = gl.GLMeshItem(meshdata=mcon, smooth=True, drawEdges=True)
m4.translate(0,0,5)
m3.rotate(10,1,1,0)
m4.rotate(10,1,1,0)
w.addItem(m3)
w.addItem(m4)




## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

