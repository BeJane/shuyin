a=input().split()
n = int(a[0])
m = int(a[1])
a = input().split()
b= input().split()
max = int(b[0])//int(a[0])
for i in range(0,n):
    a[i] = int(a[i])
    b[i]= int(b[i])
    if b[i]//a[i] < max:
        max = b[i]//a[i]
    if max == 0:
        break

b = [x-max*y for (x,y) in zip(b,a)]
while m > 0 and max != 0:
    flag = 0
    #b = [int(x) - int(y) for (x, y) in zip(b, a)]
    #print(b,m)
    for i in range(0,n):
        b[i] = b[i] - a[i]
        if b[i] < 0 and b[i] + m >= 0:
            m = m + b[i]
            b[i]=0
            #print(b,m)
        elif b[i] < 0 and b[i] + m < 0:
            flag = -1
            break

    if flag == 0:
        max = max + 1
    else:
        break
print(max)
