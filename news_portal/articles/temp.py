n = (1000000)
lst = []
while n >= 1000:
    lst.append(str(n)[-3:])
    n //= 1000
lst.append(str(n))
print(','.join(lst[::-1]))

