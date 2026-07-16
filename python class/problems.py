# validate brackets

brackets = '{[()]}'
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
print(False if stack else True)

# Reverse Vowels of a String
