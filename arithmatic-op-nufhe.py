import random
import nufhe

def fixSizeBoolList(decimal,size):
    x = [int(x) for x in bin(decimal)[2:]]
    x = list(map(bool, x))
    x = [False]*(size - len(x)) + x
    return x

# in subtraction, ciX have to be greater than ciY
def subtract(ciX, ciY):
    for i in range(size):
        ciXnotTemp = ciX
        a = vm.gate_and(vm.gate_not(ciX), ciY)
        ciX = vm.gate_xor(ciX, ciY)
        aShiftTemp = a
        aShiftTemp.roll(-1, axis=-1)
        ciY = aShiftTemp

    return ciX

def checkSubtract(sub1,sub2):
    if sub1 > sub2:
        return sub2
    else :
        return sub1

def add(ciX, ciY):
    for i in range(size):
        a = vm.gate_and(ciX, ciY)
        b = vm.gate_xor(ciX, ciY)
        aShiftTemp = a
        aShiftTemp.roll(-1, axis=-1)
        ciX = aShiftTemp
        ciY = b

    return b

def boolListToInt(bitlists):
    out = 0
    for bit in bitlists:
        out = (out << 1) | bit
    return out

### testing ###

ctx = nufhe.Context()
secret_key, cloud_key = ctx.make_key_pair()
# size even decimal only
size = 32
# test decimal number. need to be less than size/2
deci_x = 3093
deci_y = 1999

x = fixSizeBoolList(deci_x,size)
print(x)
y = fixSizeBoolList(deci_y,size)
print(y)
ciX = ctx.encrypt(secret_key, x)
ciY = ctx.encrypt(secret_key, y)
vm = ctx.make_virtual_machine(cloud_key)

# subtraction have to be done twice since we don't know which one is grater than the other
subXthenY = ctx.decrypt(secret_key, subtract(ciX, ciY))
subYthenX = ctx.decrypt(secret_key, subtract(ciY, ciX))
# the Lesser result is the right one
plainSubtractNumber = checkSubtract(boolListToInt(subXthenY),boolListToInt(subYthenX))
print("reference subtract number is : ", (deci_x-deci_y) ,"/ nuFHE subtract number is : ", plainSubtractNumber)


plainAddNumber = ctx.decrypt(secret_key, add(ciX, ciY))
print("reference add number is : ", (deci_x+deci_y) ,"/ nuFHE subtract number is : ", boolListToInt(plainAddNumber))
