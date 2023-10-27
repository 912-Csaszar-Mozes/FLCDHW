# We need the methods add and search
# We need to be able to search by the name of the identifier/constant
# We also need to be able to search by the id of the identifier/constant
import random


class HashTable:
    def __init__(self, m=2 ** 8, c=0.618033988):
        self.c = c
        self.m = m
        self.table = [[] for _ in range(self.m)]
        self.reverse_table = [[] for _ in range(self.m)]

    def hash_function(self, key):
        if isinstance(key, int):
            return int(self.m * ((key * self.c) % 1))
        elif isinstance(key, str):
            nr = 0
            for i in range(len(key)):
                nr += (ord(key[i]) % 100) ** i
            return self.hash_function(nr)
        return None

    def add(self, key, value):
        self.table[self.hash_function(key)].append((key, value))
        self.reverse_table[self.hash_function(value)].append((value, key))

    def search(self, key):
        for entry in self.table[self.hash_function(key)]:
            if entry[0] == key:
                return entry[1]
        return None

    def search_by_value(self, value):
        for entry in self.reverse_table[self.hash_function(value)]:
            if entry[0] == value:
                return entry[1]
        return None
