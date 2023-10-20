# We need the methods add and search
# We need to be able to search by the name of the identifier/constant
# We also need to be able to search by the id of the identifier/constant
import random


class Hashtable:
    def __init__(self, m=2 ** 8, c=0.618033988):
        self.c = c
        self.m = m
        self.table = [[] for _ in range(self.m)]

    def hash_function(self, key):
        if isinstance(key, int):
            return int(self.m * ((key * self.c) % 1))
        return None

    def add(self, key, value):
        self.table[self.hash_function(key)].append((key, value))

    def search(self, key):
        for entry in self.table[self.hash_function(key)]:
            if entry[0] == key:
                return entry[1]
        return None


def test(nr_runs=1, test_size=1000):
    for i in range(nr_runs):
        with open("test_out/test" + str(i + 1) + ".txt", "w") as f:
            ht = Hashtable()
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
