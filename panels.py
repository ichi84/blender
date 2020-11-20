import bpy
from bpy.props import *
from . import operators
from . import operator_joystick
from . import operator_image

#パネル追加手順
# 1. Panel Classを追加。命名規則は "大文字_PT_xxxx"
# 2. Panel Class.draw()にパネルのレイアウトを記述
# 3. 定義後にclasessにappend

classes = []
####################################################
# Panel Class
#
# bl_space_type一覧
#     EMPTY,	VIEW_3D, IMAGE_EDITOR, NODE_EDITOR	SEQUENCE_EDITOR	CLIP_EDITOR,
#     DOPESHEET_EDITOR, GRAPH_EDITOR	NLA_EDITOR, TEXT_EDITOR	CONSOLE	INFO, 
#     TOPBAR, STATUSBAR	OUTLINER, PROPERTIES	FILE_BROWSER	PREFERENCES
# bl_region_type一覧
#     WINDOW	HEADER	CHANNELS, TEMPORARY	UI	TOOLS, TOOL_PROPS	PREVIEW	HUD,
#     NAVIGATION_BAR	EXECUTE	FOOTER, TOOL_HEADER
####################################################
AddonDisplayName = 'マイアドオン'

#サンプルパネル
class MYADDON_PT_Sample(bpy.types.Panel):
    bl_space_type  = 'VIEW_3D'        #どのビューに表示するか
    bl_region_type = 'UI'             #ビュー内のどこに入れるか。UIは右のサイドバーのとこ
    bl_category    = AddonDisplayName #どのパネルカテゴリに所属するか。ツールパネルのタブに表示される名前。
    bl_label       = "Sample"         #パネル内のグループのタイトル。
    
    def draw(self, context):    #パネルレイアウトをここに記述する
        layout = self.layout
        layout.label(text="ここは自作アドオンの処理置き場")
        layout.operator("myaddon.operator1", text = "動作テスト")    #ボタン追加。textはボタンテキスト

classes.append(MYADDON_PT_Sample)
#---------------------------------------------------

#ジョイスティック
class MYADDON_PT_joystick(bpy.types.Panel):
    bl_space_type  = 'VIEW_3D'        #どのビューに表示するか
    bl_region_type = 'UI'             #ビュー内のどこに入れるか。UIは右のサイドバーのとこ
    bl_category    = AddonDisplayName #どのパネルカテゴリに所属するか。ツールパネルのタブに表示される名前。
    bl_label       = "Input"          #パネル内のグループのタイトル。

    def draw(self, context):    #パネルレイアウトをここに記述する
        layout = self.layout
        layout.label(text="ゲームパッド入力")
        
        if context.scene.myaddon_joystick_started:
            butttonTxt = '停止'
        else:
            butttonTxt = '開始'
        layout.operator("myaddon.joystick2camera", text = butttonTxt)    #ボタン追加。textはボタンテキスト
classes.append(MYADDON_PT_joystick)
#---------------------------------------------------



#イメージエディタ
class MYADDON_PT_ImageUI(bpy.types.Panel):
    bl_space_type  = 'IMAGE_EDITOR'   #どのビューに表示するか
    bl_region_type = 'UI'             #ビュー内のどこに入れるか。UIは右のサイドバーのとこ
    bl_category    = AddonDisplayName #どのパネルカテゴリに所属するか。ツールパネルのタブに表示される名前。
    bl_label       = "機能１"         #パネル内のグループのタイトル。

    def draw(self, context): #パネルレイアウトをここに記述する
        layout = self.layout
        layout.label(text="新規画像")
        layout.operator("myaddon.newimage", text = "作成")    #ボタン追加。textはボタンテキスト

        layout.label(text="塗りつぶし")
        layout.operator("myaddon.fillcolor", text = "実行")    #ボタン追加。textはボタンテキスト

        layout.label(text="移動平均")
        layout.operator("myaddon.movemeanimage", text = "実行")    #ボタン追加。textはボタンテキスト


        layout.label(text="法線作成")
        layout.operator("myaddon.createnomalimage", text = "実行")    #ボタン追加。textはボタンテキスト

classes.append(MYADDON_PT_ImageUI)
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
    


