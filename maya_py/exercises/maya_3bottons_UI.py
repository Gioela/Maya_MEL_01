'''
Script 3) 
	Extend the script that we wrote in class for the zombie rig to also Save the current state of
	the controls and Load the saved states. Write a UI to use all three scripts that we wrote
'''
import maya.cmds as cmds
from os import sep
# import os

GEG_DUPLICATE_NUMBER = 'DUPLICATION_NUMBER'
GEG_ANIMATION_MODEL_PATH = 'ANIMATION_MODEL_PATH'
GEG_ANIMATION_MODEL_NAME = 'ANIMATION_MODEL_NAME'

def gegReplaceCBetweenAB(ObjA, ObjB, ObjC, xNumber):
    bb_x_max_a = cmds.getAttr(ObjA + ".boundingBoxMaxX")
    bb_x_min_a = cmds.getAttr(ObjA + ".boundingBoxMinX")
    obj_width_a = bb_x_max_a - bb_x_min_a

    bb_x_max_b = cmds.getAttr(ObjB + ".boundingBoxMaxX")
    bb_x_min_b = cmds.getAttr(ObjB + ".boundingBoxMinX")
    obj_width_b = bb_x_max_b - bb_x_min_b

    bb_x_max_c = cmds.getAttr(ObjC + ".boundingBoxMaxX")
    bb_x_min_c = cmds.getAttr(ObjC + ".boundingBoxMinX")
    obj_width_c = bb_x_max_c - bb_x_min_c

    pos_a = cmds.getAttr(ObjA + ".translate")[0]
    pos_b = cmds.getAttr(ObjB + ".translate")[0]

    for i in range(xNumber):
        # x = pos_a[0] + obj_width_a + obj_width_c + obj_width_c * i
        x = pos_a[0] + obj_width_a + obj_width_c + (obj_width_c * i)
        cmds.move(x, pos_a[1], pos_a[2], ObjC)
        cmds.duplicate(ObjC, rr=True)

        x = pos_b[0] + obj_width_b + obj_width_c + obj_width_c * i
        cmds.move(x, pos_b[1], pos_b[2], ObjC)
        cmds.duplicate(ObjC, rr=True)

def gegResetAnimation(items):
    nurbs = cmds.ls(items, type='nurbsCurve')
    for nurb in nurbs:
        # cmds.listRelatives TORNA UNA LISTA, impostando il p=True prendo il padre
        # dell'attributo e con l'indice [0] estraggo l'elemento dalla lista
        control = cmds.listRelatives(nurb, p=True)[0]
        attributes = cmds.listAttr(control, keyable=True)
        if attributes is None:
            continue
        for attr in attributes:
            if attr.startswith('translate') or attr.startswith('rotate'):
                cmds.setAttr(f'{control}.{attr}', 0)
            elif attr.startswith('scale'):
                cmds.setAttr(f'{control}.{attr}', 1)
                
        attributes = cmds.listAttr(control, keyable=True, userDefined=True)
        if attributes is None:
            continue
        for attr in attributes:
            # chiede il valore di default dell'attributo custom definito dall'artista
            dv = cmds.addAttr(f'{control}.{attr}', q=True, dv=True)
            # reimposto il valore di default del modello
            cmds.setAttr(f'{control}.{attr}', dv)

def gegMirrorAnimation(selected):
    for element in selected:
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
    
def gegAnimationsUI():
    global GEG_DUPLICATE_NUMBER
    global GEG_ANIMATION_MODEL_PATH
    global GEG_ANIMATION_MODEL_NAME
    
    window = 'AnimationsUI'
    if cmds.window(window, q=True, ex=True):
        cmds.deleteUI(window)
    cmds.window(window, title='Choose Animation Options')
    cmds.columnLayout(adj=True)
    cmds.button(label='Reset Animation', command=geg_reset_anim)
    cmds.button(label='Mirror Animation', command=geg_mirror_anim)
    cmds.text(l='Please, specify folder path where save the animation model')
    cmds.textField(GEG_ANIMATION_MODEL_PATH)
    cmds.text(l='Please, specify name for the animation model')
    cmds.textField(GEG_ANIMATION_MODEL_NAME)
    cmds.button(label='Save Animation', command=geg_save_anim)
    cmds.button(label='Load Animation', command=geg_load_anim)
    cmds.text(l='Please, specify how many time the last of 3 selected objects will be duplicated')
    cmds.textField(GEG_DUPLICATE_NUMBER)
    cmds.button(label='Duplicate', command=geg_duplicate_objs)
    cmds.setParent('..')
    cmds.showWindow(window)

def geg_reset_anim(*args):
    gegResetAnimation(cmds.ls('*_ac_*', '*_fk_*', r=True))

def geg_mirror_anim(*args):
    gegMirrorAnimation(cmds.ls(sl=True, r=True))

def geg_save_anim(*args):
    model_attributes = {}
    nurbs = cmds.ls('*_ac_*', '*_fk_*', r=True, type='nurbsCurve')
    for nurb in nurbs:
        # cmds.listRelatives TORNA UNA LISTA, impostando il p=True prendo il padre
        # dell'attributo e con l'indice [0] estraggo l'elemento dalla lista
        control = cmds.listRelatives(nurb, p=True)[0]
        attributes = cmds.listAttr(control, keyable=True)
        if attributes is None:
            continue
        for attr in attributes:
            model_attributes[f'{control}.{attr}'] = cmds.getAttr(f'{control}.{attr}')

    filePath = geg_get_path()
    with open(filePath, 'w') as f:
        for _ in model_attributes.keys():
            f.writelines(f'{_}:{model_attributes[_]}\n')

def geg_get_path():
    model_path = cmds.textField(GEG_ANIMATION_MODEL_PATH, q=True, tx=True)
    model_name = cmds.textField(GEG_ANIMATION_MODEL_NAME, q=True, tx=True)
    return sep.join([model_path, model_name])

def geg_load_anim(*args):
    filePath = geg_get_path()
    attributes = []
    with open(filePath, 'r') as f:
        attributes = f.readlines()
    print('file attributes readed')
    for attr in attributes:
        attr_name, attr_value = attr.split(':')
        cmds.setAttr(attr_name, float(attr_value))

def geg_duplicate_objs(*args):
    selected = cmds.ls(sl=True)
    duplicate_num = cmds.textField(GEG_DUPLICATE_NUMBER, q=True, tx=True)
    gegReplaceCBetweenAB(selected[0], selected[1], selected[2], int(duplicate_num))

gegAnimationsUI()