import bpy
C = bpy.context
A = C.active_object

#選択エッジの長さを返す
def SelectedEdgeLength():
    bpy.ops.object.mode_set(mode='OBJECT')
    mat = A.matrix_world
    mesh = A.data
    l = 0.0
    for e in mesh.edges:
        if(e.select):
            l += (mat @(mesh.vertices[e.vertices[0]].co - mesh.vertices[e.vertices[1]].co)).length
    return l
