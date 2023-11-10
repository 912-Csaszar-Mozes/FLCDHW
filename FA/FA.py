class FA:
    def __init__(self, file_name):
        self.file_loaded = False
        self.__load_file(file_name)

    def check_sequence(self, sequence):
        # 0 means found, 1 means forward, -1 means backwards
        state = 1
        options = [self.init_state]
        stack = []
        while len(options) > 0:
            pass
        return False

    def format_states(self):
        return ", ".join(map(lambda x: "(" + x + ")", self.states))

    def format_alphabet(self):
        # return ", ".join(map(lambda let: "`" + let + "`", self.alphabet))
        return self.alphabet

    def format_final_states(self):
        return ", ".join(map(lambda x: "((" + x + "))", self.final_states))

    def format_transitions(self):
        return "\n".join(map(lambda state: "\n".
                             join(map(lambda tran: "(" + state + ") ---" + tran[0] + "--> (" + tran[1] + ")",
                                      self.transitions[state])), self.transitions))

    def __load_file(self, file_name):
        self.file_loaded = False
        with open(file_name, "r") as f:
            self.init_state = f.readline().strip()
            self.final_states = f.readline().strip().split("/,/")
            self.states = f.readline().strip().split("/,/")
            self.alphabet = f.readline()[:-1]
            self.transitions = {}
            for transition in f.readline().strip().split("/;/"):
                start, possibilities, end = transition.split("/,/")
                if self.transitions.get(start, None) is not None:
                    self.transitions[start].append((possibilities, end))
                else:
                    self.transitions[start] = [(possibilities, end)]
        self.file_loaded = True
