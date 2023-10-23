from hashtable import HashTable


class SymbolTable:
    def __init__(self):
        self.hashtable = HashTable()

    def add(self, key, value):
        self.hashtable.add(key, value)

    def search(self, key):
        return self.hashtable.search(key)
