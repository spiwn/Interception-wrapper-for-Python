# Python wrappings for
#   Interception by oblitum:
#       http://oblita.com/Interception
#       https://github.com/oblitum/Interception


#           !!!  Attention !!!
#                   WIP
#           Not completely tested

# May not run at all or may cause your system to stop accepting input
# And if you do not use it properly it will definetely do the later

# I am not responsible for any damage that may be caused by the use of
# this incomplete code

from ctypes import *

interceptionDll = cdll.interception

#INTERCEPTION_MAX_KEYBOARD   = 10
#INTERCEPTION_MAX_MOUSE      = 10
#INTERCEPTION_MAX_DEVICE     = INTERCEPTION_MAX_KEYBOARD + INTERCEPTION_MAX_MOUSE
#INTERCEPTION_KEYBOARD       = lambda index: index+1
#INTERCEPTION_MOUSE          = lambda index: INTERCEPTION_MAX_KEYBOARD + index + 1

class Context( c_void_p ):
    pass
class Device( c_int ):
    pass
class Precedence( c_int ):
    pass
class Filter( c_ushort ):
    pass
Predicate = CFUNCTYPE( c_int, c_int )

KEY_DOWN             = 0x00
KEY_UP               = 0x01
KEY_E0               = 0x02
KEY_E1               = 0x04
KEY_TERMSRV_SET_LED  = 0x08
KEY_TERMSRV_SHADOW   = 0x10
KEY_TERMSRV_VKPACKET = 0x20

FILTER_KEY_NONE             = 0x0000
FILTER_KEY_ALL              = 0xFFFF
FILTER_KEY_DOWN             = KEY_UP
FILTER_KEY_UP               = KEY_UP << 1
FILTER_KEY_E0               = KEY_E0 << 1
FILTER_KEY_E1               = KEY_E1 << 1
FILTER_KEY_TERMSRV_SET_LED  = KEY_TERMSRV_SET_LED << 1
FILTER_KEY_TERMSRV_SHADOW   = KEY_TERMSRV_SHADOW << 1
FILTER_KEY_TERMSRV_VKPACKET = KEY_TERMSRV_VKPACKET << 1

MOUSE_LEFT_BUTTON_DOWN   = 0x001
MOUSE_LEFT_BUTTON_UP     = 0x002
MOUSE_RIGHT_BUTTON_DOWN  = 0x004
MOUSE_RIGHT_BUTTON_UP    = 0x008
MOUSE_MIDDLE_BUTTON_DOWN = 0x010
MOUSE_MIDDLE_BUTTON_UP   = 0x020

MOUSE_BUTTON_1_DOWN      = MOUSE_LEFT_BUTTON_DOWN
MOUSE_BUTTON_1_UP        = MOUSE_LEFT_BUTTON_UP
MOUSE_BUTTON_2_DOWN      = MOUSE_RIGHT_BUTTON_DOWN
MOUSE_BUTTON_2_UP        = MOUSE_RIGHT_BUTTON_UP
MOUSE_BUTTON_3_DOWN      = MOUSE_MIDDLE_BUTTON_DOWN
MOUSE_BUTTON_3_UP        = MOUSE_MIDDLE_BUTTON_UP

MOUSE_BUTTON_4_DOWN      = 0x040
MOUSE_BUTTON_4_UP        = 0x080
MOUSE_BUTTON_5_DOWN      = 0x100
MOUSE_BUTTON_5_UP        = 0x200

MOUSE_WHEEL              = 0x400
MOUSE_HWHEEL             = 0x800

FILTER_MOUSE_NONE               = 0x0000
FILTER_MOUSE_ALL                = 0xFFFF

FILTER_MOUSE_LEFT_BUTTON_DOWN   = MOUSE_LEFT_BUTTON_DOWN
FILTER_MOUSE_LEFT_BUTTON_UP     = MOUSE_LEFT_BUTTON_UP
FILTER_MOUSE_RIGHT_BUTTON_DOWN  = MOUSE_RIGHT_BUTTON_DOWN
FILTER_MOUSE_RIGHT_BUTTON_UP    = MOUSE_RIGHT_BUTTON_UP
FILTER_MOUSE_MIDDLE_BUTTON_DOWN = MOUSE_MIDDLE_BUTTON_DOWN
FILTER_MOUSE_MIDDLE_BUTTON_UP   = MOUSE_MIDDLE_BUTTON_UP

FILTER_MOUSE_BUTTON_1_DOWN      = MOUSE_BUTTON_1_DOWN
FILTER_MOUSE_BUTTON_1_UP        = MOUSE_BUTTON_1_UP
FILTER_MOUSE_BUTTON_2_DOWN      = MOUSE_BUTTON_2_DOWN
FILTER_MOUSE_BUTTON_2_UP        = MOUSE_BUTTON_2_UP
FILTER_MOUSE_BUTTON_3_DOWN      = MOUSE_BUTTON_3_DOWN
FILTER_MOUSE_BUTTON_3_UP        = MOUSE_BUTTON_3_UP

