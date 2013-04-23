from maya import cmds
import random
import math
import logging

log = logging.getLogger('dk')
log.setLevel(logging.DEBUG)


def pipe(radius, height, name=None):
    t = 1/float(16)  # 16ga
    val = cmds.polyPipe(
        thickness=t, radius=radius, height=height*2, name=name)
    log.debug(val)
    return val


def make_pipe(new_radius, new_height, basename="pipe_000", from_pipe_name=None):
    t = 1/float(16)  # 16ga
    if from_pipe_name:
        ret = cmds.duplicate(from_pipe_name, un=True)
        log.debug(ret)
        new_name = ret[0]
        shape = ret[-1]
    else:
        new_name, shape = cmds.polyPipe(n=basename, t=t)

    log.debug("copied: " + new_name if from_pipe_name else "new: " + new_name)
    cmds.setAttr(shape + '.radius', new_radius)
    cmds.setAttr(shape + '.height', new_height)
    return new_name, shape

# thing = pipe(1, 6)

n_pipes = 3
# n_divisions = 10
vert_xlate = 3

min_piped = 1
max_piped = 3

main_radius = 6
main_c = math.pi * main_radius

rotated_deg = 0
last_pipe_d = 0
last_pipe_name = None

for i in range(1, n_pipes+1):
    p_name = "pipe%d" % i
    pd = 2  # random.choice(range(min_piped, max_piped+1))

    p_name, p_shape = make_pipe(pd, 6.0, from_pipe_name=last_pipe_name, basename=p_name)
    cmds.select(p_name, r=True)
    # translate away from center?
    cmds.xform(t=[0, 0, main_radius], ws=True)
    # reset just the translation context

    cmds.makeIdentity(apply=True, t=0, r=1, s=0, n=0)


    if not i == 1:
        # cmds.xform(t=[3, 0, 0])
        rotate_distance = last_pipe_d/2 + pd/2
        rotate_degrees = (360 * rotate_distance)/main_c

        rotated_deg = rotated_deg + rotate_degrees

        # cmds.rotate(0, rotate_degrees, 0, p=[0, 0, 0])
        log.debug('rotating %s by %d degrees around p [0 0 0] in worldspace' % (p_name, rotate_degrees))
        cmds.rotate(0, rotate_degrees, 0, p_name, p=[0, 0, 0], ws=True)

    # translate vertically
    cmds.xform(t=[0, vert_xlate*i, 0], ws=True)
    # reset just the translation context
    cmds.makeIdentity(apply=True, t=1, r=1, s=0, n=0)

    last_pipe_name = p_name
    last_pipe_d = pd

cmds.DeleteAllHistory()
