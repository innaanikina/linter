# Arguments indentation

# Aligned with opening delimiter.
# YES
foo = long_function_name(var_one, var_two,
                         var_three, var_four)

# Add 4 spaces (an extra level of indentation) to distinguish arguments from the rest.


def long_function_name(
        var_one, var_two, var_three,
        var_four):
    print(var_one)

# Hanging indents should add a level.
foo = long_function_name(
    var_one, var_two,
    var_three, var_four)


# Arguments on first line forbidden when not using vertical alignment.
# NO
foo = long_function_name(var_one, var_two,
    var_three, var_four)

# Further indentation required as indentation is not distinguishable.
def long_function_name(
    var_one, var_two, var_three,
    var_four):
    print(var_one)

foo = long_function_name(
  var_one, var_two,
  var_three, var_four)

# No extra indentation.
if (this_is_one_thing and
    that_is_another_thing):
    do_something()

# Add a comment, which will provide some distinction in editors
# supporting syntax highlighting.
if  this_is_one_thing and
    that_is_another_thing:
    # Since both conditions are true, we can frobnicate.
    do_something()

# Add some extra indentation on the conditional continuation line.
if (this_is_one_thing
        and that_is_another_thing):
    do_something()


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


# spaces between functions inside the class
class MyClass:
    def func0(self):
        pass

    def func1(self):
        pass



    def func2(self):
        pass


    def func3(self):
        pass
    def func4(self):
        pass

