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
import interception

changePriority.IncreasePriority( times = 2 )

SCANCODE_CTRL   = 29
SCANCODE_ALT    = 56
SCANCODE_DEL    = 83
SCANCODE_ESC    = 1

NormalKeys      = [ 0 ] * 255
ExtendedKeys    = [ 0 ] * 255

ExtendedKeyDown  = interception.KEY_DOWN | interception.KEY_E0

KeysToLookFor    = ( SCANCODE_CTRL, SCANCODE_ALT, SCANCODE_DEL )

def testInterception():
    with interception.Context() as context:
        context.set_filter( interception.is_keyboard, interception.FILTER_KEY_ALL )
        while ( context.wait() > 0 ):
            if interception.is_keyboard( context.device ):
                if context.stroke.code == SCANCODE_ESC:
                    break
                if context.stroke.code in KeysToLookFor:
                    if context.stroke.state >= interception.KEY_E0:
                        ExtendedKeys[ context.stroke.code ]  = ( context.stroke.state == ExtendedKeyDown )
                    else:
                        NormalKeys  [ context.stroke.code ]  = ( context.stroke.state == interception.KEY_DOWN )
                if all( (NormalKeys[i] or ExtendedKeys[i]) for i in KeysToLookFor):
                    print("Ctrl + Alt + Del")
                    continue
            context.send( context.device, context.stroke)

if __name__=='__main__':
    testInterception()
