import bpy
from bpy.props import *
from .methods import image

# Opetator追加手順
# 1. Operatorクラスの定義。命名規則は "大文字_OT_xxxx" 
# 2. execute()内に処理を書く
# 3. 定義後にclassesにappend。

classes = []
keymaps = []
####################################################
#operator Class
####################################################
#オブジェクト原点を選択物に
class MYADDON_OT_moveOriginToSelect(bpy.types.Operator):
    bl_idname = "myaddon.moveorg2sel"   #システム名。命名即は全部小文字！グローバルに（他アドオンも）被らないようにする
    bl_label = "Move Object Origin to select."             #表示名
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.active_object.mode  != 'EDIT':
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
            return {"FINISHED"}

        pre = context.scene.cursor.location.xyz
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
        bpy.ops.object.mode_set(mode='EDIT')
        context.scene.cursor.location = pre
        return {"FINISHED"}
classes.append(MYADDON_OT_moveOriginToSelect)
#---------------------------------------------------

#カーソルをを選択物に
class MYADDON_OT_moveOriginToSelect(bpy.types.Operator):
    bl_idname = "myaddon.movecur2sel"   #システム名。命名即は全部小文字！グローバルに（他アドオンも）被らないようにする
    bl_label = "Move Cursor Origin to select."             #表示名
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.view3d.snap_cursor_to_selected()
        return {"FINISHED"}
classes.append(MYADDON_OT_moveOriginToSelect)
#---------------------------------------------------

def register_shortcut():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name="3D View", space_type='VIEW_3D')
        kmi = km.keymap_items.new(
            idname='myaddon.moveorg2sel',
            type='S',
            value='PRESS',
            shift=False,
            ctrl=True,
            alt=True
        )
        keymaps.append((km, kmi))

        km = kc.keymaps.new(name="3D View", space_type='VIEW_3D')
        kmi = km.keymap_items.new(
            idname='myaddon.movecur2sel',
            type='C',
            value='PRESS',
            shift=False,
            ctrl=True,
            alt=True
        )
        keymaps.append((km, kmi))

def unregister_shortcut():
    for km, kmi in keymaps:
        km.keymap_items.remove(kmi)
    keymaps.clear()



########################
#register and unregister
########################
def register():
    for c in classes:
        bpy.utils.register_class(c)
    register_shortcut()

def unregister():
    for c in classes:
         bpy.utils.unregister_class(c)
    unregister_shortcut()