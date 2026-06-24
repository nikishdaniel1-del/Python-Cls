stream = 'DanIEl'

# looping in string
'''for i in stream:
    print(i)'''

# concatenation
'''newString = stream+' y'
print(newString)'''

# multiplication
'''newString = stream*2
print(newString)'''


# Check Anagram. (Example : listen – silent)
'''s1 = 'llisten'
s2 = 'silent'
stream1 = [0]*26
stream2 = [0]*26
for i in s1.lower():
    stream1[ord(i)-97] += 1
print(stream1)
for i in s2.lower():
    stream2[ord(i)-97] += 1
print(stream2)
print('Anagram' if stream2==stream1 else 'Not anagram')'''

# Compress a String. (Example : aaabbcccc , a3b2c4)
'''s1 = input()
result = ''
stream = [0]*26
for i in s1.lower():stream[ord(i)-97] += 1
index = 0
for x in stream:
    if x:
        result += chr(index+97)+str(x)
    index += 1
print(result)'''

stream = 'Java is a power language'
largest = currentLength = 0
result = currentWord = ''
for i in stream+' ':
    if i == ' ':
        if currentLength>largest:
            result = currentWord
            largest = currentLength
        currentWord = ''
        currentLength = 0
    else:
        currentLength += 1
        currentWord += i
print(result)