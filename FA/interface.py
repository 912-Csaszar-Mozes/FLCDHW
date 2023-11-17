from FA import FA
import os


class FAInterface:

    @staticmethod
    def get_help(readFA=False, show_help=True):
        return ("Options: " + "\n\t1) Read FA from file"
                + (("\n\t2) Display initial state"
                    + "\n\t3) Display final state(s)" + "\n\t4) Display set of states" + "\n\t5) Display alphabet"
                    + "\n\t6) Display transitions" + "\n\t7) Try to match a word") if readFA else "")
                + "\n\th) Hide help" + "\n\tx) Exit\n") if show_help else ""

    @staticmethod
    def main():
        readFA = FA("FA/string_const.in")
        command = input(FAInterface.get_help(True, True) + ">>? ").strip()
        show_help = True

        while command != "x":
            if command == "1":
                file_name = "FA/" + input("Please provide a file name (without the .in extension): ") + ".in"
                try:
                    print("PATH" + os.getcwd())
                    readFA = FA(file_name)
                    print("FA successfully read from file")
                except FileNotFoundError:
                    print("!!!File with name `" + file_name + "` not found!!!")
            elif command == "2":
                print("->(" + readFA.init_state + ")")
            elif command == "3":
                print(readFA.format_final_states())
            elif command == "4":
                print(readFA.format_states())
            elif command == "5":
                print(readFA.format_alphabet())
            elif command == "6":
                print(readFA.format_transitions())
            elif command == "7":
                sequence = input("Please provide a sequence: ")
                if readFA.check_sequence(sequence):
                    print("Sequence `" + sequence + "` is matched by the FA!")
                else:
                    print("Sequence `" + sequence + "` is NOT matched by the FA!")
            elif command == "h":
                print("Help hidden")
                show_help = False
            else:
                print("Wrong command; please try something else")
            command = input(FAInterface.get_help(readFA is not None, show_help) + ">>? ")
        print("Interface exited...")


FAInterface.main()
