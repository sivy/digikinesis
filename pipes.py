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
    cmds.setAttr(shape + '.height', new_height*2)
    return new_name, shape


def make_art(n_pipes=8,
             min_pipeh=4.0, max_pipeh=10.0,
             min_vert_overlap=3.0, max_vert_overlap=5.0,
             min_piped=1.0, max_piped=2.0,
             main_radius=3):

    last_pipe_d = 0
    last_pipe_name = None

    for i in range(1, n_pipes+1):
        p_name = "pipe%d" % i
        pd = random.choice(range(min_piped, max_piped+1))

        pipe_h = random.randrange(min_pipeh, max_pipeh)

        p_name, p_shape = make_pipe(pd, pipe_h, from_pipe_name=last_pipe_name, basename=p_name)
        cmds.select(p_name, r=True)
        # translate away from center?
        cmds.xform(t=[0, 0, main_radius], ws=True)
        # reset just the translation context

        cmds.makeIdentity(apply=True, t=0, r=1, s=0, n=0)

        if not i == 1:
            # cmds.xform(t=[3, 0, 0])

            # http://www.mathsisfun.com/algebra/trig-finding-angle-right-triangle.html
            # sin(x) = opposite/hypotenuse, x = sin-1(O/H)
            # python's inverse sin is math.asin
            last_pipe_rads = math.asin(last_pipe_d/float(main_radius))
            # http://www.mathwarehouse.com/trigonometry/radians/convert-degee-to-radians.php
            last_pipe_degs = last_pipe_rads * 180.0/math.pi  # convert radians to degrees

            log.debug("last_pipe_degs: %d" % last_pipe_degs)

            pipe_rads = math.asin(pd/float(main_radius))
            pipe_degs = pipe_rads * 180.0/math.pi  # convert radians to degrees
            log.debug("pipe_degs: %d" % pipe_degs)

            # total rotation is the last pipe's radius in degrees, plus
            # the current pipe's radius in degrees
            rotate_degrees = last_pipe_degs + pipe_degs

            # rotated_deg = rotated_deg + rotate_degrees

            # cmds.rotate(0, rotate_degrees, 0, p=[0, 0, 0])
            log.debug('rotating %s by %d degrees around p [0 0 0] in worldspace' % (p_name, rotate_degrees))
            cmds.rotate(0,                # x
                        rotate_degrees,   # y
                        0,                # z
                        p_name,           # name of object
                        pivot=[0, 0, 0],  # pivot
                        worldSpace=True)  # corrds are in worldspace, not objectspace

        # translate vertically
        cmds.xform(translation=[0, min_vert_overlap*i, 0],
                   relative=True,
                   objectSpace=True)
        # reset just the translation context
        # cmds.makeIdentity(apply=True, t=1, r=1, s=0, n=0)

        last_pipe_name = p_name
        last_pipe_d = pd

    cmds.DeleteAllHistory()

make_art()
