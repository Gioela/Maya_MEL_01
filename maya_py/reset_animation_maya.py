import maya.cmds as cmds

def resetAnimation(items):
    #nurbs = cmds.ls('*_ac_*', '*_fk_*', type='nurbsCurve')
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

items = cmds.ls('*_ac_*', '*_fk_*', r=True)
resetAnimation(items)