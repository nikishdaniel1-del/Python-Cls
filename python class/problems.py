# validate brackets

'''brackets = '{[()]}'
stack = []
pairs = {'}':'{',']':'[',')':'('}
for i in brackets:
    if i in '{[(':
        stack.append(i)
    elif stack and pairs[i]==stack[-1]:
        stack.pop()
    else:
        print(False)
        quit()
print(False if stack else True)'''

# Reverse Vowels of a String
'''string = "Python Is A Programming Language"
string = list(string)
index1 = 0
index2 = len(string)-1
while index1<=index2:
    first = string[index1] in 'AEIOUaeiou'
    second = string[index2] in 'AEIOUaeiou'
    if first and second:
        string[index1],string[index2] = string[index2],string[index1];index1+=1;index2-=1
    if not first:
        index1 += 1
    elif not second:
        index2 -= 1
print(''.join(string))'''


# keyboard row
'''keyBoard = ['qwertyuiop','asdfghjkl','zxcvbnm']
words = ["Hello","Alaska","Dad","Peace",'has']
result = []
for word in words:
    base = ''
    wordLower = word.lower()
    for i in wordLower:
        if not base:
            for x in keyBoard:
                if i in x:base=x;break
        elif i not in base:break
    else:result.append(word)
print(result)'''

'''keyDictionary = {'q': 0, 'w': 0, 'e': 0, 'r': 0, 't': 0, 'y': 0, 'u': 0, 'i': 0, 'o': 0, 'p': 0, 'a': 1, 's': 1, 'd': 1, 'f': 1, 'g': 1, 'h': 1, 'j': 1, 'k': 1, 'l': 1, 'z': 2, 'x': 2, 'c': 2, 'v': 2, 'b': 2, 'n': 2, 'm': 2}
words = ["Hello","Alaska","Dad","Peace",'has']
result = []
for word in words:
    base = ''
    wordLower = word.lower()
    for i in wordLower:
        if not base:base = keyDictionary[i]
        elif keyDictionary[i] != base:break
    else:result.append(word)
print(result)'''


# Form words in diagonal flow
'''words = ['car','can','dad','python']
largest = None
for i in words:
    currentLength = len(i)
    if largest==None or currentLength>largest:largest=currentLength
words = [x+' '*(largest-len(x)) for x in words]
result = []
index = reverse = 1
for i in words:
    if not result:result = list(i)
    else:
        for x in range(largest-1):
            if reverse:result[index+x] = i[x]+result[index+x]
            else:result[index+x] += i[x]
            reverse = not reverse
        if largest%2:reverse = not reverse
        result.append(i[-1])
        index += 1
print(result)'''

# Equal Score Substrings
'''word = 'azby'
right = left = 0
for i in word:
    right += ord(i)-96
for i in word:
    value = ord(i)-96
    left += value
    right -= value
    if left==right:print(True);quit()
print(False)'''

# Zigzag Conversion.
'''string = "PAYPALISHIRING"
rows = 4
stream = ['']*rows
index = rev = 0
for x in string:
    stream[index] += x
    if index == 0:rev = 0
    elif index == rows-1:rev = 1
    index += -1 if rev else 1
print(''.join(stream))'''


'2*((4-3)*4)'
'2*4-3'