FILTER_MOUSE_BUTTON_4_DOWN      = MOUSE_BUTTON_4_DOWN
FILTER_MOUSE_BUTTON_4_UP        = MOUSE_BUTTON_4_UP
FILTER_MOUSE_BUTTON_5_DOWN      = MOUSE_BUTTON_5_DOWN
FILTER_MOUSE_BUTTON_5_UP        = MOUSE_BUTTON_5_UP

FILTER_MOUSE_WHEEL              = MOUSE_WHEEL
FILTER_MOUSE_HWHEEL             = MOUSE_HWHEEL

FILTER_MOUSE_MOVE               = 0x1000

MOUSE_MOVE_RELATIVE      = 0x000
MOUSE_MOVE_ABSOLUTE      = 0x001
MOUSE_VIRTUAL_DESKTOP    = 0x002
MOUSE_ATTRIBUTES_CHANGED = 0x004
MOUSE_MOVE_NOCOALESCE    = 0x008
MOUSE_TERMSRV_SRC_SHADOW = 0x100

class MouseStroke( Structure ):
    _fields_ = [
        ( "state", c_ushort ),
        ( "flags",     c_ushort ),
        ( "rolling",     c_short ),
        ( "x",  c_int ),
        ( "y",  c_int ),
        ( "information", c_uint )
    ]

class KeyStroke( Structure ):
    _fields_ = [
        ( "code", c_ushort ),
        ( "state",     c_ushort ),
        ( "information",     c_uint )
    ]
def stroke2KeyStroke( stroke, dest = None ):
    if not dest:
        result = KeyStroke()
        memmove( byref( result ), byref( stroke ), sizeof( result ) )
        return result
    else:
        return memmove( byref( dest ), byref( stroke ), sizeof( KeyStroke ))

def stroke2MouseStroke( stroke, dest = None ):
    if not dest:
        result = MouseStroke()
        memmove( byref( result ), byref( stroke ), sizeof( KeyStroke ) )
        return result
    else:
        return memmove( byref( dest ), byref( stroke ), sizeof( result ) )

Stroke = c_ushort * sizeof ( MouseStroke )

create_context              = interceptionDll.interception_create_context
create_context.argtypes     = []
create_context.restype      = Context

destroy_context             = interceptionDll.interception_destroy_context
destroy_context.argtypes    = [Context]
destroy_context.restype     = c_void_p

get_precedence              = interceptionDll.interception_get_precedence
get_precedence.argtypes     = [Context, Device]
get_precedence.restype      = Precedence

set_precedence              = interceptionDll.interception_set_precedence
set_precedence.argtypes     = [Context, Device, Precedence]
set_precedence.restype      = c_void_p

get_filter                  = interceptionDll.interception_get_filter
get_filter.argtypes         = [Context, Device]
get_filter.restype          = Filter

set_filter                  = interceptionDll.interception_set_filter
set_filter.argtypes         = [Context, Predicate, Filter]
set_filter.restype          = c_void_p

wait                        = interceptionDll.interception_wait
wait.argtypes               = [Context]
wait.restype                = Device

wait_with_timeout           = interceptionDll.interception_wait_with_timeout
wait_with_timeout           = [Context, c_ulong]
wait_with_timeout           = Device

send_proto                  = interceptionDll.interception_send
send_proto.argtypes         = [Context, Device, Stroke, c_uint]
send_proto.restype          = c_int

__temp_Stroke = Stroke()
def send( con, dev, stroke, nstroke ):
    if isinstance( stroke, Stroke ):
        return send_proto( con, dev, stroke, nstroke)
    if isinstance( stroke, KeyStroke ) or isinstance( stroke, MouseStroke ):
        memmove( byref( __temp_Stroke ), byref( stroke ), sizeof( stroke ))
        return send_proto( con, dev, __temp_Stroke, nstroke )
    raise TypeError( "Argument 3. Expected <'Stroke'>, <'KeyStroke'> or <'MouseStroke'>, got {0} instead.".format( type( stroke ) ) )

receive                     = interceptionDll.interception_receive
receive.argtypes            = [Context, Device, Stroke, c_uint]
receive.restype             = c_int

get_hardware_id             = interceptionDll.interception_get_hardware_id
get_hardware_id.argtypes    = [Context, Device, c_void_p, c_uint]
get_hardware_id.restype     = c_uint

is_invalid                  = Predicate(interceptionDll.interception_is_invalid)

is_keyboard                 = Predicate( interceptionDll.interception_is_keyboard)

is_mouse                    = Predicate(interceptionDll.interception_is_mouse)