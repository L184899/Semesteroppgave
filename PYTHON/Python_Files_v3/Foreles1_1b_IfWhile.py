
# Some basis stuff


str1 = input("tall1 : ")
str2 = input("tall2 : ")

tall1:int = int(str1)
tall2:int = int(str2)

if tall1 == tall2 :
    print("tallene er like : ")
else:
    print("tallene er ulike : ")


while tall1 > 0 :
    print(f"Tallet er : {tall1}")
    tall1 = tall1 - 1


