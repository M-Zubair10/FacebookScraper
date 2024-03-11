import random
import string

import names


def username():
    username = first_name() + surname() + str(random.randint(0, 1000))
    return username


def first_name():
    return names.get_first_name()


def surname():
    return names.get_last_name()


def password(numbers=True, symbols=True):
    nums = list("0123456789")
    symb = list("~`!@#$%^&*()_-+={[}]|\:;'<,>.?/")
    letters = list(string.ascii_letters)
    while True:
        if not numbers and symbols:
            characters = letters + symb
        elif not numbers and not symbols:
            characters = letters
        elif not symbols and numbers:
            characters = letters + nums
        if not numbers or not symbols:
            return "".join([random.choice(characters) for i in range(random.randint(12, 18))])
        else:
            characters = nums + symb + letters
            password = "".join([random.choice(characters) for i in range(random.randint(12, 18))])
            if any(s in password for s in "!@#$%^&*()_+{}|") and any(n in password for n in "0123456789") and any(
                    s in password for s in string.ascii_uppercase):
                return password

