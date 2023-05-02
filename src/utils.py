import importlib.util
import os
import random
import string
import re
from src import config


def get_main_result(directory_path):
    module_name = os.path.basename(directory_path)
    module_path = directory_path

    # Load the module from the file path
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Call the main() function and return the result
    return module.main()


def get_ave_result(directory_path):
    l = []
    for i in range(config.check_itr):
        print(".", end="")
        l.append(get_main_result(directory_path))
    return sum(l) / len(l)


def generate_random_string(length):
    # Generate a random string of length `length` using ASCII letters and digits
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choices(letters_and_digits, k=length))


def count_spaces(s):
    """
    Returns the number of tabs at the beginning of the string s.
    """
    pattern = re.compile(r' +')
    match = pattern.match(s)
    if match:
        return len(match.group(0))
    else:
        return 0
