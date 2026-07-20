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
keyBoard = ['qwertyuiop','asdfghjkl','zxcvbnm']
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
print(result)

keyDictionary = {'q': 0, 'w': 0, 'e': 0, 'r': 0, 't': 0, 'y': 0, 'u': 0, 'i': 0, 'o': 0, 'p': 0, 'a': 1, 's': 1, 'd': 1, 'f': 1, 'g': 1, 'h': 1, 'j': 1, 'k': 1, 'l': 1, 'z': 2, 'x': 2, 'c': 2, 'v': 2, 'b': 2, 'n': 2, 'm': 2}
words = ["Hello","Alaska","Dad","Peace",'has']
result = []
for word in words:
    base = ''
    wordLower = word.lower()
    for i in wordLower:
        if not base:base = keyDictionary[i]
        elif keyDictionary[i] != base:break
    else:result.append(word)
print(result)


# Form words in diagonal flow
words = ['card','can','dad']
# output : ['c','ca','rad','an','d']