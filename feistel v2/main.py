from constants import b64_convertor
from modes import mode_encrypt, mode_decrypt

'''
handles input/output
RUN FROM HERE
'''

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
    b64_chunks = [b64_convertor[int(chunk, 2)] for chunk in bit_chunks]
    b64 = ''.join(b64_chunks)

    while len(b64)%4!=0:
        b64+='='
    
    return b64
def b64_to_bytes(b64):
    while b64[-1]=='=':
        b64 = b64[:-1]

    bit_chunks = [bin(b64_convertor.index(i))[2:] for i in b64]
    for i in range(len(bit_chunks)):
        while len(bit_chunks[i])<6:
            bit_chunks[i] = '0'+bit_chunks[i]

    bstring = ''.join(bit_chunks)
    while bstring[-1]=='0':
        bstring = bstring[:-1]
    bstring = bstring[:-1]

    byte_chunks = [int(bstring[8*i:8*i+8], 2) for i in range(len(bstring)//8)]
    return byte_chunks

if __name__=='__main__':
    '''
    INFO ->
    supported modes: ecb cfb cbc ofb pcbc ctr

    block size of 256 bits = 32 bytes
    key size -> any length, the longer the better
    23 rounds using a feistel design

    src, key, and extra can all be a str or list
    '''

    mode = 'pcbc'
    enc_or_dec = 'enc'

    #these can be str or list
    src = 'tdst'
    key = 'rtyuiuyf'
    extra = [0 for i in range(32)] #used as iv or nonce depending on context

    if isinstance(key, str):
        key = str_to_bytes(key)
    if isinstance(extra, str):
        extra = str_to_bytes(extra)

    if enc_or_dec=='enc':
        if isinstance(src, str):
            src = str_to_bytes(src)
        print(bytes_to_b64(mode_encrypt(src, key, extra, mode)))
    else:
        if isinstance(src, str):
            src = b64_to_bytes(src)
        print(bytes_to_str(mode_decrypt(src, key, extra, mode)))