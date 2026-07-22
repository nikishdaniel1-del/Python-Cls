import os
from os import path
os.makedirs(name='Sample',exist_ok=True)
print(os.system('dir'))
samplePath = r'C:\Users\WELCOME\Documents\Python Cls'
print(path.exists(samplePath))
print(path.basename(samplePath))
print(path.expanduser('~/App'))
print(path.dirname(samplePath))
print(os.getcwd())
print(os.getlogin())
os.chdir(r'C:\Users\WELCOME')
print(os.getcwd())
os.makedirs(name='Sample',exist_ok=True)
os.rename('Sample','Sa')
os.removedirs('Sa')
os.startfile("https://www.leetcode.com")
os.startfile(samplePath)
print(os.cpu_count())