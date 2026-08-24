original = int(input())
def sample(n,rev=0):
    if n==0:return sample(n+1,1)
    elif n==original and rev:return f'{n} '
    else:return f'{n} '+sample(n+1 if rev else n-1,rev)
print(sample(original))

half = original//2
def diamond(n,rev=0):
    if n==half:return '*'*(2*n-1)+'\n'+diamond(n-1,1)
    elif n==0 and rev:return ''
    else:return (' '*(half-n)+'*'*(2*n-1)+'\n')+diamond(n-1 if rev else n+1,rev)
print(diamond(1))