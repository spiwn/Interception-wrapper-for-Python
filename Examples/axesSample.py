#
#
# A 'safe' python implementation of
# the Interception ( https://github.com/oblitum/Interception )
# example axes ( https://github.com/oblitum/Interception/tree/master/samples/axes )
#
# Once running, it will invert the y axes of your mouse ( mice )
# Press Escape to terminate

import changePriority # https://gist.github.com/1876666
import interception

changePriority.IncreasePriority( times = 2 )

SCANCODE_ESC    = 0x01

def testInterception():
    with interception.Context() as context:
        context.set_filter( interception.is_keyboard, interception.FILTER_KEY_DOWN | interception.FILTER_KEY_UP )
        context.set_filter( interception.is_mouse, interception.FILTER_MOUSE_MOVE )
        while ( context.wait() > 0 ):
            if interception.is_keyboard( context.device ):
                if context.stroke.code == SCANCODE_ESC:
                    break
            elif interception.is_mouse( context.device ):
                if not ( context.stroke.flags & interception.MOUSE_MOVE_ABSOLUTE ):
                    context.stroke.y *= -1
            context.send( context.device, context.stroke)
            
if __name__=='__main__':
    testInterception()
