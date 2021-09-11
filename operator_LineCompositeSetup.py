import bpy
import os

#Library File info
BaseDir = os.path.dirname(os.path.realpath(__file__)) + "\\blend\\"
blendfile = "AOV.blend"
MaterialName  = "AOV"
CompositeNodeName = "AOV.CompositNode"
NodeStep = (300, 0)

#Cycles Settings
def SetCyclesSetting(scene):
    scene.render.engine = 'CYCLES'
    scene.cycles.feature_set = 'SUPPORTED'
    scene.cycles.device = 'CPU' #or 'GPU'
    scene.cycles.samples = 1
    scene.cycles.max_bounces = 1
    for vl in scene.view_layers:
        vl.use_pass_uv = True

#Set PreMeked Materials
def OverRideMaterials(scene):
    #get Material from .blend file
    directory = BaseDir + blendfile + "\\Material\\"
    if not MaterialName in bpy.data.materials:
        bpy.ops.wm.append(   #link
            filename=MaterialName,
            directory=directory)
    #OverrRide Material All Scenes
    for vl in scene.view_layers:
        vl.material_override = bpy.data.materials[MaterialName]

def LinkNodeSameSockets(scene, fromNode, toNode):
    for o in fromNode.outputs:
        for i in toNode.inputs:
            if o.name == i.name:
                scene.node_tree.links.new(fromNode.outputs[o.name], toNode.inputs[i.name])

def CreateFileSaveAllPasses(scene, context):
    output_path = context.preferences.filepaths.render_output_directory
    node = scene.node_tree.nodes.new('CompositorNodeOutputFile')


def AddCompositeNode(scene, context):
    directory = BaseDir + blendfile + "\\NodeTree\\"
    bpy.ops.wm.link( 
        filename=CompositeNodeName,
        directory=directory)

    if not CompositeNodeName in scene.node_tree.nodes:
        pos = [0,0]
        node0 = scene.node_tree.nodes.new('CompositorNodeRLayers')
        node0.location = pos

        node1 = scene.node_tree.nodes.new('CompositorNodeGroup')
        node1.node_tree =  bpy.data.node_groups[CompositeNodeName]
        node1.name = CompositeNodeName
        pos[0] += NodeStep[0]
        pos[1] += NodeStep[1]
        node1.location = pos

        LinkNodeSameSockets(scene, node0, node1)

        node2 = scene.node_tree.nodes.new('CompositorNodeMixRGB')
        pos[0] += NodeStep[0]
        pos[1] += NodeStep[1]
        node2.location = pos
        node2.blend_type = 'MULTIPLY'
        scene.node_tree.links.new(node1.outputs['Value'], node2.inputs[1])

        selectedNodes = [i for i in scene.node_tree.nodes if i.select]
        
        for l in scene.node_tree.links:
            if l.to_node.type == 'COMPOSITE':
                lastSocket = l.from_socket
                scene.node_tree.links.new(lastSocket, node2.inputs[2])

        node3 = None
        for n in scene.node_tree.nodes:
            if n.type == 'COMPOSITE':
                node3 = n

        if node3 == None:
            node3 = scene.node_tree.nodes.new('CompositorNodeComposite')
            node3.location = pos
            pos[0] += NodeStep[0]
            pos[1] += NodeStep[1]
    
        scene.node_tree.links.new(node2.outputs['Image'], node3.inputs['Image'])
 
        node4 = scene.node_tree.nodes.new('CompositorNodeViewer')
        pos[0] += NodeStep[0]
        pos[1] += NodeStep[1]
        node4.location = pos
        scene.node_tree.links.new(node2.outputs['Image'], node4.inputs['Image'])
        node3.select


def addUVMap():
    for o in [i for i in bpy.data.objects if i.type=='MESH']:
         o.data.uv_layers.new(name="AOV.UV")

def addAOV(scene, name):
    for vl in scene.view_layers:
        for aov in vl.aovs:
            if(aov.name == name):
                return        
    bpy.ops.scene.view_layer_add_aov()
    vl.aovs[-1].name = name  

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
    #Each Scene
    for s in bpy.data.scenes:
        s.use_nodes = True
        context.window.scene = s
        newScene = CreateAndLinkScene(context, ".Link.Line")
        #Only new scene
        if newScene != None:
            context.window.scene = newScene
            SetCyclesSetting(newScene)
            OverRideMaterials(newScene)
            SetAOVfromMaterials(newScene)
        AddCompositeNode(s, context)
    
    #All Data
    addUVMap()
    #Restore active scene
    context.window.scene = preScene
 
    #render Image
    #bpy.ops.render.render()
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

