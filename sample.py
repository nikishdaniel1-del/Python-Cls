'''m = 6 ; n = 16
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
print(result)'''

# ['..##############', '#..#############', '##..############', '###..###########', '####..##########', '#####...........']

#3975

occupiedIntervals = [[2,6],[4,8],[10,10],[10,12],[14,16]]; freeStart = 7; freeEnd = 11
sortedIntervals = sorted(occupiedIntervals)
stream = [sortedIntervals.pop(0)]
for i in sortedIntervals:
    first , last = i
    previousLast = stream[-1][1]
    if first>previousLast:stream.append(i)
    elif last>previousLast:stream[-1][1] = i[1]
