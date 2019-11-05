# Arguments indentation

# Aligned with opening delimiter.
# YES
foo = long_function_name(var_one, var_two,
                         var_three, var_four)

# Add 4 spaces (an extra level of indentation)
# to distinguish arguments from the rest.


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


def long_function_name1(
    var_one, var_two, var_three,
        var_four):
    print(var_one)


# Optional. Hence, considered to be correct.
foo = long_function_name(
  var_one, var_two,
  var_three, var_four)


res = []


def func0(var1, var2, var3, var4):
    return var1 + var2 + var3 + var4


# Correct
foo1 = func0(1, 2,
             3, 4)

foo2 = func0(
    1, 2,
    3, 4)

f1 = len(func0(1, 2,
               3, 4))

f11 = len(func0(1, 2,
                3, 4)
          + 10)

f2 = len(func0(
    1, 2,
    3, 4))

f21 = len(func0(
    1, 2,
    3, 4)
          + 10)

# Incorrect
foo3 = func0(1, 2,
    3, 4)

foo4 = func0(1, 2,
        3, 4)

