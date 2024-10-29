def SumProd(tallA=0, tallB=0, tallC=0):
    return tallA+tallB*2+tallC*3


print(SumProd(10, 15, 20))
print(SumProd(tallA=10, tallB=10))
print(SumProd(tallC=10, tallA=20))


#must use global, because we are changing the variable x
def incrementX(n=1):
    global x
    x = x + n

x = 100
incrementX(55)
print(x)
