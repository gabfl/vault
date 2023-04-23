"""
A module for accessing the Touch ID sensor in your Mac's Touch Bar.

Requires pyobjc to be installed
"""

import sys
import ctypes
from LocalAuthentication import LAContext
from LocalAuthentication import LAPolicyDeviceOwnerAuthenticationWithBiometrics

kTouchIdPolicy = LAPolicyDeviceOwnerAuthenticationWithBiometrics

c = ctypes.cdll.LoadLibrary(None)

PY3 = sys.version_info[0] >= 3
if PY3:
    DISPATCH_TIME_FOREVER = sys.maxsize
else:
    DISPATCH_TIME_FOREVER = sys.maxint

dispatch_semaphore_create = c.dispatch_semaphore_create
dispatch_semaphore_create.restype = ctypes.c_void_p
dispatch_semaphore_create.argtypes = [ctypes.c_int]

dispatch_semaphore_wait = c.dispatch_semaphore_wait
dispatch_semaphore_wait.restype = ctypes.c_long
dispatch_semaphore_wait.argtypes = [ctypes.c_void_p, ctypes.c_uint64]

dispatch_semaphore_signal = c.dispatch_semaphore_signal
dispatch_semaphore_signal.restype = ctypes.c_long
dispatch_semaphore_signal.argtypes = [ctypes.c_void_p]


def is_available():
    context = LAContext.new()
    return context.canEvaluatePolicy_error_(kTouchIdPolicy, None)[0]


def authenticate(reason='authenticate via Touch ID'):
    context = LAContext.new()

    can_evaluate = context.canEvaluatePolicy_error_(kTouchIdPolicy, None)[0]
    if not can_evaluate:
        raise Exception("Touch ID isn't available on this machine")

    sema = dispatch_semaphore_create(0)

    # we can't reassign objects from another scope, but we can modify them
    res = {'success': False, 'error': None}

    def cb(_success, _error):
        res['success'] = _success
        if _error:
            res['error'] = _error.localizedDescription()
        dispatch_semaphore_signal(sema)

    context.evaluatePolicy_localizedReason_reply_(kTouchIdPolicy, reason, cb)
    dispatch_semaphore_wait(sema, DISPATCH_TIME_FOREVER)

    if res['error']:
        raise Exception(res['error'])

    return res['success']