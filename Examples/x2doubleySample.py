#
#
# A 'safe' python implementation of an example usage of
# Interception ( https://github.com/oblitum/Interception )
# 
#
# Once running, it will turn your 'X' key into a double 'Y'
# Press Escape to terminate
#

import changePriority # https://gist.github.com/1876666
import interception

changePriority.IncreasePriority( times = 2 )

SCANCODE_X      = 0x2D
SCANCODE_Y      = 0x15
SCANCODE_ESC    = 0x01

def testInterception():
    with interception.Context(3) as context:
        context.set_filter( interception.is_keyboard, interception.FILTER_KEY_DOWN | interception.FILTER_KEY_UP )
        while ( context.wait() > 0 ):
            if context.stroke[0].code == SCANCODE_ESC:
                break
            nStroke = 1

            if context.stroke[0].code == SCANCODE_X:
                if context.stroke[0].state == interception.KEY_UP:
                    context.stroke[0].code = SCANCODE_Y
                    context.stroke[0].state = interception.KEY_DOWN
                    context.stroke[1].code = SCANCODE_Y
                    context.stroke[1].state = interception.KEY_UP
                else:
                    context.stroke[0].code = SCANCODE_Y
                    context.stroke[1].code = SCANCODE_X
                    context.stroke[1].state = interception.KEY_UP
                nStroke = 2

            context.send( context.device, context.stroke, nStroke )

if __name__=='__main__':
    testInterception()
