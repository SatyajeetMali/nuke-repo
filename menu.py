
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#custom nuke settings
# Date- May 24 2020
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Global imports

import nuke
import nukescripts 
import os




#--------------------------------------------------------------------------------------

import pixelfudger


#--------------------------------------------------------------------------------------
#SHORTCUTS


nuke.menu('Nodes').addCommand('Transform/Tracker', 'nuke.createNode("Tracker4").knob("shutteroffset").setValue("centered")', "ctrl+alt+t", icon= 'Tracker.png', shortcutContext = 2)
nuke.menu("Nodes").addCommand("Time/FrameHold", 'nuke.createNode("FrameHold").knob("first_frame").setValue(nuke.frame())', "ctrl+alt+h", icon= "FrameHold.png", shortcutContext = 2)
nuke.menu("Nodes").addCommand("Channel/Shuffle", 'nuke.createNode("Shuffle")', "ctrl+alt+s", icon="Shuffle.png", shortcutContext = 2)
nuke.knobDefault("Merge2.bbox", "B" )
nuke.knobDefault("Merge2.label", "pipe:[value bbox]")
nuke.knobDefault("Copy.label", "pipe:[value bbox]")
nuke.knobDefault("Transform.shutteroffset", "centered")
nuke.knobDefault("ScanlineRender.shutteroffset", "centered")

t = nuke.menu('Nodes')
t.addMenu('Tools')

def opSwitcher():
    ns = nuke.selectedNode()
    if ns.Class() == "Merge2":
        if ns.knob('operation').value() == 'over':
            ns.knob('operation').setValue('mask')
        elif ns.knob('operation').value() == 'mask':
            ns.knob('operation').setValue('stencil')
        elif ns.knob('operation').value() == 'stencil':
            ns.knob('operation').setValue('plus')
        elif ns.knob('operation').value() == 'plus':
            ns.knob('operation').setValue('minus')
        elif ns.knob('operation').value() == 'minus':
            ns.knob('operation').setValue('over')
t.addCommand('Tools/Merge_op', opSwitcher, 'alt+m')


def pipeSwitcher():
    ns = nuke.selectedNode()
    if ns.Class() == "Merge2":
        if ns.knob('bbox').value() == "union":
            ns.knob("bbox").setValue("A")
        elif ns.knob("bbox").value() == "A":
            ns.knob("bbox").setValue("B")
        elif ns.knob("bbox").value() == "B":
            ns.knob("bbox").setValue("union")
    elif ns.Class() == "Copy":
        if ns.knob('bbox').value() == "union":
            ns.knob("bbox").setValue("A")
        elif ns.knob("bbox").value() == "A":
            ns.knob("bbox").setValue("B")
        elif ns.knob("bbox").value() == "B":
            ns.knob("bbox").setValue("union")

t.addCommand('Tools/Pipe switcher', pipeSwitcher, "alt+b")

#copy premult shortcut ctrl+alt+k

def  kPre_short():

    nc=nuke.nodes.Copy(from0='rgba.alpha', to0='rgba.alpha', label='pipe: [value bbox]')
    nc.setInput(0, nuke.selectedNode())
    nuke.nodes.Premult().setInput(0, nc).hideControlPanel()

nuke.menu('Nodes').addMenu('Channel').addCommand('Create Copy premult', kPre_short, 'ctrl+alt+k', icon='Copy.png')

#roto blur shortcut

#def rotoBlur():
#    nr= nuke.createNode("Roto")
#    nuke.nodes.Blur(size=2, channel='rgba', label="[value size]").setInput(0, nr).hideControlPanel()

#nuke.menu("Nodes").addCommand("Draw/Roto", rotoBlur, "o", icon= "Roto.png")


def enableTrackerTRS():
    if nuke.selectedNode().Class() == 'Tracker4':
        ns = nuke.selectedNodes()
        for i in ns:
            i['tracks'].setValue(True)
    else:
        nuke.message('select Tracker node to enable traslate, rotate, scale')

nuke.menu('Nodes').addMenu('Tools').addCommand('Tools/Enable_TRS', enableTrackerTRS, 'ctrl+shift+t', shortcutContext = 2)


def autoWrite():
    for i in nuke.allNodes():
        if i.Class() == 'Write':
            i['file'].setValue(nuke.root().name().replace("script","renders").replace("nk","exr"))

nuke.knobDefault('write.beforeRender', 'autoWrite()')