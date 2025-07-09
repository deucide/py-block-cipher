from parts import keysched
from parts import addkey, diff, perm, sub
from parts import inv_diff, inv_perm, inv_sub
from constants import rounds

'''
handles the basic encryption/decryption w/o modes
'''

def base_encrypt(state, key):
    '''
    only supports one block
    no special modes available
    '''
    keys = keysched(key, rounds)

    state = addkey(state, keys[0])
    u, e = state[:16], state[16:]
    for r in range(rounds):
        e = addkey(e, keys[r+1])
        e = sub(e)
        e = perm(e)
        e = diff(e)

        u = addkey(u, e)
        u, e = e, u
    state = addkey(u+e, keys[-1])

    return state

def base_decrypt(state, key):
    '''
    only supports one block
    no special modes available
    '''
    keys = keysched(key, rounds)[::-1]

    state = addkey(state, keys[0])
    u, e = state[:16], state[16:]
    for r in range(rounds):
        u, e = e, u
        u = addkey(u, e)

        e = inv_diff(e)
        e = inv_perm(e)
        e = inv_sub(e)
        e = addkey(e, keys[r+1])
    state = addkey(u+e, keys[-1])

    return state