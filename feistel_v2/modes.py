from feistel_v2.basic import base_encrypt, base_decrypt
from feistel_v2.parts import addkey

'''
uses the basic encryption/decryption function and adds modes
'''

def mode_encrypt(state, key, extra=[], mode='ecb'):
    #extra treated as iv or nonce depending on context

    #initialize extra if none given
    if extra==[]:
        if mode in ['cfb', 'cbc', 'ofb', 'pcbc']:
            extra = [0 for i in range(16)]
        elif mode == 'ctr':
            extra = [0 for i in range(8)]

    #convert to bits and padding
    bstring = ''
    for i in state:
        i_bits = bin(i)[2:]
        while len(i_bits)<8:
            i_bits = '0' + i_bits
        bstring += i_bits
    #add 1 then 0s as necessary
    bstring += '1'
    while len(bstring)%256 != 0:
        bstring+='0'

    #forming blocks
    dec_vals = [int(bstring[8*i:8*i+8], 2) for i in range(len(bstring)//8)]
    blocks = [dec_vals[32*i:32*i+32] for i in range(len(dec_vals)//32)]

    #encrypting each block
    if mode=='ecb':
        blocks = [base_encrypt(block, key) for block in blocks]
    elif mode=='cfb':
        for i, block in enumerate(blocks):
            if i==0:
                blocks[i] = addkey(base_encrypt(extra, key), block)
            else:
                blocks[i] = addkey(base_encrypt(blocks[i-1], key), block)
    elif mode=='cbc':
        for i, block in enumerate(blocks):
            if i==0:
                blocks[i] = base_encrypt(addkey(block, extra), key)
            else:
                blocks[i] = base_encrypt(addkey(block, blocks[i-1]), key)
    elif mode=='ofb':
        num_blocks = len(blocks)
        output_feedback = [base_encrypt(extra, key)]
        for i in range(num_blocks-1):
            output_feedback.append(base_encrypt(output_feedback[-1], key))
        blocks = [addkey(output_feedback[i], blocks[i]) for i in range(num_blocks)]
    elif mode=='pcbc':
        plaintext_copy = [i for i in blocks]
        for i in range(len(blocks)):
            if i==0:
                blocks[i] = base_encrypt(addkey(blocks[i], extra), key)
            else:
                to_xor = addkey(plaintext_copy[i-1], blocks[i-1])
                blocks[i] = base_encrypt(addkey(blocks[i], to_xor), key)
    elif mode=='ctr':
        num_blocks = len(blocks)
        to_encrypt = []
        for i in range(num_blocks):
            ctr_bits = bin(i%65536)[2:]
            while len(ctr_bits)<128:
                ctr_bits = '0' + ctr_bits
            ctr_dec=[int(ctr_bits[8*i:8*i+8], 2) for i in range(len(ctr_bits)//8)]
            to_encrypt.append(extra + ctr_dec)
        blocks = [addkey(base_encrypt(to_encrypt[i], key), blocks[i]) for i in range(num_blocks)]
    else:
        raise ValueError('cipher mode is unsupported or invalid')

    #combine blocks and output
    output=[]
    for i in blocks:
        output+=i
    return output
            

def mode_decrypt(state, key, extra=[], mode='ecb'):
    #extra treated as iv or nonce depending on context

    #initialize extra if none given
    if extra==[]:
        if mode in ['cfb', 'cbc', 'ofb', 'pcbc']:
            extra = [0 for i in range(16)]
        elif mode == 'ctr':
            extra = [0 for i in range(8)]

    #forming blocks
    blocks = [state[32*i:32*i+32] for i in range(len(state)//32)]

    #decrypting each block
    if mode=='ecb':
        blocks = [base_decrypt(block, key) for block in blocks]
    elif mode=='cfb':
        partial_decrypt = [
            base_encrypt(extra, key) if i==0
            else base_encrypt(blocks[i-1], key)
            for i in range(len(blocks))
        ]
        blocks = [addkey(blocks[i], partial_decrypt[i]) for i in range(len(blocks))]
    elif mode=='cbc':
        partial_decrypt = [base_decrypt(block, key) for block in blocks]
        blocks = [
            addkey(partial_decrypt[i], extra) if i==0
            else addkey(partial_decrypt[i], blocks[i-1])
            for i in range(len(blocks))
        ]
    elif mode=='ofb':
        num_blocks = len(blocks)
        output_feedback = [base_encrypt(extra, key)]
        for i in range(num_blocks-1):
            output_feedback.append(base_encrypt(output_feedback[-1], key))
        blocks = [addkey(output_feedback[i], blocks[i]) for i in range(num_blocks)]
    elif mode=='pcbc':
        ciphertext_copy = [i for i in blocks]
        partial_decrypt = [base_decrypt(block, key) for block in blocks]
        for i in range(len(blocks)):
            if i==0:
                blocks[i]=addkey(partial_decrypt[i], extra)
            else:
                to_xor = addkey(ciphertext_copy[i-1], blocks[i-1])
                blocks[i] = addkey(partial_decrypt[i], to_xor)
    elif mode=='ctr':
        num_blocks = len(blocks)
        to_encrypt = []
        for i in range(num_blocks):
            ctr_bits = bin(i%65536)[2:]
            while len(ctr_bits)<128:
                ctr_bits = '0' + ctr_bits
            ctr_dec=[int(ctr_bits[8*i:8*i+8], 2) for i in range(len(ctr_bits)//8)]
            to_encrypt.append(extra + ctr_dec)
        blocks = [addkey(base_encrypt(to_encrypt[i], key), blocks[i]) for i in range(num_blocks)]
    else:
        raise ValueError('cipher mode is unsupported or invalid')

    #convert to bits and depad
    combined_blocks = []
    for block in blocks:
        combined_blocks+=block

    bstring = ''
    for i in combined_blocks:
        i_bits = bin(i)[2:]
        while len(i_bits)<8:
            i_bits = '0' + i_bits
        bstring += i_bits
    #see mode encrypt for padding details
    while bstring[-1]=='0':
        bstring = bstring[:-1]
    bstring = bstring[:-1]

    #forming blocks and output
    dec_vals = [int(bstring[8*i:8*i+8], 2) for i in range(len(bstring)//8)]
    return dec_vals