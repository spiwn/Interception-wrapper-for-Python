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
    global context
    stroke = Stroke()
    keyStroke = KeyStroke()
    mouseStroke = MouseStroke()
    context = create_context()
    set_filter( context, is_keyboard, FILTER_KEY_DOWN | FILTER_KEY_UP )
    set_filter( context, is_mouse, FILTER_MOUSE_MOVE )
    device = wait( context )
    while ( receive ( context, device, stroke,1)>0 ):
        if is_keyboard( device ):
            stroke2KeyStroke( stroke, dest = keyStroke )
            if keyStroke.code == SCANCODE_ESC:
                break
            send( context, device, stroke, 1 )
        elif is_mouse( device ):
            stroke2MouseStroke( stroke, dest = mouseStroke )
            if not ( mouseStroke.flags & MOUSE_MOVE_ABSOLUTE ):
                mouseStroke.y *= -1
            send( context, device, mouseStroke, 1)
        else:
            send( context, device, stroke, 1 )
        device = wait( context )
    destroy_context( context )

if __name__=='__main__':
    try:
        testInterception()
    except Exception as e:
        print('An Exception occured\n',e)
        destroy_context(context)
        raise e
