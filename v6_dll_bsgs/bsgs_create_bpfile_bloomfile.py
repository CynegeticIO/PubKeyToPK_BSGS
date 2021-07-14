# -*- coding: utf-8 -*-
"""
Create bpfile.bin and bloomfile.bin using multi_cpu

Usage :
 > python bsgs_create_bpfile_bloomfile.py 400000000 bpfile.bin bloomfile.bin 4

@author: iceland
"""
import sys
import time
import ctypes
import os
import platform
import math

###############################################################################
if platform.system().lower().startswith('win'):
    dllfile = 'ice_secp256k1.dll'
    if os.path.isfile(dllfile) == True:
        pathdll = os.path.realpath(dllfile)
        ice = ctypes.CDLL(pathdll)
    else:
        print('File {} not found'.format(dllfile))
    
elif platform.system().lower().startswith('lin'):
    dllfile = 'ice_secp256k1.so'
    if os.path.isfile(dllfile) == True:
        pathdll = os.path.realpath(dllfile)
        ice = ctypes.CDLL(pathdll)
    else:
        print('File {} not found'.format(dllfile))
    
else:
    print('[-] Unsupported Platform currently for ctypes dll method. Only [Windows and Linux] is working')
    sys.exit()
    
###############################################################################
ice.scalar_multiplication.argtypes = [ctypes.c_char_p, ctypes.c_char_p]            # pvk,ret
ice.point_increment.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p] # x,y,ret
ice.point_negation.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]  # x,y,ret
ice.point_doubling.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]  # x,y,ret
ice.hash_to_address.argtypes = [ctypes.c_int, ctypes.c_bool, ctypes.c_char_p]  # 012,comp,hash
ice.hash_to_address.restype = ctypes.c_char_p
ice.pubkey_to_address.argtypes = [ctypes.c_int, ctypes.c_bool, ctypes.c_char_p, ctypes.c_char_p]  # 012,comp,x,y
ice.pubkey_to_address.restype = ctypes.c_char_p
ice.create_baby_table.argtypes = [ctypes.c_ulonglong, ctypes.c_ulonglong, ctypes.c_char_p] # start,end,ret
ice.point_addition.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p] # x1,y1,x2,y2,ret
ice.point_subtraction.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p] # x1,y1,x2,y2,ret
ice.point_loop_subtraction.argtypes = [ctypes.c_ulonglong, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p] # k,x1,y1,x2,y2,ret

ice.init_secp256_lib()

###############################################################################
if platform.system().lower().startswith('win'):
    dllfile = 'BSGS.dll'
    if os.path.isfile(dllfile) == True:
        pathdll = os.path.realpath(dllfile)
        icebsgs = ctypes.CDLL(pathdll)
    else:
        print('File {} not found'.format(dllfile))

elif platform.system().lower().startswith('lin'):
    dllfile = 'BSGS.so'
    if os.path.isfile(dllfile) == True:
        pathdll = os.path.realpath(dllfile)
        icebsgs = ctypes.CDLL(pathdll)
    else:
        print('File {} not found'.format(dllfile))
else:
    print('[-] Unsupported Platform currently for ctypes dll method. Only [Windows and Linux] is working')
    sys.exit()

icebsgs.init_bsgs_bloom.argtypes = [ctypes.c_int, ctypes.c_ulonglong, ctypes.c_ulonglong, ctypes.c_int, ctypes.c_char_p] #cpu,total,_bits,_hashes,_bf

###############################################################################

def scalar_multiplication(kk):
    res = (b'\x00') * 65
    pass_int_value = hex(kk)[2:].encode('utf8')
    ice.scalar_multiplication(pass_int_value, res)
    return res

def point_increment(pubkey_bytes):
    x1 = pubkey_bytes[1:33]
    y1 = pubkey_bytes[33:]
    res = (b'\x00') * 65
    ice.point_increment(x1, y1, res)
    return res

def point_negation(pubkey_bytes):
    x1 = pubkey_bytes[1:33]
    y1 = pubkey_bytes[33:]
    res = (b'\x00') * 65
    ice.point_negation(x1, y1, res)
    return res

def hash_to_address(addr_type, iscompressed, hash160_bytes):
    # type = 0 [p2pkh],  1 [p2sh],  2 [bech32]
    res = ice.pubkey_to_address(addr_type, iscompressed, hash160_bytes)
    return res.decode('utf8')

def pubkey_to_address(addr_type, iscompressed, pubkey_bytes):
    # type = 0 [p2pkh],  1 [p2sh],  2 [bech32]
    x1 = pubkey_bytes[1:33]
    y1 = pubkey_bytes[33:]
    res = ice.pubkey_to_address(addr_type, iscompressed, x1, y1)
    return res.decode('utf8')
    
