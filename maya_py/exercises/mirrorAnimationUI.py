'''
Script 2) 
	Write a script that will work with the zombie rig and based on selected ctrls
	make the other side symmetrical (so that both sides look the same). 
	The minimum for this assignments should be a proc that will take whatever 
	is selected and mirror the attribute values to the other side.
	Write a little UI around it that lets the user specify if they want to mirror
	or if they want to switch (so that the right will be like left and left will be like right).
'''
import maya.cmds as cmds

def mirrorAnimation(selected):
    for element in selected:
        # attribute_name = attributes.split('_')
        attribute_name = '_'.join([ 'lf' if attr_word == 'rt' else 'rt' if attr_word == 'lf' else attr_word 
                                        for attr_word in element.split('_') ])
        attributes = cmds.listAttr(attribute_name, keyable=True)
        if attributes is None:
            continue
        for attr in attributes:
            if attr.startswith('translate'):
                cmds.setAttr(f'{attribute_name}.{attr}', -cmds.getAttr(f'{element}.{attr}'))
            if attr.startswith('rotate'):
                cmds.setAttr(f'{attribute_name}.{attr}', cmds.getAttr(f'{element}.{attr}'))
            elif attr.startswith('scale'):
                cmds.setAttr(f'{attribute_name}.{attr}', 1)
                
        attributes = cmds.listAttr(element, keyable=True, userDefined=True)
        if attributes is None:
            continue
        for attr in attributes:
            # chiede il valore di default dell'attributo custom definito dall'artista
            dv = cmds.addAttr(f'{element}.{attr}', q=True, dv=True)
            # reimposto il valore di default del modello
            cmds.setAttr(f'{element}.{attr}', dv)

def gegMirrorAnimationsUI():
    global GEG_DUPLICATE_NUMBER
    
    window = 'MirrorAnimationUI'
    if cmds.window(window, q=True, ex=True):
        cmds.deleteUI(window)
    cmds.window(window, title='Mirror Animation UI')
    cmds.columnLayout(adj=True)
    cmds.button(label='Mirror Animation', command=geg_mirror_anim)
    cmds.button(label='Reset Animation', command=geg_mirror_anim)
    cmds.setParent('..')
    cmds.showWindow(window)


def geg_mirror_anim(*args):
    mirrorAnimation(cmds.ls(sl=True, r=True))

gegMirrorAnimationsUI()

# selection = cmds.ls(sl=True)
# mirrorAnimation(selection)

        