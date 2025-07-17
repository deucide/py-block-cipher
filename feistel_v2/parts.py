from feistel_v2.constants import diff_sbox1, diff_sbox2
from feistel_v2.constants import keysched_sbox
from feistel_v2.constants import perm_pbox, perm_invpbox
from feistel_v2.constants import sub_sbox, sub_invsbox, sub_bypos

'''
makes the individual parts used in basic.py
'''

#addkey
def addkey(state, key): #literally just xor
    return [state[i]^key[i] for i in range(len(state))]

#diffuse
def m(a, b):
	#multiplication on gf(2**8)
	b=str(bin(b))[2:][::-1]
	o, p=[], 0
	for i in range(len(b)):
		if int(b[i]):
			o.append(a<<i)
	for i in o:
		p^=i
	for i in range(len(str(bin(p)))-11, -1, -1):
		if p>=p^(283<<i):
			p^=283<<i
	return p
def d(u, b):
	#division on gf(2**8)
	for i in range(256):
		if m(i, b)==u: #ie a*b=u -> a=u/b
			return i
	return -1

#function super sens to changes in A
r = lambda A: (7**(A%6) ^ diff_sbox1[A%16] ^ diff_sbox2[-A%16])%256
#transform A in diffusion's first transformation
t1 = lambda A, i0, B, C, D: m(A, diff_sbox1[i0+3])^r(diff_sbox1[i0]*B+diff_sbox1[i0+1]*C+diff_sbox1[i0+2]*D)
#return A from U generated in t1
invt1 = lambda U, i0, B, C, D: d(U^r(diff_sbox1[i0]*B+diff_sbox1[i0+1]*C+diff_sbox1[i0+2]*D), diff_sbox1[i0+3])
#transfrom A in diffusion's second transformation
t2 = lambda A, i, B, C, D: m(A, diff_sbox1[i])^r(diff_sbox1[i]*(B*C+D))
#return A from U generated in t2
invt2 = lambda U, i, B, C, D: d(U^r(diff_sbox1[i]*(B*C+D)), diff_sbox1[i])

def diff(state):
	state=[state[i]^diff_sbox2[i] for i in range(16)]
	for i in [0, 4, 8, 12]:
		state[i+3]=t1(state[i+3], i, state[i], state[i+1], state[i+2])
	for i in [0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 14, 15]:
		state[i]=t2(state[i], i, state[3], state[7], state[11])
	for i in range(15):
		state[i]^=r(state[15])
	return state
def inv_diff(state):
	state=[i for i in state]
	for i in range(15):
		state[i]^=r(state[15])
	for i in [0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 14, 15]:
		state[i]=invt2(state[i], i, state[3], state[7], state[11])
	for i in [0, 4, 8, 12]:
		state[i+3]=invt1(state[i+3], i, state[i], state[i+1], state[i+2])
	return [state[i]^diff_sbox2[i] for i in range(16)]

#key schedule
def keysched(init_key, rounds):
    vals = [i for i in init_key]
    for i in range(16*rounds+64):
        vals.append(keysched_sbox[(i + sum(vals[-4:]+vals[::2]))%256])
    vals = vals[len(init_key):]

    whit_in, round_keys, whit_out = vals[:32], vals[32:-32], vals[-32:]
    round_keys = [round_keys[16*i:16*i+16] for i in range(rounds)]
    return [whit_in] + round_keys + [whit_out]

#permute
def perm(state):
    return [state[i] for i in perm_pbox]
def inv_perm(state):
    return [state[i] for i in perm_invpbox]

#substitute
def sub(state):
    return [sub_sbox[v^sub_bypos[i]] for i,v in enumerate(state)]
def inv_sub(state):
    return [sub_invsbox[v]^sub_bypos[i] for i,v in enumerate(state)]