def create_baby_table(start_value, end_value):
    res = (b'\x00') * ((1+end_value-start_value) * 32)
    ice.create_baby_table(start_value, end_value, res)
    return res

def point_doubling(pubkey_bytes):
    x1 = pubkey_bytes[1:33]
    y1 = pubkey_bytes[33:]
    res = (b'\x00') * 65
    ice.point_doubling(x1, y1, res)
    return res

def point_addition(pubkey1_bytes, pubkey2_bytes):
    x1 = pubkey1_bytes[1:33]
    y1 = pubkey1_bytes[33:]
    x2 = pubkey2_bytes[1:33]
    y2 = pubkey2_bytes[33:]
    res = (b'\x00') * 65
    ice.point_addition(x1, y1, x2, y2, res)
    return res

def point_subtraction(pubkey1_bytes, pubkey2_bytes):
    x1 = pubkey1_bytes[1:33]
    y1 = pubkey1_bytes[33:]
    x2 = pubkey2_bytes[1:33]
    y2 = pubkey2_bytes[33:]
    res = (b'\x00') * 65
    ice.point_subtraction(x1, y1, x2, y2, res)
    return res

def point_loop_subtraction(num, pubkey1_bytes, pubkey2_bytes):
    x1 = pubkey1_bytes[1:33]
    y1 = pubkey1_bytes[33:]
    x2 = pubkey2_bytes[1:33]
    y2 = pubkey2_bytes[33:]
    res = (b'\x00') * (65 * num)
    ice.point_loop_subtraction(num, x1, y1, x2, y2, res)
    return res

###############################################################################

def create_table(start_value, end_value):
    baby_steps = create_baby_table(start_value, end_value)
    return baby_steps
  
# =============================================================================
if __name__ == '__main__':
    if len(sys.argv) > 5 or len(sys.argv) < 5:
        print('[+] Program Usage.... ')
        print('{} <bP items> <output bpfilename> <output bloomfilename> <Number of cpu>\n'.format(sys.argv[0]))
        print('Example to create a File with 400 million items using 4 cpu:\n{} 400000000 bpfile.bin bloomfile.bin 4'.format(sys.argv[0]))
        sys.exit()
        
    
    st = time.time()
    total = int(sys.argv[1])
    bs_file = sys.argv[2]
    bloom_file = sys.argv[3]
    num_cpu = int(sys.argv[4])
    out = open(bs_file, 'wb')
    
    
    print('\n[+] Program Running please wait...')
    if total%(num_cpu*1000) != 0: 
        total = num_cpu*1000*(total//(num_cpu*1000))
        print('[*] Number of elements should be a multiple of 1000*num_cpu. Automatically corrected it to nearest value:',total)
    w = math.ceil(math.sqrt(total))
    
    bloom_prob = 0.000000001                # False Positive = 1 out of 1 billion
    bloom_bpe = -(math.log(bloom_prob) / 0.4804530139182014)
    
    bloom_bits = int(total * bloom_bpe)  # ln(2)**2
    if bloom_bits % 8: bloom_bits = 8*(1 + (bloom_bits//8))
    bloom_hashes = math.ceil(0.693147180559945 * bloom_bpe)
    
    print('[+] Number of items required for Final Script : [bp : {0}] [bloom : {1}]'.format(w, total))
    print('[+] Output Size of the files : [bp : {0} Bytes] [bloom : {1} Bytes]'.format(w*32, bloom_bits//8))
    print('[+] Creating bpfile in range {0} to {1} '.format(1, w))
    
    
    results = create_table(1, w)
    out.write(results)
    out.flush()
    os.fsync(out.fileno())
    out.close()
    print('[+] File : {0} created successfully in {1:.2f} sec\n'.format(bs_file, time.time() - st))
    st = time.time()
    
###############################################################################
    

    print('[+] Starting bloom file creation ... with False Positive probability :', bloom_prob)
    print('[+] bloom bits  :', bloom_bits, '   size [%s MB]'%(bloom_bits//(8*1024*1024)))
    print('[+] bloom hashes:', bloom_hashes)
    
    print('[+] Initializing the bloom filters to null')
    bloom_filter = bytes(b'\x00') * (bloom_bits//8)
    
    icebsgs.init_bsgs_bloom(num_cpu, total, bloom_bits, bloom_hashes, bloom_filter)
    
    print('\r[+] Saving bloom filter to File')
    with open(bloom_file, 'wb') as fh: 
        fh.write(bloom_filter)
    print('[+] File : {0} created successfully in {1:.2f} sec'.format(bloom_file, time.time() - st))
    print('[+] Program Finished \n')