from feistel_v2.modes import mode_encrypt as feistel_v2_mode_encrypt
from feistel_v2.modes import mode_decrypt as feistel_v2_mode_decrypt
from feistel_v3.modes import mode_encrypt as feistel_v3_mode_encrypt
from feistel_v3.modes import mode_decrypt as feistel_v3_mode_decrypt

'''
handles input/output
ideally run from here
'''
B64_CONVERTOR = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

def str_to_bytes(s):
    s=s.encode('utf-8')
    return [s[i] for i in range(len(s))]
def bytes_to_str(b):
    return bytes(b).decode('utf-8')

def bytes_to_b64(b):
    bstring = ''
    for i in b:
        i_bits = bin(i)[2:]
        while len(i_bits)<8:
            i_bits = '0' + i_bits
        bstring += i_bits

    bstring+='1'
    while len(bstring)%6!=0:
        bstring+='0'

    bit_chunks = [bstring[6*i:6*i+6] for i in range(len(bstring)//6)]
    b64_chunks = [B64_CONVERTOR[int(chunk, 2)] for chunk in bit_chunks]
    b64 = ''.join(b64_chunks)

    while len(b64)%4!=0:
        b64+='='
    
    return b64
def b64_to_bytes(b64):
    while b64[-1]=='=':
        b64 = b64[:-1]

    bit_chunks = [bin(B64_CONVERTOR.index(i))[2:] for i in b64]
    for i in range(len(bit_chunks)):
        while len(bit_chunks[i])<6:
            bit_chunks[i] = '0'+bit_chunks[i]

    bstring = ''.join(bit_chunks)
    while bstring[-1]=='0':
        bstring = bstring[:-1]
    bstring = bstring[:-1]

    byte_chunks = [int(bstring[8*i:8*i+8], 2) for i in range(len(bstring)//8)]
    return byte_chunks

'''
main workings
'''
if __name__=='__main__':
    '''
    INFO ->
    supported cipher modes: ecb cfb cbc ofb pcbc ctr
    for enc_or_dec, specify either 'enc' or 'dec'
    for cipher, specify either 'feistel v2' or 'feistel v3'

    block size of 256 bits = 32 bytes
    key size -> any length, the longer the better
    23 rounds using a feistel design

    io modes are:
        utf8: for standard string input
        bytes: for a list of integers (ie bytes)
        b64: for base64
    '''

    #cipher config
    cipher_mode = 'ecb'
    enc_or_dec = 'enc'
    cipher = 'feistel v3'

    #data value io
    src = ''
    key = ''
    extra = [0 for i in range(8)] #used as iv or nonce depending on context

    #handles io formats
    src_imode = 'utf8'
    key_imode = 'utf8'
    extra_imode = 'bytes'
    ctext_omode = 'b64'

    #converting input data to bytes
    if src_imode == 'utf8':
        src = str_to_bytes(src)
    elif src_imode == 'b64':
        src = b64_to_bytes(src)
    elif src_imode != 'bytes':
        raise ValueError('main.py: improper src_imode passed')
    if key_imode == 'utf8':
        key = str_to_bytes(key)
    elif key_imode == 'b64':
        key = b64_to_bytes(key)
    elif key_imode != 'bytes':
        raise ValueError('main.py: improper key_imode passed')
    if extra_imode == 'utf8':
        extra = str_to_bytes(extra)
    elif extra_imode == 'b64':
        extra = b64_to_bytes(extra)
    elif extra_imode != 'bytes':
        raise ValueError('main.py: improper extra_imode passed')

    #encryption/decryption
    if cipher == 'feistel v2':
        if enc_or_dec == 'enc':
            f = feistel_v2_mode_encrypt
        elif enc_or_dec == 'dec':
            f = feistel_v2_mode_decrypt
    elif cipher == 'feistel v3':
        if enc_or_dec == 'enc':
            f = feistel_v3_mode_encrypt
        elif enc_or_dec == 'dec':
            f = feistel_v3_mode_decrypt
    ctext = f(src, key, extra, cipher_mode)

    #convert bytes to output data
    if ctext_omode == 'utf8':
        ctext = bytes_to_str(ctext)
    elif ctext_omode == 'b64':
        ctext = bytes_to_b64(ctext)
    elif ctext_omode != 'bytes':
        raise ValueError('main.py: improper ctext_omode passed')
    print(ctext)
