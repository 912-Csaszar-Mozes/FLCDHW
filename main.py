from scanner.scanner import Scanner


def main():
    program_names = ["p3.sisl"]
    token_in = "token.in"
    for program in program_names:
        sc = Scanner(program, token_in)
        sc.construct_st_pif()
        sc.save(program)


main()
