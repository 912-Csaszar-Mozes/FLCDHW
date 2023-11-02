import string

from datastructures.symboltable import SymbolTable
from datastructures.hashtable import HashTable


class Scanner:
    separators = [" ", "\n", "\t", "=", "<", "+", "*", "[", "]"]

    def __init__(self, file_name, token_in_name):
        self.__tokens = self.__create_token_in(token_in_name)
        self.file_name = file_name
        self.st = SymbolTable()
        self.pif = HashTable()
        self.constructed = False

    def get_next_word(self, i, line):
        while i < len(line) and line[i] not in Scanner.separators:
            i += 1
        while i < len(line) and line[i] in [" ", "\n", "\t"]:
            i += 1
        return i

    def is_constant(self, word):
        # Is string constant
        if word[0] == "\"" and word[-1] == "\"":
            if word.count("\"") == 2:
                return "str"
            else:
                return "no-str"
        # Is numeric constant
        # check that first digit is non-zero
        first_ind = 0
        if word[0] == "+" or word[0] == "-":
            first_ind = 1
        if word == "0":
            return "int"
        if len(word) <= first_ind:
            return "no-int"
        if "123456789".find(word[first_ind]):
            for i in range(first_ind + 1, len(word)):
                if not "1234567890".find(word[i]):
                    return "no-int"
            else:
                return "int"
        return "no-const"

    def parse_is_constant_response(self, word, resp):
        if resp.find("no"):
            if resp.find("str"):
                return "`{}` is not a valid string constant".format(word)
            elif resp.find("int"):
                return "`{}` is not a valid integer constant".format(word)
            else:
                return "`{}` is doesn't follow any constant rules".format(word)
        return False

    def is_identifier(self, word):
        if word[0] in string.ascii_letters or word[0] == "_":
            chars = string.ascii_letters + string.digits + "_"
            for i in range(1, len(word)):
                if word[i] not in chars:
                    return False
            else:
                return True
        return False

    def construct_st_pif(self):
        with open(self.file_name, "r") as f:
            line_nr = 1
            line = f.readline()
            while line:
                backup = line + ""
                curr_char = 0
                while curr_char < len(line):
                    next_char = self.get_next_word(curr_char, line)
                    if next_char == curr_char:
                        next_char += 1
                    word = line[curr_char:next_char].strip()
                    print("Current word <" + word + ">, curr_char=" + str(curr_char) + ", next_char=" + str(
                        next_char) + ", length=" + str(len(line)))
                    if word != "":
                        categorized = False
                        error = ""
                        token_nr = self.__tokens.search(word)
                        if token_nr:
                            categorized = True
                            self.pif.add(token_nr, -1)
                        resp = self.parse_is_constant_response(word, self.is_constant(word))
                        # if you could find a valid constant, insert (-1, ST_KEY) into PIF
                        if not resp:
                            categorized = True

                            key = self.st.search_by_value(word)
                            if not key:
                                key = self.st.size()
                                self.st.add(key, word)
                            self.pif.add(-1, key)
                        # else write it in error
                        elif error == "":
                            error = resp

                        if self.is_identifier(word):
                            categorized = True

                            key = self.st.search_by_value(word)
                            if not key:
                                key = self.st.size()
                                self.st.add(key, word)
                            self.pif.add(-2, key)
                        elif error == "":
                            error = "could not categorize word `{}`".format(word)

                        if not categorized:
                            print("ERROR AT LINE {}, AT WORD `{}`:".format(line_nr, word))
                            print("Error text:> " + error)
                            print(backup)
                            return
                        # while next_char < len(line) and line[next_char] in [" ", "\n", "\t"]:
                        #     next_char += 1
                    curr_char = next_char
                line = f.readline()
                line_nr += 1
            self.constructed = True

    def save(self, name):
        if self.constructed:
            pass
        else:
            raise Exception("ERROR: PIF and ST not constructed yet; nothing to save")

    def __create_token_in(self, token_in_name):
        with open(token_in_name, "r") as f:
            tokens = f.readline().strip().split(" ")
            tokens_dict = HashTable()
            i = 0
            for token in tokens:
                tokens_dict.add(token, i)
                i += 1
            return tokens_dict
