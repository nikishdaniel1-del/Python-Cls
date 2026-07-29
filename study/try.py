lists = [0,1,0,2,3,8,-1]
length = zeros = 0
for i in lists:
    if i==0:zeros += 1
    length += 1
for i in range(length-zeros):
    currentElement = lists[i]
    if currentElement==0:
        for j in range(i+1,length):
            if lists[j]:lists[i] , lists[j] = lists[j] , lists[i];break
print(lists)