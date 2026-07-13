from collections import Counter,ChainMap,defaultdict,UserDict,OrderedDict,abc,deque,UserList,UserString,namedtuple

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