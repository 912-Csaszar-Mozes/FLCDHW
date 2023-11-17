class Transition:
    def __init__(self, symbols, end):
        self.symbols = symbols
        self.end = end


class FA:
    def __init__(self, file_name):
        self.file_loaded = False
        self.__load_file(file_name)

    def check_sequence(self, sequence):
        if len(sequence) == 0:
            return self.init_state in self.final_states
        stack = [[self.init_state, 0]]
        match_ind = 0
        # while there are more options to explore, go for it
        while len(stack) > 0:
            # check if terminal is in alphabet
            if sequence[match_ind] not in self.alphabet:
                return False
            state, option = stack[-1]
            # print("Current state {:^5} with option {:^5}".format(state, option))
            # if you can go forward
            if option < len(self.transitions.get(state, [])):
                # if the next element of the sequence can be obtained by a transition
                if sequence[match_ind] in self.transitions[state][option].symbols:
                    # add new option to the stack
                    stack.append([self.transitions[state][option].end, 0])
                    match_ind += 1
                    # check if the sequence is fully matched
                    if match_ind == len(sequence):
                        # if we are at a final state, return True
                        if stack[-1][0] in self.final_states:
                            return True
                        # else backtrack
                        else:
                            stack[-1][1] += 1
                            match_ind -= 1
                # if not found the correct option
                else:
                    stack[-1][1] += 1
            # if you need to go back because of lack of options
            else:
                stack.pop()
                match_ind -= 1
                # if the stack is not empty, move the step before one transition try forward
                if len(stack) > 0:
                    stack[-1][1] += 1
        return False

    def format_states(self):
        return ", ".join(map(lambda x: "(" + x + ")", self.states))

    def format_alphabet(self):
        # return ", ".join(map(lambda let: "`" + let + "`", self.alphabet))
        return self.alphabet

    def format_final_states(self):
        return ", ".join(map(lambda x: "((" + x + "))", self.final_states))

    def format_transitions(self):
        return "\n".join(map(lambda state: "\n".join(
            map(lambda tran: "(" + state + ") ---" + tran.symbols + "--> (" + tran.end + ")",
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
                    self.transitions[start].append(Transition(possibilities, end))
                else:
                    self.transitions[start] = [Transition(possibilities, end)]
        self.file_loaded = True
