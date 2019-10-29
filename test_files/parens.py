for i in range(0, 5):
    print("Hello")

for (i) in (range(0, 5)):
    print("Hello there")

for(i)in(range(0, 5)) :
    print("This is a test")


def func0():
    return ("Sample string")


if (3 > 4):
    print("This should never ever happen")
elif(3 == 4):
    print("This should never ever happen as well")
else:
    print("This is what's gonna happen")

if (this_is_one_thing and
    that_is_another_thing):
    do_something()

if (this_is_one_thing or that_is) and that_is_another_thing:
    do_something()

try:
    print()
except (IndexError):
    print("!")

while (True):
    break

for enc in encoding:
    try:
        open(file_name, encoding=enc).read()
    except (UnicodeDecodeError, LookupError):
        pass
    else:
        correct_encoding = enc
        break

