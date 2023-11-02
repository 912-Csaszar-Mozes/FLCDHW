import string

from symboltable import SymbolTable
import random


def one_test(test_size, key_generator, value_generator):
    ht = SymbolTable()
    keys = [key_generator() for _ in range(test_size)]
    values = [value_generator() for _ in range(test_size)]
    for j in range(len(keys)):
        ht.add(keys[j], values[j])
    # search by key
    key_errors = 0
    for j in range(len(keys)):
        if ht.search(keys[j]) != values[j]:
            key_errors += 1
    value_errors = 0
    # search by values
    for j in range(len(keys)):
        if ht.search_by_value(values[j]) != keys[j]:
            key_errors += 1
    if key_errors != 0 or value_errors != 0:
        return "Found {} errors when searching by key, {} when searching by value after inserting {} elements.".format(
            key_errors, value_errors, test_size)
    else:
        return "No errors found after inserting, searching and reverse-searching {} elements.".format(test_size)


def gen_rand_int(min, max):
    return random.randint(min, max)


def gen_rand_str(min, max):
    return ''.join(random.choice(string.ascii_letters) for i in range(random.randint(min, max)))


def test(nr_runs=1, test_size=1000):
    with open("test_out/sym_tb_tests.txt", "w") as f:
        for i in range(nr_runs):
            ret_val = one_test(test_size, lambda: gen_rand_str(7, 10), lambda: gen_rand_str(7, 10))
            f.write("Test number {} returned with result: \n\t {}\n".format(i + 1, ret_val))


test(5)
