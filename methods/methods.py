import bpy

#Add control bones. 
#Then add Copy location constraint and Strech constraint to original bones.
def AddCtrlBone(context):
    #preferece
    CTLBONE_LENGTH = 0.5
    ENDCTLBONE_NAME = 'CTL_END'

    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.mode_set(mode='EDIT')
    armObject = context.active_object

    #create target bones collection
    bones_collection = [b for b in context.active_object.pose.bones]
    s = 0
    for b in bones_collection : s += b.length
    CTLBONE_LENGTH = CTLBONE_LENGTH * (s / len(bones_collection))

    #create new bone as a tail bone's child
    end_bones = [b for b in context.active_object.data.edit_bones if len(b.children) == 0]


    bpy.ops.object.mode_set(mode='EDIT')
    for end in end_bones:
        bname = ENDCTLBONE_NAME + '.' + end.name
        b = context.active_object.data.edit_bones.new(bname)
        b.head = end.tail
        b.tail = b.head
        b.tail.z = b.head.z + CTLBONE_LENGTH;
        b.parent = end

    #create Control bones
    for b in bones_collection:
        if (b in end_bones) == False:
            bpy.ops.object.mode_set(mode='EDIT')
            bname = 'CTL_' + b.name
            newbone = context.active_object.data.edit_bones.new(bname)
            newbone.head = b.head
            newbone.tail = newbone.head
            newbone.tail.z = newbone.head.z + CTLBONE_LENGTH;
            #set bone constraint
            bpy.ops.object.mode_set(mode='POSE')
            cr = b.constraints.new(type='COPY_LOCATION')
            cr.target = context.active_object
            cr.subtarget = bname
            cr.name = 'BT Copy Location'
            cr.target_space='POSE'
            cr.owner_space = 'POSE'

    #set Bone Constraints
    bpy.ops.object.mode_set(mode='POSE')
    for b in context.active_object.pose.bones:
        if len(b.children) != 0 :
            cr = b.constraints.new(type='STRETCH_TO')
            cr.target = context.active_object
            cr.subtarget = b.children[0].name
            cr.bulge = 0
            cr.name = "BT Stretch To"
            cr.keep_axis = 'PLANE_Z'

    #add cube
    bpy.ops.object.mode_set(mode='OBJECT')
    if "WGT_CUBE" not in bpy.data.objects:
        bpy.ops.mesh.primitive_cube_add(size=0.5, enter_editmode=False, align='WORLD', location=(0, 0, 0))
        context.object.name = "WGT_CUBE"
        context.object.hide_viewport = True

    bpy.context.view_layer.objects.active = armObject
    bpy.ops.object.mode_set(mode='POSE')
    for b in armObject.pose.bones:
        if b.name.startswith('CTL_'):
            b.custom_shape = bpy.data.objects["WGT_CUBE"]


    #clear parent all bone
    bpy.ops.object.mode_set(mode='EDIT')
    for b in context.active_object.data.edit_bones:
        if b.parent != None:
            b["org_parent"] = b.parent.name
            b["org_use_connect"] = b.use_connect
            b.parent = None
        if b.name.startswith('CTL_'):
            b.use_deform = False
            b.show_wire = True
            b.layers[31] = True
            for i in range(31):
                b.layers[i] = False

    #set layers visiblity
    bpy.ops.object.mode_set(mode='EDIT')
    for i in range(32):
        context.object.data.layers[i] = True
    bpy.ops.object.mode_set(mode='POSE')


#Apply pose, and ajust stretch length
def ApplyAll(context):
    #Apply All Armature Modifires
    ctxObj = context.active_object
    modObjs = []
    for o in [obj for obj in bpy.data.objects if obj.modifiers]:
        for m in [mod for mod in o.modifiers if hasattr(mod,'object')]:
            if m.object ==  context.active_object:
                context.view_layer.objects.active = o
                bpy.ops.object.modifier_apply(apply_as='DATA', modifier=m.name)
                modObjs.append(o)
    context.view_layer.objects.active = ctxObj
    
    #Apply Bone Stretch
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.armature_apply(selected=False)

    #Set Current Pose to rest Pose
    for b in context.active_object.pose.bones:
        for cr in b.constraints:
            if cr.type == 'STRETCH_TO':
                cr.rest_length = 0
    
    #reconvert
    ReconvertToOriginalBone(context)
    AddCtrlBone(context)
    
    for o in modObjs:
        context.view_layer.objects.active = o
        bpy.ops.object.modifier_add(type='ARMATURE')
        o.modifiers[len(o.modifiers)-1].object = ctxObj




#Return to Original Bone
def ReconvertToOriginalBone(context):
    bpy.ops.object.mode_set(mode='POSE')
    for b in context.active_object.pose.bones:
        for cr in b.constraints:
            if cr.name.startswith("BT "):
                b.constraints.remove(cr)

    bpy.ops.object.mode_set(mode='EDIT')
    for b in context.active_object.data.edit_bones:
        if "org_parent" in b:
            b.parent = context.active_object.data.edit_bones[ b["org_parent"] ]
        if "org_use_connect" in b:
            b.use_connect = b["org_use_connect"] == 1
        if b.name.startswith('CTL_'):
            context.active_object.data.edit_bones.remove(b)
