m = 6 ; n = 16
result = []
nLimit = n-1
for i in range(m):
    if i>nLimit:i=nLimit
    remaining = ''
    if n-i-1>0:
        if i==m-1:remaining = '.'*(n-i-1)
        else:remaining = '.'+'#'*(n-i-2)
    resultantString = '#'*i+'.'+remaining
    result.append(resultantString)
print(result)

# ['..##############', '#..#############', '##..############', '###..###########', '####..##########', '#####...........']

