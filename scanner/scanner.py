import string

from datastructures.symboltable import SymbolTable
from datastructures.hashtable import HashTable


class Scanner:
    removable_separators = [" ", "\n", "\t"]
    non_removable_separators = ["=", "+", "*", "[", "]", ";", "(", ")"]
    # starter separators and what they can continue with; used for double separator support
    starter_separators = {"<": "=", ">": "=", "=": "=", ":": ":", "!": "!=", "&": "&", "|": "|", "?": "!", "@": "!",
                          "~": "!"}
    separators = removable_separators + non_removable_separators + list(starter_separators.keys())

    def __init__(self, file_name, token_in_name):
        self.__tokens = self.__create_token_in(token_in_name)
        self.file_name = file_name
        self.st = SymbolTable()
        self.pif = []
        self.constructed = False
        self.construct_st_pif()

    def get_next_word(self, i, line):
        start_i = i
        # if there is a two character delimiter, handle it
        if line[i] in list(Scanner.starter_separators.keys()):
            if i + 1 < len(line) and line[i + 1] in Scanner.starter_separators[line[i]]:
                i += 1
            i += 1
        else:
            # if there is a string, go until the end of it
            if line[i] == "\"":
                i += 1
                while i < len(line) and line[i] != "\"":
                    i += 1
                i += 1
            else:
                while i < len(line) and line[i] not in Scanner.separators:
                    i += 1
        i += (start_i == i)
        while i < len(line) and line[i] in Scanner.removable_separators:
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
        # special case of the word being 0
        if word == "0":
            return "int"
        # take potential sign into account
        first_ind = 0
        if word[0] == "+" or word[0] == "-":
            first_ind = 1

        # if the word only has a sign, return no-int message
        if len(word) <= first_ind:
            return "no-int"

        # check that first digit is non-zero
        if "123456789".find(word[first_ind]) != -1:
            # check that the subsequent digits are digits and not characters
            for i in range(first_ind + 1, len(word)):
                if not "1234567890".find(word[i]) != -1:
                    return "no-int"
            else:
                return "int"
        return "no-const"

    def parse_is_constant_response(self, word, resp):
        if resp.find("no") != -1:
            if resp.find("str") != -1:
                return "`{}` is not a valid string constant".format(word)
            elif resp.find("int") != -1:
                return "`{}` is not a valid integer constant".format(word)
            else:
                return "`{}` doesn't follow any constant rules".format(word)
        return False

    def is_identifier(self, word):
        if word[0] in string.ascii_letters or word[0] == "_":
            chars = string.ascii_letters + string.digits + "_"
            # check for word to only use allowed characters
            for i in range(1, len(word)):
                if word[i] not in chars:
                    return False
            else:
                return True
        return False

    def remove_separators(self, word):
        while len(word) > 0 and word[0] in Scanner.removable_separators:
            word = word[1:]
        while len(word) > 0 and word[-1] in Scanner.removable_separators:
            word = word[:-1]
        return word

    def construct_st_pif(self):
        with open(self.file_name, "r") as f:
            line_nr = 1
            line = f.readline()
            while line:
                backup = line + ""
                curr_char = 0
                while curr_char < len(line):
                    next_char = self.get_next_word(curr_char, line)
                    word = self.remove_separators(line[curr_char:next_char])
                    # print("Current word <" + word + ">, curr_char=" + str(curr_char) + ", next_char=" + str(
                    #     next_char) + ", length=" + str(len(line)))
                    if word != "":
                        categorized = False
                        error = ""
                        token_nr = self.__tokens.search(word)
                        if token_nr is not None:
                            categorized = True
                            self.pif.append((token_nr, -1))
                        resp = self.parse_is_constant_response(word, self.is_constant(word))
                        # if you could find a valid constant, insert (-1, ST_KEY) into PIF
                        if not resp and not categorized:
                            categorized = True

                            key = self.st.search_by_value(word)
                            if key is None:
                                key = self.st.size()
                                self.st.add(key, word)
                            self.pif.append((-1, key))
                        # else write it in error
                        elif error == "" and not categorized:
                            error = resp

                        if self.is_identifier(word) and not categorized:
                            categorized = True

                            key = self.st.search_by_value(word)
                            if key is None:
                                key = self.st.size()
                                self.st.add(key, word)
                            self.pif.append((-2, key))
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
            with open("scan_out/PIF_" + name + ".txt", "w") as f:
                f.write("{:^12}|{:^12}\n".format("KEYS", "VALUES"))
                for entry in self.pif:
                    f.write("{:^12}|{:^12}\n".format(entry[0], entry[1]))

            with open("scan_out/ST_" + name + ".out", "w") as f:
                for line in self.st.save():
                    f.write(line)
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
