
#XBOX Controller
axisName = ['Lstick x', 'Lstick y', 'Ltriger', 'Rstick x', 'Rstick y', 'Rtriger' ]
TrigerThreathiold = 0.1


import bpy
from bpy.props import *
import sys
import site

try:
	import pygame
except ImportError:
	try:
		import subprocess
		import ensurepip

		ensurepip.bootstrap()
		pybin = bpy.app.binary_path_python
		subprocess.check_call([pybin, '-m', 'pip', 'install', '--upgrade', 'pip', '--user'])
		subprocess.check_call([pybin, '-m', 'pip', 'install', 'pygame', '--user'])
		import pygame
		
	except subprocess.SubprocessError:
		print("Can't load module.: pygame")

from pygame.locals import *
import time
import threading

classes = []

def printAxesStatus(joystick):
    axesNum = joystick.get_numaxes()

    for i in range(axesNum):
        bpy.context.scene.myaddon_joystick_axesValue[i] \
            = joystick.get_axis(i) - bpy.context.scene.myaddon_joystick_axesInit[i] 
    
    for i in range(axesNum):
        if abs( bpy.context.scene.myaddon_joystick_axesValue[i] ) > TrigerThreathiold:
            print(axisName[i] + ': ' +str(bpy.context.scene.myaddon_joystick_axesValue[i]))


def getStatus(joystick):
    #axes
    axesNum = joystick.get_numaxes()
    for i in range(axesNum):
        bpy.context.scene.myaddon_joystick_axesValue[i] \
            = joystick.get_axis(i) - bpy.context.scene.myaddon_joystick_axesInit[i] 
        if abs( bpy.context.scene.myaddon_joystick_axesValue[i] ) <TrigerThreathiold:
            bpy.context.scene.myaddon_joystick_axesValue[i] = 0.0

    #hat button
    x,y  = joystick.get_hat(0)
    bpy.types.Scene.myaddon_joystick_hatValue = x,y

    #other buttons

def moveObject(name, joystick):
    dash = 1
    if joystick.get_button(1): #R button
        dash = 2.4
    if joystick.get_button(0): #L button
        dash = .2
    
    try:
        moveScale = .7
        #target = bpy.data.objects['Cube']
        target = bpy.data.objects[name]

        if target.type == 'CAMERA':
            dash *= .3

        target_vector = target.matrix_world.transposed().to_3x3()
        localXaxis = target_vector[0]
        localYaxis = target_vector[1]
        localZaxis = target_vector[2]

        if target.type == 'CAMERA':
            front = localZaxis
            right = localXaxis
        else:
            front = localYaxis
            right = -localXaxis

        #前後
        target.location.x += front[0] *bpy.context.scene.myaddon_joystick_axesValue[1]* moveScale * dash
        target.location.y += front[1] *bpy.context.scene.myaddon_joystick_axesValue[1]* moveScale * dash
        #左右
        target.location.x += right[0] *bpy.context.scene.myaddon_joystick_axesValue[0]* moveScale * dash
        target.location.y += right[1] *bpy.context.scene.myaddon_joystick_axesValue[0]* moveScale * dash

        #回転
        rotateScalePitch = .2
        rotateScaleYaw = .5
        if target.type == 'CAMERA':
            zoomCalc = target.data.lens/50.
            rotateScaleYaw /= zoomCalc
            rotateScalePitch /= zoomCalc
        else:
            rotateScalePitch *= -1

        target.rotation_euler[2] -= bpy.context.scene.myaddon_joystick_axesValue[3]*rotateScaleYaw *dash
        target.rotation_euler[0] -= bpy.context.scene.myaddon_joystick_axesValue[4]*rotateScalePitch *dash
        
        #ズーム
        ZoomScale = 20      
        if target.type == 'CAMERA':
            target.data.lens += bpy.context.scene.myaddon_joystick_axesValue[5]*ZoomScale *dash #R Triggerでズームイン
            target.data.lens -= bpy.context.scene.myaddon_joystick_axesValue[2]*ZoomScale *dash #L Triggerでズームアウト
            if target.data.lens < 7.0: #リミット
                target.data.lens = 7.0

        #Z（高さ）移動
        LiftScale = .5
        if joystick.get_button(4): #L button で下がる
            target.location.z -= moveScale  *LiftScale*dash 
        if joystick.get_button(5): #R button で上がる
            target.location.z += moveScale   *LiftScale*dash 
        

    except:
        print('except')
        
