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
import interception

changePriority.IncreasePriority( times = 2 )

SCANCODE_ESC    = 0x01

def testInterception():
    with interception.Context() as context:
        context.set_filter( interception.is_keyboard, interception.FILTER_KEY_DOWN | interception.FILTER_KEY_UP )
        context.set_filter( interception.is_mouse, interception.FILTER_MOUSE_LEFT_BUTTON_DOWN )
        while ( context.wait() > 0 ):
            if interception.is_keyboard( context.device ):
                print( "K", context.device.value - interception.KEYBOARD( 0 ) )
                if context.stroke.code == SCANCODE_ESC:
                    break
            else:
                if interception.is_mouse( context.device ):
                    print( "M", context.device.value - interception.MOUSE( 0 ) )
            print( context.get_hardware_id( context.device ))
            context.send( context.device, context.stroke)

if __name__=='__main__':
    testInterception()
