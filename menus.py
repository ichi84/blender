import bpy
from . import operators

#メニュー追加手順
# 1. Menu Classを追加。命名即は"大文字_MT_xxxx" 定義後にclassesにappend。
# 2. 追加したMenu Classをメニューのどこに表示するかをmenu_funcに記述
# 3. register/unregisterでmenu_funcをコールバック登録する。

classes = []
####################################################
#Menu Class
####################################################
class MYADDON_MT_mainmenu(bpy.types.Menu):
    bl_idname = "MYADDON_MT_mainmenu"     #システム名。グローバルに（他アドオンも）被らないようにする
    bl_label = "My Addon"                 #表示名
    bl_description = "My Addon scripts."  #表示説明文

    def draw(self, context):
        #Oparetorクラスを登録する
        layout = self.layout
        #layout.operator("Your operator's bl_idname. ex.hoge.hogehoge")
classes.append(MYADDON_MT_mainmenu)
#---------------------------------------------------

####################################################
# Menu関数   Register/Unregisterでコールバック関数として渡す
####################################################
def menu_func(self, context):
    self.layout.separator() #最初にセパレータ（横線）追加
    self.layout.menu(MYADDON_MT_mainmenu.bl_idname) #上で定義した、Menu Classを登録
#---------------------------------------------------


########################
#register and unregister
########################
def register():
    for c in classes:
        bpy.utils.register_class(c)
    #blender上でpyhton開発者ツールチップで出てくる場所にMenu関数を登録する。
    bpy.types.VIEW3D_MT_object.append(menu_func)
    #bpy.types.VIEW3D_MT_edit_armature.append(menu_func)
    #bpy.types.VIEW3D_MT_pose.append(menu_func)

def unregister():
    #bpy.types.VIEW3D_MT_edit_armature.remove(menu_func)
    #bpy.types.VIEW3D_MT_pose.remove(menu_func)
    bpy.types.VIEW3D_MT_object.append(menu_func)
    for c in classes: bpy.utils.unregister_class(c)

