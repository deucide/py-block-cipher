from feistel_v3.constants import WHOLE_KEYSIZE_TO_ROUNDS
from feistel_v3.parts import keyexp
from feistel_v3.parts import addkey, mix, perm, sub1, sub2
from feistel_v3.parts import inv_addkey, inv_mix, inv_perm, inv_sub1, inv_sub2

#encrypt, decrypt blocks
def encrypt_block(state, init_key):
    #preparations
    rounds = WHOLE_KEYSIZE_TO_ROUNDS[len(init_key)] #get rounds
    keys = keyexp(init_key, rounds) #get keys
    state = addkey(state[:], keys[0]) #input whitening

    #rounds
    for rd_num in range(rounds):
        #addkey
        state = addkey(state, keys[rd_num+1]) #xor all
        a,b,c,d = state[:4], state[4:8], state[8:12], state[12:] #split
        #run F on a,b
        a, b = sub1(a), sub2(b) #substitute
        ab = mix(perm(a+b)) #combine, perm, mix
        a,b = ab[:4], ab[4:8] #split
        #diffuse to c,d
        ac, bd = mix(a+c), mix(b+d) #combine, mix
        a,b,c,d = ac[:4], bd[:4], ac[4:], bd[4:] #split
        #rearrange, combine
        state = d+c+a+b
    
    #output whitening, return
    state = addkey(state, keys[-1])
    return state
def decrypt_block(state, init_key):
    #preparations
    rounds = WHOLE_KEYSIZE_TO_ROUNDS[len(init_key)] #get rounds
    keys = keyexp(init_key, rounds)[::-1] #get keys, reverse
    state = inv_addkey(state[:], keys[0]) #undo output whitening

    #rounds
    for rd_num in range(rounds):
        #split, undo rearrange
        a,b,c,d = state[8:12], state[12:], state[4:8], state[:4]
        #undo diffuse to c,d
        ac, bd = inv_mix(a+c), inv_mix(b+d) #combine, undo mix
        a,b,c,d = ac[:4], bd[:4], ac[4:], bd[4:] #split
        #undo run F on a,b
        ab = inv_perm(inv_mix(a+b)) #undo combine, perm, mix
        a,b = ab[:4], ab[4:] #split
        a, b = inv_sub1(a), inv_sub2(b) #undo substitute
        #undo addkey
        state = inv_addkey(a+b+c+d, keys[rd_num+1]) #combine, undo xor all

    #undo input whitening, return
    state = addkey(state, keys[-1])
    return state