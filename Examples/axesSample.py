#
#
# A 'safe' python implementation of
# the Interception ( https://github.com/oblitum/Interception )
# example axes ( https://github.com/oblitum/Interception/tree/master/samples/axes )
#
# Once running, it will invert the y axes of your mouse ( mice )
# Press Escape to terminate

import changePriority # https://gist.github.com/1876666
from interception import *

changePriority.IncreasePriority( times = 2 )

SCANCODE_ESC    = 0x01

def testInterception():
    keyStroke = KeyStroke()
    mouseStroke = MouseStroke()

    with Context() as context:
        context.set_filter( is_keyboard, FILTER_KEY_DOWN | FILTER_KEY_UP )
        context.set_filter( is_mouse, FILTER_MOUSE_MOVE )
        while ( context.wait() > 0 ):
            if is_keyboard( context.device ):
                stroke2KeyStroke( context.stroke, dest = keyStroke )
                if keyStroke.code == SCANCODE_ESC:
                    break
                context.send( context.device, stroke)
            elif is_mouse( context.device ):
                stroke2MouseStroke( context.stroke, dest = mouseStroke )
                if not ( mouseStroke.flags & MOUSE_MOVE_ABSOLUTE ):
                    mouseStroke.y *= -1
                context.send( context.device, mouseStroke)
            else:
                send( context, device, stroke, 1 )
if __name__=='__main__':
    testInterception()
