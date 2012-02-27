#
#
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
from ctypes import _CFuncPtr

interceptionDll = cdll.interception

#
# Exposing(emulating) Interception's functions, types and constants
# ( note, the "interception_" prefix that all the identifiers had is obsolete as when you import this module
#   you would access the fields either with "interception." (or you will know what your are doing) )
#

MAX_KEYBOARD   = 10
MAX_MOUSE      = 10
MAX_DEVICE     = MAX_KEYBOARD + MAX_MOUSE
KEYBOARD       = lambda index: index+1
MOUSE          = lambda index: MAX_KEYBOARD + index + 1

class ContextType( c_void_p ):
    pass
class Device( c_int ):
    pass
class Precedence( c_int ):
    pass
class Filter( c_ushort ):
    pass

PredicateCache = {}

class PredicateType():
    def __init__( self, func ):
        if isinstance(func, _CFuncPtr):
            self._as_parameter_ = func
            self._as_parameter_.argtypes = [ c_int ]
            self._as_parameter_.restype = c_bool
        elif callable( func ):
            self._as_parameter_ = CFUNCTYPE( c_bool, c_int )( func )
        else:
            raise TypeError
    def from_param( self ):
        return self._as_parameter_
    def __call__( self, device ):
        return self._as_parameter_( device )

def Predicate ( func ):
    if isinstance( func, _CFuncPtr ):
        hashValue = id( func )
    elif callable( func ):
        hashValue = id( func )
    else:
        raise TypeError("Wrong type for a Predicate ( should be something like a function")
    predFunc = PredicateCache.get( hashValue , False )
    if not predFunc:
        predFunc = PredicateType( func )
        PredicateCache [ hashValue ] = predFunc
    return predFunc


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

strokeValueMap = { 'state' : ( 0, ( -1, 0, 0 ), ( 0, 1, 0 ), ),
                   'information' : ( 0, ( 7, 9, 0 ), ( 1, 3, 0 ) ),
                   'code' : ( 0, 0, ( -1, 0, 0 ) ),
                   'flags': ( 0, ( 0, 1, 0 ), 0 ),
                   'rolling': ( 0, ( 1, 2, 1 ), 0 ),
                   'x': ( 0, ( 3, 5, 1 ), 0 ),
                   'y': ( 0, ( 5, 7, 1 ), 0 ) }

unsignedHelper1 = [0,2**16,2**32]
unsignedHelper2 = [0,2**15,2**31]

class Stroke():
    MouseStroke = 1
    KeyStroke = 2
    undefined = 0
    def __init__( self, initial = None ):
        if initial:
            self._as_parameter_ = ( c_ushort * 10 ) (*initial)
        else:
            self._as_parameter_ = ( c_ushort * 10 ) ()
        self.typ = Stroke.undefined
        
    def from_param( self ):
        return self._as_parameter_

    def __getitem__( self, index):
        return self._as_parameter_[ index ]

    def __setitem__( self, index, value):
        self._as_parameter_[ index ] = value
    
    def settype( self, typ ):
        if not isinstance( typ, int ):
            raise TypeError
        if not 0 <= typ <= 2:
            raise ValueError
        self.typ = typ
        
    def __getattr__( self, key ):
        span = strokeValueMap.get( key, 0 )
        if span:
            if not self.typ:
                raise AttributeError
            span = span[ self.typ ]
            result = 0
            for i in range( span[ 1 ], span[ 0 ], -1 ):
                result = ( result << 16 ) + self._as_parameter_[ i ]
            if span[ 2 ] and result > unsignedHelper2[ span[ 1 ] - span[ 0 ] ]:
                result = result - unsignedHelper1[ span[ 1 ] - span[ 0 ] ]
                pass
            return result
        else:
            raise AttributeError

    def __setattr__( self, key, value ):
        span = strokeValueMap.get( key, 0 )
        if span:
            if not self.typ:
                raise AttributeError
            span = span[ self.typ ]
            if span[ 2 ] and value < 0:
                value = unsignedHelper1[ span[ 1 ] - span [ 0 ] ] + value
            for i in range( span[ 0 ] + 1, span[ 1 ] + 1 ):
                self._as_parameter_[ i ] = value & 65535
                value = value >> 16
            if value > 0:
                raise ValueError
        else:
            return super().__setattr__( key, value )

