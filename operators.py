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
#サンプルオペレータ。残しておいても悪さはしない。コピーして使ってね。
class MYADDON_OT_operator1(bpy.types.Operator):
    bl_idname = "myaddon.operator1"   #システム名。命名即は全部小文字！グローバルに（他アドオンも）被らないようにする
    bl_label = "Say Comment"             #表示名
    bl_options = {'REGISTER', 'UNDO'}

    #properties
    comment: StringProperty(default = "hoge", options = {'HIDDEN'})

    def execute(self, context):
        #なんか処理。
        self.report({'INFO'}, self.comment)
        return {"FINISHED"}

classes.append(MYADDON_OT_operator1)
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

