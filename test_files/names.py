# Forbidden names
l = 10
I = "string"
O = "hey, I am an incorrectly (i.e. ambiguously) named variable"

# Snake-case var names
snake_case_var = 0
notSnakeCaseVar = 1
ThisOneIsMixed = 2
__blah__ = 3
__still_snake_case__ = 4
__notReallyThough__ = 5
_iAmAlsoIncorrect = 6
IAMINCORRECT = 7

# Snake case functions names


def func_num_one():
    print("Correct")


def funcNumTwo():
    print("Incorrect")


def __func3__():
    print("correct")


def FUNCFOUR():
    print("Incorrect")


def __funcNumberFive():
    print("Incorrect again")

# camel case variables

camelCaseVar = 0


# camel case functions


def functionOne():
    print("Correct")


def FunctionTwo():
    print()


def function_three():
    print("Incorrect")


# class names

class MyClass:
    pass


class my_class:
    pass


class thisIsMyClass:
    pass
