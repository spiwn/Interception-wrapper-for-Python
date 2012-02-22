#
#
# A 'safe' python implementation of
# the Interception ( https://github.com/oblitum/Interception )
# example cadstop ( https://github.com/oblitum/Interception/tree/master/samples/cadstop )
#
# Once running, it will intercept the Ctrl + Alt + Del combination ( it stop it )
# Instead when the combination of keys is pressed it will output a notification to the default output stream
# Press Escape to terminate

import changePriority # https://gist.github.com/1876666
from interception import *

changePriority.IncreasePriority( times = 2 )

SCANCODE_CTRL   = 29
SCANCODE_ALT    = 56
SCANCODE_DEL    = 83
SCANCODE_ESC    = 1

NormalKeys      = [ 0 ] * 255
ExtendedKeys    = [ 0 ] * 255

ExtendedKeyDown  = KEY_DOWN | KEY_E0

KeysToLookFor    = ( SCANCODE_CTRL, SCANCODE_ALT, SCANCODE_DEL )

def testInterception():
    global context
    stroke          = Stroke()
    keyStroke       = KeyStroke()
    context         = create_context()
    set_filter( context, is_keyboard, FILTER_KEY_ALL )
    device          = wait( context )
    while ( receive ( context, device, stroke,1)>0 ):
        if is_keyboard( device ):
            stroke2KeyStroke( stroke, keyStroke )
            if keyStroke.code == SCANCODE_ESC:
                break
            if keyStroke.code in KeysToLookFor:
                if keyStroke.state >= KEY_E0:
                    ExtendedKeys[ keyStroke.code ]  = ( keyStroke.state == ExtendedKeyDown )
                else:
                    NormalKeys  [ keyStroke.code ]  = ( keyStroke.state == KEY_DOWN )
            if all( (NormalKeys[i] or ExtendedKeys[i]) for i in KeysToLookFor):
                print("Ctrl + Alt + Del")
            else:
                send(context,device,stroke,1)
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
