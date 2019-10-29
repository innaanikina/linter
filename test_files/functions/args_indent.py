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
