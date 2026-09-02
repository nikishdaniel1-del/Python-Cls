# list
'''print([x for x in range(1,5)])'''

# dictionary
'''print({x:chr(x+97) for x in range(26)})'''

# set
'''print({x for x in 'abbacd'})'''

# generators
'''stream = (x for x in range(5))
for i in stream:
    print(i)'''

# with 2 conditions
'''print(['odd' if x%2 else 'even' for x in range(1,5)])'''

# with 1 condition
'''print([x for x in range(1,5) if x%2])'''

# with 3 or more conditions
def sample(x):
    if x==1:return 'One'
    elif x==2:return 'Two'
    else:return 'Three'
print([sample(x) for x in range(1,4)])