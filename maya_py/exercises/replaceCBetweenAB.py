'''
Script 1) 
	Write a procedure that has 4 arguments: 3 strings (objA, objB, objC) and 1 int x_number
	when running the proc, objC should get duplicated x_number of times
	and be distributed evenly in a line between objA and objB.
'''
import maya.cmds as cmds

def replaceCBetweenAB(ObjA, ObjB, ObjC, xNumber):
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

        # rot_x = random.randint(-15, 15)
        # if i % 2:
        #     rot_x += 90
        # cmds.rotate(rot_x, 0, 0, dup, r=True, os=True, fo=True)
