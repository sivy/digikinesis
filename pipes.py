from maya import cmds
import random
import math


def pipe(radius, height, name=None):
    t = 1/float(16)  # 16ga
    val = cmds.polyPipe(
        thickness=t, radius=radius, height=height*2, name=name)
    print val
    return val


def copy_pipe(new_radius, new_height, from_pipe=None, name=None):
    if pipe:
        cmds.duplicate(pipe[0], rr=True)
    else:
        cmds.polyPipe(name=name)
    val = cmds.polyPipe(
        e=True, radius=new_radius, height=new_height*2, name=name)
    print val
    return val

# thing = pipe(1, 6)

n_pipes = 20
n_divisions = 10
vert_xlate = 3

min_piped = 1
max_piped = 3

main_radius = 6
main_c = math.pi * main_radius

rotated_deg = 0
last_pipe_d = 0

for i in range(1, n_pipes):
    n = "p%d" % i
    pd = random.choice(range(min_piped, max_piped+1))
    p = pipe(pd, 6.0, name=n)
    cmds.select(p[0], r=True)
    # translate away from center?
    cmds.xform(t=[main_radius, 0, 0], ws=True)
    # reset just the translation context
    cmds.makeIdentity(apply=True, t=1, r=1, s=0, n=0)

    # cmds.xform(t=[3, 0, 0])
    rotate_degrees = (360 * pd)/main_c
    rotated_deg = rotated_deg + rotate_degrees

    cmds.rotate(0, rotate_degrees, 0, p=[0, 0, 0])

    # translate vertically
    cmds.xform(t=[0, vert_xlate*i, 0], ws=True)
    # reset just the translation context
    cmds.makeIdentity(apply=True, t=1, r=0, s=0, n=0)

    cmds.DeleteHistory()
