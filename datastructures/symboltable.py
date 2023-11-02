from datastructures.hashtable import HashTable


class SymbolTable:
    def __init__(self):
        self.hashtable = HashTable()

    def add(self, key, value):
        self.hashtable.add(key, value)

    def search(self, key):
        return self.hashtable.search(key)

    def search_by_value(self, value):
        return self.hashtable.search_by_value(value)

    def size(self):
        return self.hashtable.size
