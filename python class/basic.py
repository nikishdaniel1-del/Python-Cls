# number = int(input('Enter the number : '))
# end : 
# for i in range(number):print(i,end='*')

# Output : 
# Enter the number : 5
# 0*1*2*3*4*

# sep : 
# print(*range(number),sep='*')


# Practice :

# print(*range(1,6))


# number = int(input('Enter the number : '))
# start = int(input('Enter the start number : '))
# step = int(input('Enter the step number : '))
# for i in range(start,number,step):
#     print(i)


'''1*2*3*4
1*2*3
1*2
1'''

# print(1,2,sep='*')

for i in range(int(input('Enter the number : ')),0,-1):print(*range(1,i+1),sep='*')