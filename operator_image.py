import bpy
from bpy.props import *
from .methods import image

# Opetator追加手順
# 1. Operatorクラスの定義。命名規則は "大文字_OT_xxxx" 
# 2. execute()内に処理を書く
# 3. 定義後にclassesにappend。

classes = []
####################################################
#operator Class
####################################################


#新規画像作成
class MYADDON_OT_newimage(bpy.types.Operator):
    bl_idname = "myaddon.newimage"   #システム名。命名即は全部小文字！グローバルに（他アドオンも）被らないようにする
    bl_label = "Create New Image"             #表示名
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        image.CreateNewImage(context=context, width=1024, height=1024)
        return {"FINISHED"}

classes.append(MYADDON_OT_newimage)
#---------------------------------------------------

#画像処理テスト　塗りつぶし
class MYADDON_OT_fill(bpy.types.Operator):
    bl_idname = "myaddon.fillcolor"   #システム名。命名即は全部小文字！グローバルに（他アドオンも）被らないようにする
    bl_label = "Fill Image"             #表示名
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        image.FillColor(context)
        return {"FINISHED"}

classes.append(MYADDON_OT_fill)
#---------------------------------------------------

#法線作成
class MYADDON_OT_fill(bpy.types.Operator):
    bl_idname = "myaddon.movemeanimage"   #システム名。命名即は全部小文字！グローバルに（他アドオンも）被らないようにする
    bl_label = "mean Image"             #表示名
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        image.MoveMeanImage(context)
        return {"FINISHED"}

classes.append(MYADDON_OT_fill)
#---------------------------------------------------

#法線作成
class MYADDON_OT_fill(bpy.types.Operator):
    bl_idname = "myaddon.createnomalimage"   #システム名。命名即は全部小文字！グローバルに（他アドオンも）被らないようにする
    bl_label = "Create Noemal Image"             #表示名
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        image.createNomalImage(context)
        return {"FINISHED"}

classes.append(MYADDON_OT_fill)
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

