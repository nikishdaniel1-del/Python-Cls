from faker import Faker

fake = Faker()

print(fake.name())
print(fake.language_name())
print(fake.random_int(20,85))
print(fake.random_int(1,1000))