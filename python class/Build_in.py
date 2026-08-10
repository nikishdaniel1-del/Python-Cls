sample = [1,2,3,4]
print(list(filter(lambda x:x%2,sample)))
print([x for x in sample if x%2])
print(list(map(lambda x:x**2,sample)))
print([x**2 for x in sample])
print(any([x%2 for x in [2,4,6]]))

twoDlist = [[1,2,4],[3,5,6],[7,8,9]]
print(list(zip(*twoDlist)))