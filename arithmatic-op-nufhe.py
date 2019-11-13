import random
import nufhe

def fixSizeBoolList(decimal,size):
    x = [int(x) for x in bin(decimal)[2:]]
    x = list(map(bool, x))
    x = [False]*(size - len(x)) + x
    return x

def subtract(ciX, ciY):
    for i in range(size):
        ciXnotTemp = ciX
        a = vm.gate_and(vm.gate_not(ciX), ciY)
        # print("a : ",ctx.decrypt(secret_key, a))
        ciX = vm.gate_xor(ciX, ciY)
        # print("b : ",ctx.decrypt(secret_key, b))
        aShiftTemp = a
        # print("aShiftTemp : ",ctx.decrypt(secret_key, aShiftTemp))
        aShiftTemp.roll(-1, axis=-1)
        ciY = aShiftTemp
        # print("ciX : ",ctx.decrypt(secret_key, ciX))
        # print("ciY : ",ctx.decrypt(secret_key, ciY))
    return ciX

# incase the
def checkSubtract(sub1,sub2):
    if sub1 > sub2:
        return sub2
    else :
        return sub1

def add(ciX, ciY):
    for i in range(size):
        a = vm.gate_and(ciX, ciY)
        # print("a : ",ctx.decrypt(secret_key, a))
        b = vm.gate_xor(ciX, ciY)
        # print("b : ",ctx.decrypt(secret_key, b))
        aShiftTemp = a
        # print("aShiftTemp : ",ctx.decrypt(secret_key, aShiftTemp))
        aShiftTemp.roll(-1, axis=-1)
        ciX = aShiftTemp
        # print("ciX : ",ctx.decrypt(secret_key, ciX))
        ciY = b
        # print("ciY : ",ctx.decrypt(secret_key, ciY))
    return b

def boolListToIntList(bitlists):
    out = 0
    for bit in bitlists:
        out = (out << 1) | bit
    return out

ctx = nufhe.Context()
secret_key, cloud_key = ctx.make_key_pair()
# size even decimal only
size = 32
#
deci_x = 3093
deci_y = 1999

x = fixSizeBoolList(deci_x,size)
print(x)
y = fixSizeBoolList(deci_y,size)
print(y)
ciX = ctx.encrypt(secret_key, x)
ciY = ctx.encrypt(secret_key, y)
# refAndGate = [(b1 and b2) for b1, b2 in zip(x, y)]
vm = ctx.make_virtual_machine(cloud_key)


plainNumber = ctx.decrypt(secret_key, subtract(ciX, ciY))
print("reference subtract number is : ", (deci_x-deci_y) ,"/ nuFHE subtract number is : ", boolListToIntList(plainNumber))
# print("add nuber is... : ",ctx.decrypt(secret_key, add(ciX, ciY)))

# a = vm.gate_not(ciY)
# ciY.copy()
# assert all(result_bits == refAndGate)
# result = vm.gate_and(ciX, ciY)
# result_bits = ctx.decrypt(secret_key, result)
