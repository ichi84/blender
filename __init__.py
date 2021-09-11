bl_info = {
    "name" : "MyAddonTemplate",
    "author" : "ich",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

from . import menus
from . import panels
from . import operators
from . import operator_joystick
from . import operator_image
from . import operator_LineCompositeSetup
from . import operator_snap

def register():
    operator_LineCompositeSetup.register()
    operator_joystick.register()
    operator_image.register()
    operator_snap.register()
    operators.register()
    menus.register()
    panels.register()
    
def unregister():
    operator_LineCompositeSetup.unregister()
    operator_joystick.unregister()    
    operator_image.unregister()
    operator_snap.unregister()
    operators.unregister()
    menus.unregister()
    panels.unregister()
    

