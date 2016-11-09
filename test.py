mylist = [1,2,3,4,5,6]



rightval = 0
leftval = 0

for i in mylist[0:3]:
    rightval += i
for i in mylist[3:6]:
    leftval += i

print(rightval)
print(leftval)


