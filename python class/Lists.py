#  Store 10 numbers in a list and print only the even numbers.
# Find the largest and smallest element in a list of numbers.

# two type of iterative methods
'''sample = [1, 2, 3, 4, 5, 1 , 4]'''
'''for i in range(len(sample)):
    print(i,sample[i])'''

'''for i in sample:
    print(i)'''

'''print(set(sample))'''

# Find Duplicate Elements
'''
result = []
for i in set(sample):
    if sample.count(i)>1:result.append(i)
print(result)'''

# store inputs to lists 
# method 1
'''n = int(input("number : "))
result = [0]*n
for i in range(n):
    result[i] = int(input())
print(result)'''

# method 2
'''result = []
for i in range(int(input("number : "))):result.append(int(input()))
print(result)'''


# Find the largest and smallest element in a list of numbers.
'''stream = [1,5,3,9]
print(min(stream),max(stream))'''


# Count how many times a given number appears in a list.
# : List = [1, 2, 3, 2, 4, 2], Number = 2
# Output: 3

'''List = [1, 2, 3, 2, 4, 2]
Number = int(input())
print(List.count(Number))
result = 0
for i in List:
    if i==Number:result += 1
print(result)
'''
# Create a new list containing the squares of all elements in a given list.
# Example: [1, 2, 3, 4] → [1, 4, 9, 16]
'''print([x**2 for x in List])'''


# Check whether a given number exists in a list or not.
# Example: List = [10, 20, 30, 40], Number = 30
# Output: Found

# number = int(input())
# method 1
'''List = [1,3,2,4,5]
print('exits' if int(input()) in List else 'not exits')'''
# method 2
'''list = [1,3,2,4,5]
num = int(input("Enter num: "))
for i in list:
    if(num == i):
        print("Num is in the list")
        break
else:
    print("Num is not in the list" )'''

# Find the first Duplicate Element.
'''stream = []
for i in [1,2,3,4,7,5,1,2]:
    if i in stream:
        print(i)
        break
    stream.append(i)
else:print('no duplicates found')'''