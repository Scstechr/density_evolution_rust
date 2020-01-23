from datetime import datetime
from misc import strip_line, display
from proc import start, init_and_eval, mutation_loop


def main():
    origin = datetime.now()

    log, sub, cands = start(origin)

    candidates = init_and_eval(origin)

    best, count = mutation_loop(origin, log, sub, cands, candidates)
    print(f"\n \033[41mBEST OUT OF {count} ITERATION(S)\033[m")
    strip_line(space=False)
    display(best)


main()
