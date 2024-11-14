def logical_or(x1, x2): 
    return x1 or x2

def logical_and(x1, x2): 
    return x1 and x2

def xor(x1, x2): 
    return int(logical_or(x1, x2) and not logical_and(x1, x2))

print("XOR(0, 0):", xor(0, 0)) 
print("XOR(1, 0):", xor(1, 0))
print("XOR(0, 1):", xor(0, 1))
print("XOR(1, 1):", xor(1, 1)) 