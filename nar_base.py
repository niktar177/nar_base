import random
from nar_error import nar_error
_DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
_HEX_DIGITS = "0123456789ABCDEF"

def nar_to10(a, base):
    if isinstance(a, int):
        a = str(a)
    
    if base <= 36:
        a = a.upper()
    
    result = 0
    for char in a:
        try:
            digit_value = _DIGITS.index(char)
        except ValueError:
            nar_error(1)
        
        if digit_value >= base:
            nar_error(2)
        
        result = result * base + digit_value
    
    return result

def nar_from10(a, base, L=None):
    if a == 0:
        result = "0"
    else:
        result = ""
        num = a
        while num > 0:
            result = _DIGITS[num % base] + result
            num //= base
    
    if L is not None:
        if len(result) > L:
            nar_error(7)
        result = result.zfill(L)
    
    return result

def nar_conv(code, base1=2, base2=10, L=None):
    dec = nar_to10(code, base1)
    return nar_from10(dec, base2, L)

def nar_add(a, b, base):
    dec_a = nar_to10(a, base)
    dec_b = nar_to10(b, base)
    result = dec_a + dec_b
    return nar_from10(result, base)

def nar_sub(a, b, base):
    dec_a = nar_to10(a, base)
    dec_b = nar_to10(b, base)
    result = dec_a - dec_b
    
    if result < 0:
        nar_error(4)
    
    return nar_from10(result, base)

def nar_mul(a, b, base):
    dec_a = nar_to10(a, base)
    dec_b = nar_to10(b, base)
    result = dec_a * dec_b
    return nar_from10(result, base)

def nar_div(a, b, base, rem=False):
    dec_a = nar_to10(a, base)
    dec_b = nar_to10(b, base)
    
    if dec_b == 0:
        nar_error(3)
    
    q = dec_a // dec_b
    r = dec_a % dec_b
    
    q_res = nar_from10(q, base)
    r_res = nar_from10(r, base)
    
    if rem:
        return (q_res, r_res)
    else:
        return q_res

def nar_pow(a, exp, base, L=None):
    dec_a = nar_to10(a, base)
    result = dec_a ** exp
    return nar_from10(result, base, L)

def _mix(ch1, ch2, op, prop):
    w1 = prop / 100.0
    w2 = (100 - prop) / 100.0
    
    if op == 'add':
        val = int(round(ch1 * w1 + ch2 * w2))
        return min(val, 255)
    elif op == 'sub':
        val = int(round(ch1 * w1 - ch2 * w2))
        return max(val, 0)
    else:
        nar_error(5)

def nar_hex(c1, c2, op='add', prop=50):
    if len(c1) != 6 or len(c2) != 6:
        nar_error(7)
    
    for ch in c1.upper():
        if ch not in _HEX_DIGITS:
            nar_error(1)
    for ch in c2.upper():
        if ch not in _HEX_DIGITS:
            nar_error(1)
    
    if not 0 <= prop <= 100:
        nar_error(6)
    
    c1 = c1.upper()
    c2 = c2.upper()
    
    r1 = nar_to10(c1[0:2], 16)
    g1 = nar_to10(c1[2:4], 16)
    b1 = nar_to10(c1[4:6], 16)
    
    r2 = nar_to10(c2[0:2], 16)
    g2 = nar_to10(c2[2:4], 16)
    b2 = nar_to10(c2[4:6], 16)
    
    r_res = _mix(r1, r2, op, prop)
    g_res = _mix(g1, g2, op, prop)
    b_res = _mix(b1, b2, op, prop)
    
    return (nar_from10(r_res, 16, 2) +
            nar_from10(g_res, 16, 2) +
            nar_from10(b_res, 16, 2))

def nar_rgb(r1, g1, b1, r2, g2, b2, op='add', prop=50):
    for val in [r1, g1, b1, r2, g2, b2]:
        if not isinstance(val, int) or val < 0 or val > 255:
            nar_error(8)
    
    if not 0 <= prop <= 100:
        nar_error(6)
    
    r_res = _mix(r1, r2, op, prop)
    g_res = _mix(g1, g2, op, prop)
    b_res = _mix(b1, b2, op, prop)
    
    return (r_res, g_res, b_res)

def nar_hex2rgb(h):
    if len(h) != 6:
        nar_error(7)
    
    for ch in h.upper():
        if ch not in _HEX_DIGITS:
            nar_error(1)
    
    h = h.upper()
    r = nar_to10(h[0:2], 16)
    g = nar_to10(h[2:4], 16)
    b = nar_to10(h[4:6], 16)
    
    return (r, g, b)

def nar_rgb2hex(r, g, b):
    for val in [r, g, b]:
        if not isinstance(val, int) or val < 0 or val > 255:
            nar_error(8)
    
    return (nar_from10(r, 16, 2) +
            nar_from10(g, 16, 2) +
            nar_from10(b, 16, 2))

def nar_rand(base, length):
    if base < 2 or base > 62:
        nar_error(1)
    if length <= 0:
        nar_error(7)
    
    if length > 1:
        first_digit = random.randint(1, base-1)
        first_char = _DIGITS[first_digit]
        other_chars = ''.join(random.choice(_DIGITS[:base]) for _ in range(length-1))
        return first_char + other_chars
    else:
        return random.choice(_DIGITS[:base])

def nar_gray(hex_color):
    if len(hex_color) != 6:
        nar_error(7)
    
    for ch in hex_color.upper():
        if ch not in _HEX_DIGITS:
            nar_error(1)
    
    hex_color = hex_color.upper()
    r = nar_to10(hex_color[0:2], 16)
    g = nar_to10(hex_color[2:4], 16)
    b = nar_to10(hex_color[4:6], 16)
    
    gray = int(round(0.299 * r + 0.587 * g + 0.114 * b))
    gray = max(0, min(gray, 255))
    
    return nar_from10(gray, 16, 2) * 3

def nar_pad(num, base, length):
    if not nar_validate(num, base):
        nar_error(1)
    
    if length < len(num):
        nar_error(7)
    
    return num.rjust(length, '0')

def nar_validate(num, base):
    if isinstance(num, int):
        num = str(num)
    
    if base < 2 or base > 62:
        return False
    
    if base <= 36:
        num = num.upper()
    
    for char in num:
        try:
            digit_value = _DIGITS.index(char)
        except ValueError:
            return False
        
        if digit_value >= base:
            return False
    
    return True
