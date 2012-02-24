#
#
# A 'safe' python implementation of
# the Interception ( https://github.com/oblitum/Interception )
# example x2y ( https://github.com/oblitum/Interception/tree/master/samples/x2y )
#
# Once running, it will turn your 'X' key into an 'Y' key
# Press Escape to terminate

import changePriority # https://gist.github.com/1876666
import interception

changePriority.IncreasePriority( times = 2 )

SCANCODE_X      = 0x2D
SCANCODE_Y      = 0x15
SCANCODE_ESC    = 0x01

def testInterception():
    with interception.Context() as context:
        context.set_filter( interception.is_keyboard, interception.FILTER_KEY_DOWN | interception.FILTER_KEY_UP )
        while ( context.wait() > 0 ):
            if context.stroke.code == SCANCODE_ESC:
                break
            # if 'x' is pressed/released - turn it to 'y'
            if context.stroke.code == SCANCODE_X: context.stroke.code = SCANCODE_Y
            
            #uncomment the next line to also turn 'y's in to 'x's
            #elif context.stroke.code == SCANCODE_Y: context.stroke.code = SCANCODE_X

            context.send( context.device, context.stroke )

if __name__=='__main__':
    testInterception()
