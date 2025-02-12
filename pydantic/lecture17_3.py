'''
Author : Aditya Bhatt
Date : 12-02-2025

Understanding dataclasses in python

Advantages of dataclasses over normal classes:

1.Automatically adds __init__ method
2.It makes the class attributes clear at a glance
'''

from dataclasses import dataclass

@dataclass
class Person:
    name: str
    age: int

a=Person("Aditya",20)

print(a)
print(a.name)
print(a.age)


#Without dataclass
class Person:
    def __init__(self,name,age):
        self.name=name
        self.age=age

b=Person("Aditya",20)

print(b)
print(b.name)
print(b.age)








