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
    for vl in scene.view_layers:
        vl.use_pass_uv = True


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


def getAllNodes(NodeTree):
    result = []
    if  hasattr(NodeTree, 'nodes'):
        for n in NodeTree.nodes:
            if n.type == 'GROUP':
                result += getAllNodes(n.node_tree)
            else:
                if(n.name !="Group Input") and (n.name !="Group Output"):
                    result.append(n)
    return result

def SetAOVfromMaterials(scene):
    nodes = []
    for m in bpy.data.materials:
        nodes += getAllNodes(m.node_tree)

    for n in nodes:
        if(n.type == "OUTPUT_AOV"):
            addAOV(scene, n.name)


def CreateAndLinkScene(context, NameExt):
    scene = context.scene
    Name = scene.name +".Link.Line"
    
    if(NameExt in scene.name):
        return None
    #Create Scene
    if (Name) in bpy.data.scenes:
        #Re-Link Objects
        #Link Collections
        for c in scene.collection.children:
            if not c.name in bpy.data.scenes[Name].collection.children:
                bpy.data.scenes[Name].collection.children.link(c)
        #Link Top Level Objects
        for o in scene.collection.objects:
            if not o.name in bpy.data.scenes[Name].collection.objects:
                bpy.data.scenes[Name].collection.objects.link(o)
    else:
        bpy.ops.scene.new(type='LINK_COPY')
        newScene = context.window.scene
        newScene.name = Name
        
    bpy.data.scenes[Name].camera = scene.camera
    return bpy.data.scenes[Name]

def start_main(context):
    preScene = context.window.scene 
    for s in bpy.data.scenes:
        context.window.scene = s
        newScene = CreateAndLinkScene(context, ".Link.Line")
        if newScene != None:
            context.window.scene = newScene
            SetCyclesSetting(newScene)
            OverRideMaterials(newScene)
            SetAOVfromMaterials(newScene)
            newScene.use_nodes = True
    context.window.scene = preScene
    #render Image
    #bpy.ops.render.render()
    #render Animation
    #bpy.ops.render.render(animation=True)
    


"""
    lapNode = bpy.data.scenes[0].node_tree.nodes.new(type='CompositorNodeFilter')
    lapNode.filter_type = 'LAPLACE'
    mathNode = bpy.data.scenes[0].node_tree.nodes.new(type='CompositorNodeMath')
    mathNode.operation = 'LESS_THAN'
    mathNode.inputs['Value'].default_value = .001
"""

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

