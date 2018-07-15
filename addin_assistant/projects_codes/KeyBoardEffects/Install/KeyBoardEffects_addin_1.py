# -*- coding: utf-8 -*- # 
import arcpy
import pythonaddins
import pythoncom
import pyHook
global flag
flag = False
class End_Effect(object):
    """Implementation for End_Effect_addin.button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def Effects(object):
        mxd = arcpy.mapping.MapDocument('current')
        df = pythonaddins.GetSelectedTOCLayerOrDataFrame()
        if (df.isFeatureLayer == True) or (df.isGroupLayer == True) or (df.isRasterLayer == True) or (df.isServiceLayer == True):
            df.visible == False
        else:
            df.visible == False
    def onMouseEvent(event):
        print "MessageName:",event.MessageName   
        print "Message:", event.Message   
        print "Time:", event.Time   
        print "Window:", event.Window   
        print "WindowName:", event.WindowName   
        print "Position:", event.Position   
        print "Wheel:", event.Wheel   
        print "Injected:", event.Injected      
        print"---"

        return True
      
    def onKeyboardEvent(event):   
#         global KeyValue
        print "MessageName:", event.MessageName   
        print "Message:", event.Message   
        print "Time:", event.Time   
        print "Window:", event.Window   
        print "WindowName:", event.WindowName   
        print "Ascii:", event.Ascii, chr(event.Ascii)   
        print "Key:", event.Key   
#         KeyValue = event.Key 
        if event.Key  ==  'Space':
            Effects()
        print "KeyID:", event.KeyID   
        print "ScanCode:", event.ScanCode   
        print "Extended:", event.Extended   
        print "Injected:", event.Injected   
        print "Alt", event.Alt   
        print "Transition", event.Transition   
        print "---"    
        return True 
     
    def main():   
        hm = pyHook.HookManager()   
 
        hm.KeyDown = onKeyboardEvent   

        hm.HookKeyboard()   
  
        hm.MouseAll = onMouseEvent   
 
        hm.HookMouse()   
 
        pythoncom.PumpMessages()
        
    def onClick(self):
        main()

class Start_Effect(object):
    """Implementation for Start_Effect_addin.button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False

    def Effects(object):
        mxd = arcpy.mapping.MapDocument('current')
        df = pythonaddins.GetSelectedTOCLayerOrDataFrame()
        if (df.isFeatureLayer == True) or (df.isGroupLayer == True) or (df.isRasterLayer == True) or (df.isServiceLayer == True):
            df.visible == True
        else:
            df.visible == False
            
    def onMouseEvent(event):
        print "MessageName:",event.MessageName   
        print "Message:", event.Message   
        print "Time:", event.Time   
        print "Window:", event.Window   
        print "WindowName:", event.WindowName   
        print "Position:", event.Position   
        print "Wheel:", event.Wheel   
        print "Injected:", event.Injected      
        print"---"

        return True
      
    def onKeyboardEvent(event):   
#         global KeyValue
        print "MessageName:", event.MessageName   
        print "Message:", event.Message   
        print "Time:", event.Time   
        print "Window:", event.Window   
        print "WindowName:", event.WindowName   
        print "Ascii:", event.Ascii, chr(event.Ascii)   
        print "Key:", event.Key   
#         KeyValue = event.Key 
        if event.Key  ==  'Space':
            Effects()
        print "KeyID:", event.KeyID   
        print "ScanCode:", event.ScanCode   
        print "Extended:", event.Extended   
        print "Injected:", event.Injected   
        print "Alt", event.Alt   
        print "Transition", event.Transition   
        print "---"    
        return True
        
    def main():   
        hm = pyHook.HookManager()   
 
        hm.KeyDown = onKeyboardEvent   

        hm.HookKeyboard()   
  
        hm.MouseAll = onMouseEvent   
 
        hm.HookMouse()   
 
        pythoncom.PumpMessages()
        
    def onClick(self):
        flag = True
        main()
