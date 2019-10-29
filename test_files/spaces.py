# slicing

ham = "fksherfjgvfs;klrgjhs;"

ham[1:9], ham[1:9:3], ham[:9:3], ham[1::3], ham[1:9:]
ham[lower:upper], ham[lower:upper:], ham[lower::step]
ham[lower+offset : upper+offset]
ham[: upper_fn(x) : step_fn(x)], ham[:: step_fn(x)]
ham[lower + offset : upper + offset]

ham[lower + offset:upper + offset]
ham[1: 9], ham[1 :9], ham[1:9 :3]
ham[lower : : upper]
ham[ : upper]


# Spaces between function and arguments
print("asd")
print ("asd")
print    ("lksfhlsdfhjlkad")


# Spaces before indexing
dct['key'] = lst[index]
dct ['key'] = lst [index]

# Spaces around an assignment
x = 1
y = 2
long_variable = 3

x             = 1
y             = 2
long_variable = 3

# Arithmetic operators
x1 = 1
y1 = 2
x1 == y1
x1==y1
x1 is not y1
a =           x1          is      not y1

