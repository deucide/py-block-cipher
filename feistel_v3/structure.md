## very very rough notes

### structure: (using parts)    
    i=o = 128bits=16bytes

    input whitening   
    i —split→ a,b,c,d (each 32bits=4bytes)

    each round: (# of rounds dep on key size)   
        all —addkey→ all   
        a,b —F→ A,B   
            F:   
            a —sub1→ a   
            b —sub2→ b   
            a,b —h→ A,B   
                h: perm+mix all
        A,c —diff→ A,c; B,d —diff→ B,d   
        A,B,c,d → d,c,a,b (ie a,b,c,d=d,c,A,B)

    a,b,c,d —recombine→ o   
    output whitening   
    return o   
   
### parts:   
    ADDKEY                              xor(state, round key)
        i=o = 128bits=16bytes   
    MIX                                 (state → vector) \* mds   
        i=o = 64bits=8bytes   
        mds                             cyclic using rots of [1,13,1,11,2,7,3,5]   
            dimensions                  (8x8, bytes)   
        over                            gf(256)/<x8+x7+x5+x+1> 
    PERMUTE                             permute nibbles by map   
        i=o = 64bits=8bytes   
        map                             [4,14,5,1,8,7,3,9,12,11,6,13,0,15,10,2]   
    SUB                                 sub by map of bent func   
        i=o = any; 2 variants   
        map                             nyberg sbox; see code   
    KEYEXP                              iter.ly append "summary" of prev.; see code
        i = any
        o = 32+8\*rounds bytes