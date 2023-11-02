from scanner.scanner import Scanner


def main():
    program_names = ["p1.sisl", "p2.sisl", "p3.sisl", "perr.sisl"]
    token_in = "token.in"
    for program in program_names:
        sc = Scanner(program, token_in)
        sc.construct_st_pif()
        if sc.constructed:
            print("lexically correct")
            sc.save(program.split(".")[0])


main()
