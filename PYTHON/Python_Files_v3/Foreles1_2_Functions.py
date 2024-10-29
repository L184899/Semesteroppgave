# 1. Functions must be defined before usag
# 2. Variables, THAT change muest be defined by the global keyword

def summer(x, y)  :
    return x+y

z = summer(2,4)
print (f"2+4={z}")


def multipliser(x, y:int)  -> int :
   return x * y

prod = multipliser(3, 5)
print(f"3*5={prod}")


print(f"3.14*4 = {multipliser(3.14, 4)}")


def summer_tupple(t1, t2):
    return t1+t2

def summer_tupple2(t1, t2):
    return t1[0] + t2[0], t1[1] + t2[1]

a = (1,1)
b = (2,1)

print (summer_tupple2(a,b))
