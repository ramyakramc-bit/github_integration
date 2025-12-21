# Variables and Datatypes

name = 'Mani' # string
age = 25 # Integer
height = 5.6 # Float
is_student = True # Boolean

print('name = ', name)
print('Datatype of name = ', type(name))

print('age = ', age)
print('Datatype of age = ', type(age))

print('height = ', height)
print('Datatype of height = ', type(height))

print('is_student = ', is_student)
print('Datatype of is_student = ', type(is_student))

# 1 - Integer
# 1.5 - Float
# 'a' or "a" or "1" - String
# True - Boolean
# False - Boolean

# Input/Output & Comments
# Comments
# This is a single line comment

"""
This 
is 
Multiline
Comments
"""

#  Output
print('Hello')
# Input
#user_name = input('Enter your name: ')
#print('User name entered = ', user_name)
print('*********************************************************')
# Operators & Expressions
# Arithmetic
x = 10 + 5 # Addition
y = 10 - 3 # Subtraction
z = 4 * 3 # Multiplication
a = 10/ 3 # Division
b = 10//3 # Floor Division
c = 10 %3 # Modulus
d = 2**3 # Exponential

print('x = ', x)
print('y = ', y)
print('z = ', z)
print('a = ', a)
print('b = ', b)
print('c = ', c)
print('d = ', d)

# Comparison
e =  (10>5)
print('e = ', e)
f = (10==10)
print('f = ', f)
g = 10!=5
print('g = ', g)

print('******************')
h =  (10<5)
print('h = ', h)
i = (10!=10)
print('i = ', i)
j = 10==5
print('j = ', j)

# Logical Operators
# k = False and False
# l = False and True
# m = True and False
# n = True and True
# print(k, l, m, n)

k = False or False
l = False or True
m = True or False
n = True or True
print(k, l, m, n)

# Control Flow
# If/else
age = 18
if age>=18:
    print("Adult")
elif age>=13:
    print("Teenager")
else:
    print('Child')
# for loops
fruits = ['apple', 'banana', 'cherry'] # list
# looping through the list
for i in fruits:
    print(i)

# looping using range method
# for i in range(3):
#     print(fruits[i])


# while loops
count = 0
while count<5:
    print(count)
    count = count + 1


# Functins (Including Lambda)
def reverse_string(s): # function definition
    reversed_string = ''
    for char in s:
        print('Char = ', char)
        reversed_string = char + reversed_string
        print('reversed_string = ', reversed_string)
    return reversed_string  # Return Statement

v1 = 'Python'
reversed_string = reverse_string(v1) # Function Calling
print('reversed_string = ', reversed_string)

# slicing
print('Advanced Reversing = ', v1[::-1])


# Finding Max and Minimum values in the list

def find_max(numbers):
    max_value = numbers[0]
    for num in numbers:
        if num> max_value:
            max_value = num
    return max_value

def find_min(numbers):
    min_value = numbers[0]
    for num in numbers:
        if num<min_value:
            min_value = num
    return min_value

numbers = [45, 23, 67, 12, 89, 34]
max_value = find_max(numbers)
min_value = find_min(numbers)
print('Max Value = ', max_value)
print('Min Value = ', min_value)

square = lambda x, y: x**y
# Lambda can conists any number of parameters but will have only 1 expression
print(square(5, 2))


# Traditional way of writing a loop
square_list = []
for i in range(10):
    square_list.append(i**2)
print('square_list = ', square_list)

# List comprehension
ls_square_list = [i**2 for i in range(10)]
print('ls_square_list = ', ls_square_list)

fruits = ['a', 'b', 'c', 'd', 'e']
print('fruits = ', fruits)
for i in range(len(fruits)):
    print(i, fruits[i])

for idx, X in enumerate(fruits):
    print(idx, X)

# zip
names = ['a', 'b', 'c']
ages = [25, 30, 35]
cities = ['z', 'y', 'x']
for n, a, c in zip(names, ages, cities):
    print(n, a, c)

# to install numpy pip install numpy
import numpy as np
arr = np.array([1, 2, 3, 4, 5])
print(arr, type(arr))
print(arr.mean())
print(arr.std())
print(arr.sum())

# pandas data manipulation library pip install pandas
import pandas as pd
data = {'names' : ['a', 'b', 'c'], 'ages' : [25, 30, 35], 'cities' : ['z', 'y', 'x']}

df = pd.DataFrame(data)
print(df)
print(df.head())
print(df.describe())
print(df.info())
print(df['names'])
print(df[['names', 'ages']])
print(df.iloc[0])


arr1 = np.array([1, 2, 3, 4])
arr2 = np.array([1, 2, 3, 4])
print(arr1 + arr2)
print(arr1 * arr2)

# Assignments
#1. Accepts a list of numbers, mean, variance, max, min, sorted output, stats.txt python write
#2. Fibonacci series
#3. data frame (drop na)