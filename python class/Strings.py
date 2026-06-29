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

'''stream = 'Java is a power language'
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
print(result)'''

# Count Digits, Alphabets, and Special Characters.
# Example : Java@123 , o/p : Letters: 4,Digits: 3,Special: 1

'''stream = 'Java@123'
result = [0,0,0]
for i in stream:
    if i.isdigit():result[0] += 1
    elif i.isalpha():result[1] += 1
    else:result[2] += 1
print(result)'''

# Check Rotation. (Example : ABCD,CDAB , Rotation)
'''string1 = 'ABCD'
string2 = 'CDBA'
left = ''
if string1==string2:
    print(True)
    quit()
for i in string1:
    if string1+left==string2:
        print(True)
        quit()
    left += i
    string1 = string1[1:]
print(False)'''

# Reverse Words in a Sentence. 
# Example : Java is awesome , o/p : awesome is Java

string1 = 'Java is awesome'
# method 1
'''output = ''
for i in string1.split()[::-1]:
    output += i+' '
print(output.strip())
'''
# method 2
'''result = currentWord = ''
for i in string1+' ':
    if i == ' ':
        result = ' '+currentWord+result
        currentWord = ''
    else:currentWord += i
print(result[1:])'''