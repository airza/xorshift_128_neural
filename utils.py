import numpy as np
import torch

def print_comparable_bits(int1, int2):
    if (int1==int2):
        print("Equal")
        return None
    bin1 = f'{int1:064b}'
    bin2 = f'{int2:064b}'
    print(bin1)
    print(bin2)

def float_bits_to_int(x):
    x = x.squeeze(0).round().int().tolist()
    out = 0
    for bit in x:
        out = (out << 1) | bit
    return out
def int_to_bits_tensor(x,width=64):
    out = torch.zeros(width)
    for i in range(width):
        out[width-i-1] = x & 1
        x >>= 1
    return out