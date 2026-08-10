# Count Frequency.
# aaababbcddd - a4b3c1d3
'''string = "aaababbcddd"
freq = {}
for i in string:
    if i in freq:freq[i] += 1
    else:freq[i] = 1'''

# Sort String wrt frequency.
'''sortedFreq = sorted(freq,key=lambda x:freq[x])'''

# Grouping. Example : {"John":20, "Mary":21, "Tom":20, "Alice":21}; o/p:{ 20:["John","Tom"], 21:["Mary","Alice"]}.
'''dictionary = {"John":20, "Mary":21, "Tom":20, "Alice":21}
grouped = {}
for i in dictionary:
    if dictionary[i] in grouped:grouped[dictionary[i]].append(i)
    else:grouped[dictionary[i]] = [i]
print(grouped)'''

# largest palindrome in a string
'''result = ones = ''
for i in sortedFreq[::-1]:
    frequency = freq[i]
    half = frequency//2
    if frequency%2 and not ones:
        result += i*half
        ones = i
    elif frequency>1:
        result += i*half
largestPalindrome = result + ones + result[::-1]
print(largestPalindrome)
print(largestPalindrome == largestPalindrome[::-1])'''

# Word Pattern : pattern="abba" , sentence="dog cat cat dog" . o/p : True.
'''pattern = "abba"
sentence = "dog cat cat dog"
words = sentence.split()
stream = {}
for i in range(len(pattern)):
    currentWord , currentMatch = pattern[i] , words[i]
    if currentWord in stream and stream[currentWord] != currentMatch:
        print(False)
        quit()
    stream[currentWord] = currentMatch
print(True)'''

'''stream = ["eat","tea","tan","ate","nat","bat"]
result = {}
for i in stream:
    data = {}
    for x in i:
        if x not in data:data[x] = 0
        data[x] += 1
    compressedString = ''
    for x in sorted(data):
        compressedString += x+str(data[x])
    if compressedString not in result:
        result[compressedString] = []
    result[compressedString].append(i)
print(result)'''