def AxesInit(joystick):
    axesNum = joystick.get_numaxes()
    print('axes initializie.')
    axisInitValue = [] #clear past value.
    for i in range(axesNum):
        axisInitValue.append( joystick.get_axis(i) )
    
    bpy.context.scene.myaddon_joystick_axesInit = tuple(axisInitValue)

def init():
    pygame.init()
    pygame.joystick.init()
    if pygame.joystick.get_count() < 1: #joystickがない
        return None 
    joystick0 = pygame.joystick.Joystick(0)
    joystick0.init()
    
    #軸はニュートラルが0ではない。ニュートラル位置として初期位置を記録。
    AxesInit(joystick0) 
    return joystick0

class GamePadHandler(threading.Thread):
    joystick = None
    target = "Camera"
    def __init__(self, joystick, name):
        super().__init__()
        self.joystick = joystick
        self.target = name

    def run(self):
        loop = True
        while loop:
            getStatus(self.joystick)
            moveObject(self.target, self.joystick)
            for e in pygame.event.get():
                
                if e.type == pygame.locals.JOYAXISMOTION:
                    printAxesStatus(self.joystick)
                    
                elif e.type == pygame.locals.JOYHATMOTION:
                    x, y = self.joystick.get_hat(0)
                    print('hat x:' + str(x) + ' hat y:' + str(y) )
                elif e.type == pygame.locals.JOYBUTTONDOWN:
                    print('button:' + str(e.button) )
            time.sleep(0.1)
            try:
                loop = bpy.context.scene.myaddon_joystick_started
            except:
                loop = False


#ジョイスティックコントロール
class MYADDON_OT_joystick2camera(bpy.types.Operator):
    bl_idname = "myaddon.joystick2camera"    #システム名。命名即は全部小文字！グローバルに（他アドオンも）被らないようにする
    bl_label = "Camera controll by joystick start" #表示名
    bl_options = {'REGISTER', 'UNDO'}
    #properties

    def execute(self, context):
        if bpy.context.scene.myaddon_joystick_started:
            bpy.context.scene.myaddon_joystick_started = False
        else:
            joystick0 = init()
            if joystick0 :
                bpy.context.scene.myaddon_joystick_started = True
                thread = GamePadHandler(joystick0, context.active_object.name)
                thread.start()
            else:
                self.report({'INFO'}, 'No Gamepad connected.')
        return {"FINISHED"}
             
classes.append(MYADDON_OT_joystick2camera)
#---------------------------------------------------

def register():
    for c in classes:
        bpy.utils.register_class(c)
    #properties
    bpy.types.Scene.myaddon_joystick_started = bpy.props.BoolProperty(name = 'Gamepad start status', default = False)
    bpy.types.Scene.myaddon_joystick_axesInit = bpy.props.FloatVectorProperty(size=len(axisName))
    bpy.types.Scene.myaddon_joystick_axesValue = bpy.props.FloatVectorProperty(size=len(axisName))
    bpy.types.Scene.myaddon_joystick_hatValue = bpy.props.FloatVectorProperty(size=2)
    bpy.types.Scene.myaddon_joystick_buttonValue = bpy.props.FloatVectorProperty(size=20)
    bpy.types.Scene.myaddon_joystick_active_name = bpy.props.StringProperty(default = "Camera")
    

def unregister():
    for c in classes:
         bpy.utils.unregister_class(c)
    #properties
    del bpy.types.Scene.myaddon_joystick_started
    del bpy.types.Scene.myaddon_joystick_axesInit
    del bpy.types.Scene.myaddon_joystick_axesValue
    del bpy.types.Scene.myaddon_joystick_hatValue
    del bpy.types.Scene.myaddon_joystick_buttonValue
    del bpy.types.Scene.myaddon_joystick_active_name