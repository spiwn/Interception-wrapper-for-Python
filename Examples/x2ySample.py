#
#
# A 'safe' python implementation of
# the Interception ( https://github.com/oblitum/Interception )
# example x2y ( https://github.com/oblitum/Interception/tree/master/samples/x2y )
#
# Once running, it will turn your 'X' key into an 'Y' key
# Press Escape to terminate

import changePriority # https://gist.github.com/1876666
from interception import *

changePriority.IncreasePriority( times = 2 )

SCANCODE_X      = 0x2D
SCANCODE_Y      = 0x15
SCANCODE_ESC    = 0x01

def testInterception():
    global context
    stroke = Stroke()
    context = create_context()
    set_filter( context, is_keyboard, FILTER_KEY_ALL)
    device = wait( context )
    keyStroke = KeyStroke()
    while ( receive ( context, device, stroke,1)>0 ):
        if is_keyboard( device ):
            stroke2KeyStroke( stroke, dest = keyStroke )
            if keyStroke.code == SCANCODE_ESC:
                break

            # if 'x' is pressed/released - turn it to 'y'
            if keyStroke.code == SCANCODE_X: keyStroke.code = SCANCODE_Y

            #uncomment the next line to also turn 'y's in to 'x's
            #elif keyStroke.code == SCANCODE_Y: keyStroke.code = SCANCODE_X

            send(context,device, keyStroke,1)
        else:
            send(context,device, stroke,1)
        device=wait(context)
    destroy_context(context)

if __name__=='__main__':
    try:
        testInterception()
    except Exception as e:
        print('An Exception occured\n',e)
        destroy_context(context)
        raise e