create_context          = interceptionDll.interception_create_context
create_context.argtypes = []
create_context.restype  = ContextType

destroy_context         = interceptionDll.interception_destroy_context
destroy_context.argtypes= [ ContextType ]
destroy_context.restype = c_void_p

get_precedence          = interceptionDll.interception_get_precedence
get_precedence.argtypes = [ ContextType, Device ]
get_precedence.restype  = Precedence

set_precedence          = interceptionDll.interception_set_precedence
set_precedence.argtypes = [ ContextType, Device, Precedence ]
set_precedence.restype  = c_void_p

get_filter              = interceptionDll.interception_get_filter
get_filter.argtypes     = [ ContextType, Device ]
get_filter.restype      = Filter

set_filter_proto              = interceptionDll.interception_set_filter
set_filter_proto.argtypes     = [ ContextType, PredicateType, Filter ]
set_filter_proto.restype      = c_void_p

wait                    = interceptionDll.interception_wait
wait.argtypes           = [ ContextType ]
wait.restype            = Device

wait_with_timeout       = interceptionDll.interception_wait_with_timeout
wait_with_timeout       = [ ContextType, c_ulong ]
wait_with_timeout       = Device

send              = interceptionDll.interception_send
send.argtypes     = [ ContextType, Device, Stroke, c_uint ]
send.restype      = c_int

receive                 = interceptionDll.interception_receive
receive.argtypes        = [ ContextType, Device, Stroke, c_uint ]
receive.restype         = c_int

get_hardware_id           = interceptionDll.interception_get_hardware_id
get_hardware_id.argtypes  = [ ContextType, Device, c_void_p, c_uint ]
get_hardware_id.restype   = c_uint

is_invalid      = Predicate( interceptionDll.interception_is_invalid )

is_keyboard     = Predicate( interceptionDll.interception_is_keyboard )

is_mouse        = Predicate( interceptionDll.interception_is_mouse )

#-------------------------------------------------------------------------

def memoryChunk2Strings( string, lenght = 0 ):
    if lenght:
        limit = lenght
    else:
        limit = sizeof( string )
    result = []
    offset = 0
    while offset < limit:
        part = wstring_at( addressof( string ) + offset * 2 )
        if part:
            result.append( part )
            offset += len( part )+1
        else:
            break
    return result

hardware_Id_Data = [ create_unicode_buffer( 300 ), 300 ]

class Context():
    def __enter__(self):
        self.context = create_context()
        self.stroke = Stroke()
        return self
        
    def __exit__( self, *exc ):
        destroy_context( self.context )

    def set_filter( self, predicate, filt ):
        if isinstance( predicate, PredicateType ):
            return set_filter_proto( self.context, predicate, filt )
        else:
            return set_filter_proto( self.context, Predicate( predicate ), filt )

    def get_filter( self, device ):
        return get_filter( self.context, device )

    def wait( self, timeout = 0 ):
        if timeout:
            self.device = wait_with_timeout( self.condext, timeout )
        else:
            self.device = wait( self.context )
        result = receive( self.context, self.device, self.stroke, 1 )
        if is_keyboard( self.device ):
            self.stroke.settype( self.stroke.KeyStroke )
        elif is_mouse( self.device ):
            self.stroke.settype( self.stroke.MouseStroke )
        return result

    def send( self, device, stroke, nStroke = 1 ):
        return send( self.context, device, stroke, nStroke )

    def set_precedence( self, device, precedence):
        return set_precedence( self.context, device, precedence )

    def get_precedence( self, device):
        return get_precedence( self.context, device )

    def get_hardware_id ( self, device, max_size = 0):
        if max_size > hardware_Id_Data[ 1 ]:
            hardware_Id_Data[ 1 ] = max_size
            hardware_Id_Data[ 0 ] = create_unicode_buffer( max_size )
        lenght = get_hardware_id( self.context, device, hardware_Id_Data[ 0 ], hardware_Id_Data[ 1 ] )
        if lenght > 0:
            return memoryChunk2Strings( hardware_Id_Data[ 0 ], lenght)
        return None
