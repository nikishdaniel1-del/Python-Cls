original = int(input())
def sample(n,rev=0):
    if n==0:return sample(n+1,1)
    elif n==original and rev:return f'{n} '
    else:return f'{n} '+sample(n+1 if rev else n-1,rev)
print(sample(original))