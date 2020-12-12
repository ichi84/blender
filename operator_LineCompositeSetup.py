import bpy
import os

#Library File info
BaseDir = os.path.dirname(os.path.realpath(__file__)) + "\\blend\\"
blendfile = "AOV.blend"
AssetName = "Material"
OverRideMaterialName  = "AOV"

#Cycles Settings
def SetCyclesSetting(scene):
    scene.render.engine = 'CYCLES'
    scene.cycles.feature_set = 'SUPPORTED'
    scene.cycles.device = 'CPU' #or 'GPU'
    scene.cycles.samples = 1
    scene.cycles.max_bounces = 1

#Get PreMeked Materials
def OverRideMaterials(scene):
    #get Material from .blend file
    directory = BaseDir + blendfile + "\\" + AssetName + "\\"
    bpy.ops.wm.link(
        filename=OverRideMaterialName,
        directory=directory)

    #OverrRide Material All Scenes
    for vl in scene.view_layers:
        vl.material_override = bpy.data.materials[OverRideMaterialName]

def addAOV(scene, name):
    for vl in scene.view_layers:
        for aov in vl.cycles.aovs:
            if(aov.name == name):
                return        
    bpy.ops.cycles.add_aov()
    vl.cycles.aovs[-1].name = name  

def SetAOVfromMaterials(scene):
    for m in bpy.data.materials:
        if  hasattr(m.node_tree, 'nodes'):
            for n in m.node_tree.nodes:
                if(n.type == "OUTPUT_AOV"):
                    addAOV(scene, n.name)

def start_main(context):
    for s in bpy.data.scenes:
        SetCyclesSetting(s)
        OverRideMaterials(s)
        SetAOVfromMaterials(s)
        s.use_nodes = True

    lapNode = bpy.data.scenes[0].node_tree.nodes.new(type='CompositorNodeFilter')
    lapNode.filter_type = 'LAPLACE'
    mathNode = bpy.data.scenes[0].node_tree.nodes.new(type='CompositorNodeMath')
    mathNode.operation = 'LESS_THAN'
    mathNode.inputs['Value'].default_value = .001

    #render Image
    bpy.ops.render.render()

    #render Animation
    #bpy.ops.render.render(animation=True)

classes = []
####################################################
#operator Class
####################################################
class MYADDON_OT_LineComposeteSetup(bpy.types.Operator):
    bl_idname = "myaddon.linecompositesetup"   #システム名。命名即は全部小文字！グローバルに（他アドオンも）被らないようにする
    bl_label = "Line Composite Setup"             #表示名
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        #なんか処理。
        start_main(context)
        return {"FINISHED"}

classes.append(MYADDON_OT_LineComposeteSetup)
#---------------------------------------------------


########################
#register and unregister
########################
def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in classes:
         bpy.utils.unregister_class(c)

