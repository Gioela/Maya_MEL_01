import maya.cmds as cmds

AIV_RENAME_TEXTFIELD_NAME = 'AIV_RENAME_TEXTFIELD_NAME'

def geg_rename_list_objs(items, new_name):
    # items = cmds.ls(sl=True)
    temp_objs = [cmds.rename(item, 'temp') for item in items]
    for i, item in enumerate(temp_objs, 1):
        cmds.rename(item, f'{new_name}{i}')
    
def gegRenameObjsUI():
    global AIV_RENAME_TEXTFIELD_NAME
    
    window = 'RenameUI'
    if cmds.window(window, q=True, ex=True):
        cmds.deleteUI(window)
    cmds.window(window, title='AIV Rename')
    cmds.columnLayout(adj=True)
    cmds.text(l='Please enter the name')
    cmds.textField(AIV_RENAME_TEXTFIELD_NAME)
    cmds.button(label='Rename', command=geg_rename_command)
    cmds.setParent('..')
    cmds.showWindow(window)
    
def geg_rename_command(*args):
    new_name = cmds.textField(AIV_RENAME_TEXTFIELD_NAME, q=True, tx=True)
    geg_rename_list_objs(cmds.ls(sl=True), new_name)
    
gegRenameObjsUI()