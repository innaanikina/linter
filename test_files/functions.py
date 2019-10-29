# Function parameters
# CORRECT
def complex1(real, imag=0.0):
    return magic(r=real, i=imag)


# INCORRECT
def complex1(real, imag = 0.0):
    return magic(r = real, i = imag)


# Spaces between the function and its arguments
# TODO убрать повторные проверки
print()

print  ()

print                  ()

