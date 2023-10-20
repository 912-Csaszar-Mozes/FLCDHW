from symboltable import SymbolTable
import random


def test(nr_runs=1, test_size=1000):
    for i in range(nr_runs):
        with open("test_out/test" + str(i + 1) + ".txt", "w") as f:
            ht = SymbolTable()
            f.write("Initializing test number " + str(i + 1) + " with " + str(
                test_size) + " value inserts into the hashtable\n")
            keys = [random.randint(100000000, 15000000000) for _ in range(test_size)]
            values = [random.randint(1000, 150000) for _ in range(test_size)]
            for j in range(len(keys)):
                ht.add(keys[j], values[j])
            f.write("Added " + str(test_size) + " values successfully.\n")
            for j in range(len(keys)):
                if ht.search(keys[j]) != values[j]:
                    f.write("Search unsuccessful, expected value {} at place {}, got {}\n".format(values[j], j,
                                                                                                  ht.search(keys[j])))
                    return
                f.write("Value " + str(values[j]) + " successfully found at key " + str(keys[j]) + "\n")
            f.write("Search successful\n")


test(5)
