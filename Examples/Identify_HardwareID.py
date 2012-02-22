#
#
# A 'safe' python implementation of
# the Interception ( https://github.com/oblitum/Interception )
# example identify ( https://github.com/oblitum/Interception/tree/master/samples/identify )
#
# Once running, at imput from keypresses/releases or clicking mouse button one,
# it will output the id (internal to Interception) of originating device
# as well as its hardware ID
# Press Escape to terminate

import changePriority # https://gist.github.com/1876666
from interception import *

changePriority.IncreasePriority( times = 2 )

SCANCODE_ESC    = 0x01

def testInterception():
    global context
    stroke = Stroke()
    keyStroke = KeyStroke()
    context = create_context()
    set_filter( context, is_keyboard, FILTER_KEY_DOWN | FILTER_KEY_UP )
    set_filter( context, is_mouse, FILTER_MOUSE_LEFT_BUTTON_DOWN )
    device = wait( context )
    while ( receive ( context, device, stroke,1)>0 ):
        if is_keyboard( device ):
            stroke2KeyStroke( stroke, dest = keyStroke )
            print( "K", device.value - KEYBOARD( 0 ) )
            print( get_hardware_id( context, device ) )
            if keyStroke.code == SCANCODE_ESC:
                break
            send( context, device, stroke, 1 )
        else:
            if is_mouse( device ):
                print( "M", device.value - MOUSE( 0 ) )
                print( get_hardware_id( context, device ) )
            send( context, device, stroke, 1)
        device = wait( context )
    destroy_context( context )

if __name__=='__main__':
    try:
        testInterception()
    except Exception as e:
        print('An Exception occured\n',e)
        destroy_context(context)
        raise e
