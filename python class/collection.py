from collections import Counter,ChainMap,defaultdict,OrderedDict,abc,deque

data = defaultdict(int)
string1 = 'aabaadccabbcd'
for i in string1:
    data[i] += 1
print(data)

print(Counter(string1))

defaults = {"theme": "light", "font": 12}
user = {"theme": "dark"}
data = ChainMap(defaults,user)
print(data)

data = OrderedDict([('b',2),('c',1)])
data.setdefault('a',5)
data.move_to_end('b',last=False)
data.popitem(last=False)
print(data)

data = deque([1,3,2,5])
data.rotate(3)
print(data)
data.appendleft(6)
data.extendleft([8,9])
print(data)
print(data.pop())
print(data.popleft())
data.extend([10,11])
print(data)