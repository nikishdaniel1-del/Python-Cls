# square pattern
row = int(input('Enter the number of rows : '))
'''for i in range(row):print('* '*row)'''

# hollow square pattern
'''for i in range(1,row+1):
    if i==1 or i==row:print(('* '*row)[:-1])
    else:print('* '+'  '*(row-2)+'*')'''

# Left Triangle 
'''for i in range(1,row+1):
        print(('* '*i).strip())'''

# Left Hollow Triangle
'''for i in range(1,row+1):
    if i==1 or i==row:print(('* '*i).strip())
    else:print('* '+'  '*(i-2)+'*')'''

# Right Triangle
'''for i in range(1,row+1):print('  '*(row-i)+('* '*i).strip())'''

# Right Hollow Triangle
'''for i in range(1,row+1):
    if i==1 or i==row:print('  '*(row-i)+('* '*i).strip())
    else:print('  '*(row-i)+'* '+'  '*(i-2)+'*')'''

# Inverted Left Triangle 
'''for i in range(1,row+1):print(('* '*(row-i+1)).strip())'''

# Inverted Left Hollow Triangle
'''for i in range(1,row+1):
    if i == 1 or i==row:print(('* '*(row-i+1)).strip())
    else:print('* '+'  '*(row-i-1)+'*')'''

# Inverted Right Triangle
'''for i in range(1,row+1):spaces = i-1;print('  '*spaces+'* '*(row-spaces))'''

# Inverted Right Hollow Triangle
'''for i in range(1,row+1):
    spaces = i-1
    if i==1 or i==row:print('  '*spaces+'* '*(row-spaces))
    else:print('  '*spaces+'* '+'  '*(row-i-1)+'*')'''

# Pyramid Pattern
'''for i in range(1,row+1):print('  '*(row-i)+('* '*(2*i-1)).strip())'''

# Pyramid Hollow Pattern
'''for i in range(1,row+1):
    if i==1 or i==row:print('  '*(row-i)+('* '*(2*i-1)).strip())
    else:print('  '*(row-i)+'* '+'  '*(2*(i-1)-1)+'*')'''

# Inverted Pyramid Pattern
'''for i in range(row):print('  '*i+('* '*(2*row-2*i-1)).strip())'''

# Inverted Hollow Pyramid Pattern
'''for i in range(row):
    base = 2*row-2*i-1
    if i==0 or i==row-1:print('  '*i+('* '*(base)).strip())
    else:print('  '*i+'* '+'  '*(base-2)+'*')'''

# Diamond Pattern
'''index = reverse = 0
half = row//2
for i in range(row):
    if i==half:
        reverse = 1
        if row%2:print('* '*(2*index+1));index-=1;continue
        index-=1
    print('  '*(half-index)+'* '*(2*index+1))
    if reverse:index-=1
    else:index+=1'''

# Hollow Diamond Pattern
'''index = reverse = 0
half = row//2
for i in range(row):
    if i==half:
        reverse = 1
        if row%2:print('* '+'  '*(2*index-1)+'*');index-=1;continue
        index-=1
    if i==0 or i==row-1:print('  '*(half-index)+'*')
    else:print('  '*(half-index)+'* '+'  '*(2*index-1)+'*')
    if reverse:index-=1
    else:index+=1'''

# Butterfly Pattern 
# for i in range(row):
