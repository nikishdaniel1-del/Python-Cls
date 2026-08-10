string1 = 'Name : {name} Age : {age}'
print(string1.format(name="Daniel",age=22))
print('Name : {1} Age : {0}'.format('22','Daniel'))

print(f'{10:b}')
name = 'Daniel'
age = 22
print(f'Name : {name} Age : {age}')

print(f'{3.12546:.2f}')

print(f'{20:5}')
print(f'{20:3}')

print(f'{20:04}')

print(f'{20000:,}')
print(f'{0.98:.2%}')

print(f'-{20:>05}-')
print(f'-{20:<05}-')
print(f'-{20:^05}-')